#!/bin/bash
# The Empty Circle Reconnaissance Framework - 2023
# v 1.0
# Developed by David Kuszmar
# The Empty Circle is a recon framework for pentesters and
# redteamers. It is meant to be simple, easy to use, and easy
# to modify. Check the readme for exact instructions and a
# walkthrough.

# Define workspace variable
workspace_info="No workspace set"

# Define global variables
workspace_name=""
workspace_location=""

# Path to the configuration file
config_file="config.ecf"

# Check if the configuration file exists
if [[ ! -f $config_file ]]; then
  # Create the file if it doesn't exist
  touch $config_file

  # Get the directory of the script
  framework_path=$(dirname "$(readlink -f "$0")")

  # Write the initial configuration to the file
  echo "framework_path=$framework_path" > $config_file
fi

# Define banner
function banner() {
  clear
  echo "========================================="
  echo "           THE EMPTY CIRCLE"
  echo "                  2023"
  echo "           by David Kuszmar"
  echo "========================================="
}

# Define menu
function main_menu() {
  echo "1) New Workspace"
  echo "2) Load Workspace"
  echo "3) Workspace Operations"
  echo "4) Exit"
}

function workspace_setup() {
  # Ask for name of workspace
  echo "Name of Workspace:"
  read workspace_name

  # Ask for location of workspace directory - default is workspace/
  echo "Location of Workspace Directory (Press enter for default: workspace/):"
  read workspace_location

  # If the user didn't enter anything, use the default location
  if [[ -z $workspace_location ]]; then
    workspace_location="workspace/"
  fi


  # Check if workspace directory exists, if not, create it
  if [ ! -d "$workspace_location" ]; then
    mkdir -p "$workspace_location"
  fi

  # Update workspace_info
  workspace_info="$workspace_name"

  # Add workspace to the configuration file
  echo -e "\n# New Workspace" >> config.ecf
  echo "workspace=\"${workspace_name}=${workspace_location}\"" >> config.ecf

  while true; do
    workspace_menu
    read -p "Select an option: " workspace_option
    case $workspace_option in
      1)
        echo "Enter target range in CIDR notation:"
        read target_range
        echo "Enter output file:"
        read output_file
        basker_stealth_scan -t $target_range -o $output_file
        ;;
        2)
        hiss_aggressive_scan
        ;;
      3)
        automated_svsc_scan
        ;;
      4)
        clearweb_scraper
        ;;
      5)
        darkweb_scraper
        ;;
      6)
        script_scan_hub
        ;;
      7)
        pastebin_crawler
        ;;
      8)
        break # Will break the workspace_menu loop, back to main menu
        ;;
      *)
        echo "Invalid option, please select a valid option."
        ;;
    esac
    # Pause before looping again
    read -n1 -r -p "Press any key to continue..."
  done
}


function workspace_load() {
  # Ask for name of workspace
  echo "Enter Workspace Name to load:"
  read workspace_name

  # Search for the workspace in the config file
  workspace_entry=$(grep "workspace=\"${workspace_name}=" $config_file)

  # If the workspace was not found, notify the user and return
  if [ -z "$workspace_entry" ]; then
    echo "Workspace \"$workspace_name\" does not exist."
    return
  fi

  # If workspace found, load it into the workspace_info
  workspace_info="$workspace_entry"

  echo "Workspace \"$workspace_name\" loaded."
}

# Define sub_menu
function workspace_menu() {
  clear
  echo "1) Basker Stealth Scan"
  echo "2) Hiss Aggressive Scan"
  echo "3) Automated Version/Service Scan"
  echo "4) Clearweb Scraper"
  echo "5) Darkweb Scraper"
  echo "6) Script Scanning Hub"
  echo "7) Pastebin Crawler"
  echo "8) Return to Main Menu"
  echo "-----------------------------------------"
  echo "Current Workspace: $workspace_info"
}

function generate_random_mac() {
  local oui_list=("00:0C:29" "00:50:56" "00:1C:42" "00:1D:0F" "00:1E:68" "00:1F:29" "00:21:5A" "00:25:B5" "00:26:5E" "00:50:43")
  local oui=${oui_list[$((RANDOM % ${#oui_list[@]}))]}
  local nic=$(openssl rand -hex 3 | sed 's/\(..\)/\1:/g; s/.$//')
  echo "$oui:$nic"
}

function generate_random_dns_servers() {
  local dns_servers=("208.67.222.222" "208.67.220.220" "8.8.8.8" "8.8.4.4" "9.9.9.9" "149.112.112.112" "1.1.1.1" "1.0.0.1" "64.6.64.6" "64.6.65.6")
  local random_dns_servers=($(shuf -e "${dns_servers[@]}"))
  local random_dns_servers_list=$(IFS=,; echo "${random_dns_servers[*]}")
  echo "$random_dns_servers_list"
}

function lizard_eye(){
  output_file="$1"
  declare -A open_ips_files

  open_ports=(21 22 23 80 110 125 443 3306 5060 8080)

  for port in "${open_ports[@]}"; do
    open_ips_files["$port"]="open_ips_port_$port.txt"
    touch "${workspace_location}${open_ips_files["$port"]}"
  done

  while read -r line; do
    if [[ $line =~ ^Host:\ (.+)[[:space:]]\(\)[[:space:]]Ports:\ (.+) ]]; then
      ip=${BASH_REMATCH[1]}
      ports=${BASH_REMATCH[2]}
        for port in "${open_ports[@]}"; do
          if [[ $ports =~ $port/open ]]; then
            echo "$ip" >> "${workspace_location}${open_ips_files["$port"]}"
          fi
        done
    fi
  done < "$output_file"
}

function basker_stealth_scan() {
    verbose=0
    fragment=0

    # Load a MAC address for spoofing
    mac=$(generate_random_mac)

    # Load a list of random DNS servers
    random_dns_servers=$(generate_random_dns_servers)

    # Build nmap command
    nmap_command="nmap -sS -Pn --source-port 53 --randomize-hosts -p21,22,23,25,53,80,110,113,143,443,1723,3389,8080 -T2 --max-retries 2 --spoof-mac $mac --dns-servers $random_dns_servers --data-length 731 -D 190.173.78.36,186.18.16.7,ME,190.175.27.84 $target_range -oG $workspace_location/$output_file"

    # Check if verbosity or frag are requested
    if [ "$verbose" -eq 1 ]; then
        nmap_command="$nmap_command -v"
    fi

    if [ "$fragment" -eq 1 ]; then
        nmap_command="$nmap_command -f"
    fi

    # Initiate scan
    eval $nmap_command

    echo "Completed phase one. Your output location: $workspace_location/$output_file"

    # Call lizard eye
    lizard_eye "$workspace_location/$output_file"

    echo "Completed phase two. Sorted lists created."
}

function hiss_aggressive_scan() {
  read -p "Enter the target range: " tgtrange
  read -p "Enter the output file: " output

  mac=$(generate_random_mac)
  random_dns_servers=$(generate_random_dns_servers)

  nmap_command="nmap -n -PE -PP -PS21,22,23,25,80,113,443,31339 -PA80,113,443,10042 -PU40125,161 --source-port 53 --randomize-hosts -T4 --spoof-mac $mac --dns-servers $random_dns_servers --data-length 731 -D 190.173.78.36,186.18.16.7,ME,190.175.27.84 $tgtrange -oG $workspace_location/$output"

  eval $nmap_command

  lizard_eye "$workspace_location/$output"

  echo "Completed. Sorted lists created. Check your output location: $workspace_location/$output"
}

function automated_svsc_scan() {
  declare -A open_ips_files
  open_ports=(21 22 23 80 110 125 443 3306 5060 8080)

  for port in "${open_ports[@]}"; do
    open_ips_files["$port"]="$workspace_location/open_ips_port_$port.txt"
  done

  read -p "Select output file:" output_file

  echo "Select a file to use for the scan:"
  select file in "${open_ips_files[@]}"; do
    # Skip file selection if file size is zero
    if [[ -s $file ]]; then
      target_file=$file
      break
    else
      echo "File $file is empty, skipping..."
    fi
  done

  read -p "Enter the version intensity (0-9): " intensity
  if [[ $intensity -ge 0 ]] && [[ $intensity -le 9 ]]; then
    nmap_command="nmap -sV -sC --version-intensity $intensity -iL $workspace_location/$target_file -oG $workspace_location/$output_file"
    eval $nmap_command
  else
    echo "Invalid intensity level. Please enter a value between 0 and 9."
  fi
}

function clearweb_scraper() {
  read -p "Enter the target URL: " target_url
  read -p "Enter target keywords, separated by comma: " target_keywords

  # Replace comma with space
  target_keywords=${target_keywords//,/ }

  python3 scrappy_pup.py "$target_url" $target_keywords
}

function darkweb_scraper() {
  read -p "Enter the target URL: " target_url
  read -p "Enter target keywords, separated by comma: " target_keywords

  # Replace comma with space
  target_keywords=${target_keywords//,/ }
  python3 scrappy_badger.py -u "$target_url" -k "$target_keywords"
}

function script_scan_hub() {
  # Func to check for valid IP
  function is_valid_ip {
      local ip=$1
      local stat=1
      if [[ $ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
          OIFS=$IFS
          IFS='.'
          ip=($ip)
          IFS=$OIFS
          [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
          stat=$?
      fi
      return $stat
  }

  # Func check hostname
  function is_valid_hostname {
      local host=$1
      if [[ $host =~ ^[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$ ]]; then
          return 0
      else
          return 1
      fi
  }

  # Base NMAP scan
  function run_scan {
      local scan_type=$1
      local aggressive=$2
      local script_name

      if [[ $aggressive == 1 ]]; then
        script_name="intrusive"
      else
        script_name="safe"
      fi

      nmap -Pn --source-port 80 --script="$script_name" "$tgt" -oG "$workspace_location/$outfile"
  }

  echo "Welcome to the script scanning hub"
  read -p "Enter the target IP or hostname: " tgt

  # Validate target input
  if ! is_valid_ip "$tgt" && ! is_valid_hostname "$tgt"; then
      echo "Invalid target input"
      return 1
  fi

  read -p "Enter output file name (leave blank for no output file): " outfile

  # Validate output file name input
  if [[ -n $outfile && ! -w $(dirname "$outfile") ]]; then
      echo "Invalid output file name"
      return 1
  fi

  scan_types=("http" "mssql" "pop3" "smb" "ftp" "sip" "ssh" "ajp")
  selection_index=1

  echo "Select a scan to run:"
  for scan_type in "${scan_types[@]}"; do
      echo "$selection_index) FULL ${scan_type} script scan (Safe)"
      echo "$((selection_index + 1))) FULL ${scan_type} script scan (Aggressive)"
      selection_index=$((selection_index + 2))
  done

  read -p "Enter selection: " selection

  if [[ $selection -lt 1 || $selection -gt $((selection_index - 1)) ]]; then
      echo "Invalid selection"
      return 1
  fi

  scan_index=$(((selection - 1) / 2))
  aggressive=$((selection % 2))

  run_scan "${scan_types[$scan_index]}" "$aggressive"
}

function pastebin_crawler() {
  read -p "Enter target keywords, separated by comma: " pastebin_keywords

  pastebin_keywords=${pastebin_keywords//,/ }
  python3 pastebin_scraper.py -k "$pastebin_keywords"
}

# Define main loop
while true; do
  banner
  main_menu
  read -p "Select an option: " option

  case $option in
    1)
      workspace_setup
      ;;
    2)
      workspace_load
      ;;
    3)
      workspace_menu
      read -p "Select an option: " workspace_option
      case $workspace_option in
        1)
          echo "Enter target range in CIDR notation:"
          read target_range
          echo "Enter output file:"
          read output_file
          basker_stealth_scan -t $target_range -o $output_file
          ;;
        2)
          hiss_aggressive_scan
          ;;
        3)
          automated_svsc_scan
          ;;
        4)
          clearweb_scraper
          ;;
        5)
          darkweb_scraper
          ;;
        6)
          script_scan_hub
          ;;
        7)
          pastebin_crawler
          ;;
        8)
          ;;
        *)
          echo "Invalid option, please select a valid option."
          ;;
      esac
      ;;
    4)
      echo "Exiting..."
      exit 0
      ;;
    *)
      echo "Invalid option, please select a valid option."
      ;;
  esac

  # Pause before looping again
  read -n1 -r -p "Press any key to continue..."
done
