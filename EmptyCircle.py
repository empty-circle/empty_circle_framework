#!/usr/bin/env python3
# https://github.com/empty-circle/empty-circle.git
# The Empty Circle Reconnaissance Framework - 2023
# v 0.5

# Developed by David Kuszmar & Nikita Kotlyarov
# https://github.com/empty-circle
# https://github.com/thenikitakotlyarov

# The Empty Circle is a recon framework for pentesters and
# redteamers. It is meant to be simple, easy to use, and easy
# to modify. Check the readme for exact instructions and a
# walkthrough.


# Import necessary libraries
import os

import configparser

import asyncio

from pathlib import Path
import time




class Console:
    """
    TODO:fill in this section
    """
    def __init__(self):
        self.state = 0
        self.running = True

        self.work_dir = "./"


        self.module_dir = 'modules'
        self.wspace_dir = 'workspaces'

        self.global_config_file = "global_config.toml"

        self.module_config_file = f"{self.module_dir}.toml"
        self.wspace_config_file = f"{self.wspace_dir}.toml"

        self.fs_struct = {
            f"{self.wspace_dir}/",
            f"{self.module_dir}/",
            f"{self.global_config_file}",
            f"{self.module_config_file}",
            f"{self.wspace_config_file}"
            }


        self.GlobalConfiger = configparser.ConfigParser()
        self.ModuleConfiger = configparser.ConfigParser()
        self.WspaceConfiger = configparser.ConfigParser()

        self.wspaces = dict()
        self.modules = dict()

        self.startup()



    def startup(self):
        # put startup events here
        self.clear()


        print("Loading Empty Circle Framework...")

        # loads modules
        self.ModuleConfiger.read(self.module_config_file)
        self.module_options =[ e for e in self.ModuleConfiger ]
        self.module_options.remove('DEFAULT')
        for module_name in self.module_options:
            self.module_load(module_name)

        # loads workspaces
        self.WspaceConfiger.read(self.wspace_config_file)
        self.wspace_options = self.strap(self.work_dir)


        self.wspaces['__default__'] = {'name' : "__no_workspace__",
                                       'path' : "./__default__",
                                       'info' : "No Workspace Set" }

        for wspace_name in self.wspace_options:
            self.wspace_load(name=wspace_name)

        self.wspaces['__current__'] = dict(self.wspaces['__default__'])


        self.WspaceConfiger.read(self.wspace_config_file)
        self.wspace_load(options=self.wspace_options)






    def strap(self,include_dir):
        include_file_path = f"{include_dir}.include"

        if not os.path.isfile(include_file_path):
            self.error(f"missing critical file {include_file_path}!",0)
        self.paths = self.include(f"{include_dir}.include")

        for required_fs in self.fs_struct:
            if f"{self.work_dir}{required_fs}" not in self.paths:
                self.error(f"missing critical folder {required_fs}",0)


        return self.paths[f"{self.work_dir}{self.wspace_dir}/"][0][1]



    @staticmethod
    def include(include_file_path):
        # print(f"including {include_file_path}")
        paths = dict()

        with open(include_file_path,'r') as f:
            for line in f.readlines():
                line = line.strip('\n').split(' ')
                mod, path = line[-1], ' '.join(line[:-1])
                if mod == 'r':
                    paths[path] = [ f for f in os.walk(path) ]
                elif mod == 'o':
                    with open(path) as f:
                        paths[path] = ''.join(f.readlines())
        def announce_include():
            for e in paths:
                if type(paths[e]) == str:
                    print(f"found [{e}] :\n\"\"\"\n{paths[e]}\n\"\"\"\n")
                elif type(paths[e]) == list:
                    print(f"found [{e}] :\n\"\"\"\n")

                    for i in paths[e]:
                        print(f"\t{i}")

                    print("\n\"\"\"\n")

        #announce_include()

        return paths


    #helpers
    def prompt(self,msg):
        tstamp = time.strftime("%a, %H:%M", time.gmtime())
        wspace = self.wspaces['__current__']['name']
        return input(f"\n\n  {tstamp}\n  [{wspace}]\n  <{msg}> :\t")

    @staticmethod
    def error(e,cont):
        if cont:
            input(f"error: {e}\n  <enter to proceed> :\t")
            pass
        else:
            input(f"critical error! {e}\n  <exiting> :\t")
            exit()

    def agent(self):
        while True:
                try:
                    attempt = self.prompt("  enter code, agent :\t")
                    if attempt == 'exit':
                        break
                    exec(attempt) # probably the most stress inducing line of code i've ever written
                except Exception as e:
                    self.error(e,1)
                    pass

    @staticmethod
    def clear():
        os.system('clear') # Clears the terminal screen



    #menus
    def splash(self):
        self.clear()

        width = os.get_terminal_size()[0]
        spanner = f"\n{''.join(['=' for i in range(width)])}"

        title_text = "THE EMPTY CIRCLE"
        title_spanner = ''.join([' ' for i in range(int(width/2)-int(len(title_text)/2)-1)])
        title = f"\n[{title_spanner}{title_text}{title_spanner}]"

        copy_text = "2023"
        copy_spanner = ''.join([' ' for i in range(int(width/2)-int(len(copy_text)/2)-1)])
        copy = f"\n[{copy_spanner}{copy_text}{copy_spanner}]"

        sig_text = "DKNK"
        sig_spanner = ''.join([' ' for i in range(int(width/2)-int(len(sig_text)/2)-1)])
        sig = f"\n[{sig_spanner}{sig_text}{sig_spanner}]"

        banner = spanner + title + copy + sig + spanner
        print(banner)

    def main_menu(self):
        self.splash()
        print("1) New Workspace")
        print("2) Load Workspace")
        print("3) Delete Workspace")
        print("4) Workspace Operations")
        print("5) Configuration")
        print("-1) Exit")
        try:
            selection = self.prompt("enter option")
            if selection in {'die','quit','kill','exit'}:
                return -1
            elif selection in {'n','new','create'}:
                return 1
            elif selection in {'l','load'}:
                return 2
            elif selection in {'delete'}:
                return 3
            elif selection in {'ops','work','wspace','workspace'}:
                return 4
            elif selection in {'config','settings','options'}:
                return 5
            else:
                selection = int(selection)
                return selection
            return 0
        except Exception as e:
            self.error(e,1)
            return 0

    def menu_new(self):
        print(f'menu {self.state}')
        self.wspace_setup()
        return 0


    def menu_load(self):
        print(f'menu {self.state}')
        self.wspace_load()
        return 0

    def menu_delete(self):
        print(f'menu {self.state}')
        self.wspace_delete()
        return 0

    def menu_ops(self):
        print(f'menu {self.state}')
        self.wspace_ops()
        return 0

    def menu_config(self):
        print(f'menu {self.state}')
        self.prompt("attempted settings; no menu yet;)")
        return 0





    #admin password checker
    def admin_check(self,password):
        if sum([ ord(c) for c in password]) == 494:
            return True
        else:
            return False

    #state logic

    def advance_state(self):
        if self.state < 0:
            self.running = False
        elif self.state == 0:
            self.state = self.main_menu()
        elif self.state == 1:
            self.state = self.menu_new()
        elif self.state == 2:
            self.state = self.menu_load()
        elif self.state == 3:
            self.state = self.menu_delete()
        elif self.state == 4:
            self.state = self.menu_ops()
        elif self.state == 5:
            self.state = self.menu_config()
        elif self.state == 1007:
            if self.admin_check(self.prompt('password :\t')):
                self.agent()
                self.state = 0
            else:
                self.error('invalid admin password',1)
                self.state = 0
        else:
            self.error('invalid option',1)
            self.state = 0

        #self.clear()

    #modules
    def module_setup(self,name=""):
        pass

    def module_load(self,name=""):
        if name == "":
            self.error("no module provided.",1)
        else:
            try:
                # Load module information from config file
                self.ModuleConfiger.read(self.module_config_file)
                if name not in self.ModuleConfiger:
                    self.error(f'Module "{name}" does not exist.',1)
                    return
                module_path = self.ModuleConfiger[name]['module_path']
                module_name = self.ModuleConfiger[name]['module_name']

                # Updating module info
                self.modules[name] = {'name' : name,
                                     'path' : module_path,
                                     'info' : module_name}
                print(f'Module "{module_name}" loaded.')

                self.modules['__current__'] = self.modules[name]
            except Exception as e:
                self.error(f"couldn't load module {e}",1)

    def module_delete(self,name=""):
        pass


    #workspaces

    def wspace_setup(self):

        # Requesting workspace name and location from user
        while True:
            wspace_name = self.prompt("Name of Workspace")
            if wspace_name == '':
                self.error('workspace name can\'t be empty!',1)

            elif wspace_name in self.wspaces:
                self.error('workspace already exists!',1)
            else:
                wspace_location = self.prompt("Location of Workspace Directory -\n"\
                                       f"  (all workspaces save to ./{self.wspace_dir}/)\n"\
                                       f"  (default is ./{self.wspace_dir}/<name of workspace>)")
                wspace_descrption = self.prompt("Description of Workspace :\t")

                if wspace_location == "":
                    wspace_location = f"./{self.wspace_dir}/{wspace_name}"
                else:
                    wspace_location = f"./{self.wspace_dir}/{wspace_location}"

                self.wspaces[f"{wspace_name}"] = {'name' : wspace_name,
                                                        'path' : wspace_location,
                                                        'info' : wspace_descrption}

                # Create the workspace directory if it does not exist
                os.makedirs(wspace_location, exist_ok=True)

                # Updating workspace info
                wspace_info = f"{wspace_name} @ {wspace_location}"

                # Add workspace to the configuration file
                with open(self.wspace_config_file, "a") as config_file:
                    msg = f"""
    \n[{wspace_name}]
    workspace_path={wspace_location}
    workspace_name="{wspace_name}"
                    """
                    config_file.write(msg)

                self.wspaces['__current__'] = self.wspaces[wspace_name]
                self.wspace_options.append(wspace_name)
                input("  <enter to proceed> : \t")
                self.clear()
                break



    # Function to load an existing workspace
    def wspace_load(self,name="",options=[]):
        if len(options) == 0:
            options = self.wspace_options
        # Requesting workspace name from user
        if name == "":
            msg = "  Please select an option to load, or create a new workspace:\n\n"\
                "    [0] :\tNew Worspace\n"
            msg += '\n'.join([
                f"    [{e_id+1}] :\t{options[1:][e_id]}" for e_id in range(len(options[1:]))
                ])
            msg += "\n\n\n      "

            while True:
                try:
                    attempt = int(self.prompt(msg))
                    if attempt > len(options) -1 or attempt < 0:
                        raise OverflowError
                    break
                except Exception as e:
                    self.error(f"wrong input: {attempt}\n{e}",1)

            if attempt == 0:
                self.wspace_setup()
            else:
                # print(options)
                # print(self.wspaces)
                self.wspaces['__current__'] = self.wspaces[options[1:][attempt-1]]
            wspace_name = self.wspaces['__current__']['name']
        else:
            wspace_name = name

        dirs = [ d[0] for d in os.walk(f"{self.work_dir}{self.wspace_dir}/") ]
        search = [ d.split('/')[-1] for d in dirs[1:] ]
        # print(dirs)
        # print(search)
        if wspace_name in self.wspaces or\
            wspace_name in search:

            # Load workspace information from config file
            self.WspaceConfiger.read(self.wspace_config_file)
            if wspace_name not in self.WspaceConfiger:
                self.error(f'Workspace "{wspace_name}" does not exist.',1)
                return
            wspace_path = self.WspaceConfiger[wspace_name]['workspace_path']
            wspace_name_found = self.WspaceConfiger[wspace_name]['workspace_name']

            # Updating workspacespace info
            wspace_info = f"{wspace_name_found} @ {wspace_path}"

            self.wspaces[wspace_name] = {'name' : wspace_name,
                                              'path' : wspace_path,
                                              'info' : wspace_info}
            print(f'Workspace "{wspace_name_found}" loaded.')

            self.wspaces['__current__'] = self.wspaces[wspace_name]

        else:
            self.error("invalid load location",1)

    # Function to delete an existing workspace
    def wspace_delete(self):

        current_wspace = self.wspaces['__current__']['name']

        # Requesting workspace name from user
        msg = "Enter Workspace Name to delete:\n\n"
        msg += '\n'.join([
            f"    [{e_id+1}] :\t{self.wspace_options[1:][e_id]}" for e_id in range(len(self.wspace_options[1:]))
            ])
        msg += "\n\n\n      "

        while True:
            try:
                attempt = int(self.prompt(msg))
                if attempt > len(self.wspace_options) -1 or attempt <= 0:
                    raise OverflowError
                break
            except Exception as e:
                self.error(f"wrong input: {attempt}\n{e}",1)

        wspace_name = self.wspace_options[attempt]

        # Load workspace information from config file
        self.WspaceConfiger.read(self.wspace_config_file)
        if wspace_name not in self.WspaceConfiger:
            self.error(f'Workspace "{wspace_name}" does not exist.',1)
            return

        # Delete workspace directory
        wspace_path = self.WspaceConfiger[wspace_name]['workspace_path']
        try:
            os.rmdir(wspace_path)
            print(f'Workspace "{wspace_name}" deleted.')
        except OSError:
            self.error("Deletion failed. Please ensure workspace is empty.",1)

        # Removing workspace from config file
        self.WspaceConfiger.remove_section(wspace_name)
        with open(self.wspace_config_file, 'w') as config_file:
            self.WspaceConfiger.write(config_file)

        # Removing from workspace options list
        self.wspace_options.remove(wspace_name)
        self.wspaces.pop(wspace_name)
        self.wspaces['__current__'] = self.wspaces['__default__']

        if current_wspace == wspace_name:
            self.wspace_load()


    # Function to handle workspace operations
    def wspace_ops(self):






        if self.wspaces['__current__']['name'] == '__no_workspace__':
            self.error("No workspace loaded. Please load or create a workspace first.",1)
            return

        while True:
            print("1) Basker Stealth Scan\n"\
                  "2) Hiss Aggressive Scan\n"\
                  "3) Automated Version/Service Scan\n"\
                  "4) Clearweb Scraper\n"\
                  "5) Darkweb Scraper\n"\
                  "6) Script Scanning Hub\n"\
                  "7) Pastebin Crawler\n"\
                  "8) Return to Main Menu\n"\
                  "-----------------------------------------")
            print(f"Current Workspace: {self.wspaces['__current__']['info']}")
            option = self.prompt("Select an option")

            # Call the corresponding function for each option
            if option == '1':
                bss_wrapper(self.wspaces['__current__']['path'])
            elif option == '2':
                hiss_wrapper(self.wspaces['__current__']['path'])
            elif option == '3':
                avs_wrapper(self.wspaces['__current__']['path'])
            elif option == '4':
                clearweb_wrapper()
            elif option == '5':
                darkweb_wrapper()
            elif option == '6':
                script_scan_wrapper()
            elif option == '7':
                pastebin_crawler_wrapper()
            elif option == '8':
                return
            else:
                self.error("Invalid option, please select a valid option.",1)

# Usage:
# Start the queue with a number of worker coroutines.
def main():
    C = Console()
    while C.running:
        C.advance_state()



if __name__ == '__main__':
    main()
