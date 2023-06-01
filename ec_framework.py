#!/usr/bin/env python3
# https://github.com/empty-circle/empty-circle.git
# The Empty Circle Reconnaissance Framework - 2023
# v 0.3

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

# Import Local Files
from wrappers import *

class Console:

    def __init__(self):
         self.state = 0
         self.running = True

         self.config_file = "config"
         self.Configer = configparser.ConfigParser()

         self.workspaces = dict()

         self.startup()



    def startup(self):
        # put startup events here
        self.clear()


        self.workspaces['_default'] = {'name' : "__no_workspace__",
                                       'path' : "./",
                                       'info' : "No Workspace Set" }
        self.workspaces['_current'] = dict(self.workspaces['_default'])


        #load existing workspaces off disk
        #loads into self.worskspaces['<name>']
        dirs = [ d[0] for d in os.walk('./')][1:]
        for ws in dirs:
            self.workspace_load(name=ws[2:])

        ws_options = [ n for n in [ e for e in self.workspaces ][2:] ]

        msg = "  Please select an option to load, or create a new workspace:\n\n"\
              "    [0] : New Worspace\n"
        msg += '\n'.join([
            f"    [{e_id+1}] :\t{ws_options[e_id]}" for e_id in range(len(ws_options))
            ])
        msg += "\n\n\n      "

        while True:
            try:
                attempt = int(self.prompt(msg))
                if attempt > len(ws_options) or attempt < 0:
                    raise OverflowError
                break
            except Exception as e:
                self.error(f"wrong input: {e}",1)

        if attempt == 0:
            self.workspace_setup()
        else:
            self.workspaces['_current'] = self.workspaces[ws_options[attempt-1]]



    #helpers
    def prompt(self,msg):
        tstamp = time.strftime("%a, %H:%M", time.gmtime())
        wspace = self.workspaces['_current']['name']
        return input(f"\n\n  {tstamp}\n  [{wspace}]\n  <{msg}> :\t")

    @staticmethod
    def error(e,cont):
        if cont:
            input(f"error: {e}\n  <enter to proceed> :\t")
            pass
        else:
            input(f"critical error! {e}\n  <exiting> :\t")
            exit()

    @staticmethod
    def clear():
        os.system('clear') # Clears the terminal screen

    #menus
    def splash(self):
        self.clear()
        banner = \
            """
=========================================
            THE EMPTY CIRCLE
                  2023
                  DKNK
=========================================
            """
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
            elif selection in {'ops','work','workspace'}:
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
        self.workspace_setup()
        return 0


    def menu_load(self):
        print(f'menu {self.state}')
        self.workspace_load()
        return 0

    def menu_delete(self):
        print(f'menu {self.state}')
        self.workspace_delete()
        return 0

    def menu_ops(self):
        print(f'menu {self.state}')
        self.workspace_ops()
        return 0

    def menu_config(self):
        print(f'menu {self.state}')
        self.prompt("attempted settings; no menu yet;)")
        return 0


    def menu_secret(self):
        exec(self.prompt("  enter code, agent :\t")) # probably the most stress inducing line of code i've ever written
        input('  <enter to proceed> :\t')
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
                try:
                    self.clear()
                    self.state = self.menu_secret()
                except Exception as e:
                    self.error(e,1)
                    pass
            else:
                self.error('invalid admin password',1)
                self.state = 0
        else:
            self.error('invalid option',1)
            self.state = 0

        #self.clear()

    #workspaces

    def workspace_setup(self):

        # Requesting workspace name and location from user
        while True:
            workspace_name = self.prompt("Name of Workspace")
            if workspace_name in self.workspaces:
                self.error('workspace already exists!',1)
            else:
                workspace_location = self.prompt("Location of Workspace Directory -\n"\
                                        "  (default is empty_circle/workspaces/)")
                workspace_descrption = self.prompt("Description of Workspace :\t")

                self.workspaces[f"{workspace_name}"] = {'name' : workspace_name,
                                                        'path' : workspace_location,
                                                        'info' : workspace_descrption}

                # Create the workspace directory if it does not exist
                os.makedirs(workspace_location, exist_ok=True)

                # Updating workspace info
                workspace_info = f"{workspace_name} @ {workspace_location}"

                # Add workspace to the configuration file
                with open(self.config_file, "a") as config_file:
                    msg = f"""
    \n[{workspace_name}]
    workspace_path={workspace_location}
    workspace_name="{workspace_name}"
                    """
                    config_file.write(msg)

                self.workspaces['_current'] = self.workspaces[workspace_name]

                input("  <enter to proceed> : \t")
                self.clear()
                break



    # Function to load an existing workspace
    def workspace_load(self,name=""):

        # Requesting workspace name from user
        if name == "":
            workspace_name = self.prompt("Enter Workspace Name to load:")
        else:
            workspace_name = name

        dirs = [ d[0] for d in os.walk('./') ]
        if workspace_name in self.workspaces or\
            workspace_name in [ d[2:] for d in dirs[1:] ]:

            # Load workspace information from config file
            self.Configer.read(self.config_file)
            if workspace_name not in self.Configer:
                print(f'Workspace "{workspace_name}" does not exist.')
                return
            workspace_path = self.Configer[workspace_name]['workspace_path']
            workspace_name_found = self.Configer[workspace_name]['workspace_name']

            # Updating workspace info
            workspace_info = f"{workspace_name_found} @ {workspace_path}"

            self.workspaces[workspace_name] = {'name' : workspace_name,
                                              'path' : workspace_path,
                                              'info' : workspace_info}
            print(f'Workspace "{workspace_name_found}" loaded.')

            self.workspaces['_current'] = self.workspaces[workspace_name]

        else:
            self.error("invalid load location",1)

    # Function to delete an existing workspace
    def workspace_delete(self):

        current_workspace = self.workspaces['_current']['name']

        # Requesting workspace name from user
        workspace_name = self.prompt("Enter Workspace Name to delete:")

        # Load workspace information from config file
        self.Configer.read(self.config_file)
        if workspace_name not in self.Configer:
            print(f'Workspace "{workspace_name}" does not exist.')
            return

        # Delete workspace directory
        workspace_path = self.Configer[workspace_name]['workspace_path']
        try:
            os.rmdir(workspace_path)
            print(f'Workspace "{workspace_name}" deleted.')
        except OSError:
            print("Deletion failed. Please ensure workspace is empty.")

        # Removing workspace from config file
        self.Configer.remove_section(workspace_name)
        with open(self.config_file, 'w') as config_file:
            self.Configer.write(config_file)


        if current_workspace == workspace_name:
            self.workspaces['_current'] = dict(self.workspaces['_default'])


    # Function to handle workspace operations
    def workspace_ops(self):
        if self.workspaces['_current']['name'] == '__no_workspace__':
            input("No workspace loaded. Please load or create a workspace first.\n  <enter to proceed> :\t")
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
            print(f"Current Workspace: {self.workspaces['_current']['info']}")
            option = self.prompt("Select an option")

            # Call the corresponding function for each option
            if option == '1':
                bss_wrapper(self.workspaces['_current']['path'])
            elif option == '2':
                hiss_wrapper(self.workspaces['_current']['path'])
            elif option == '3':
                avs_wrapper(self.workspaces['_current']['path'])
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
                print("Invalid option, please select a valid option.")

# Usage:
# Start the queue with a number of worker coroutines.
def main():
    C = Console()
    while C.running:
        C.advance_state()



if __name__ == '__main__':
    main()
