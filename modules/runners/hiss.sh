#!/bin/bash
# empty_circle - 2023
# v1.1

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
    output_file=$output_file
    output_dir=$(cut -d '/') #strip file name from path
    declare -A open_ips_files

    open_ports=(21 22 23 80 110 125 443 3306 5060 8080)

    for port in "${open_ports[@]}"; do
        open_ips_files["$port"]="open_ips_port_$port.txt"
        touch "${open_ips_files["$port"]}"
    done

    while read -r line; do
        if [[ $line =~ ^Host:\ (.+)[[:space:]]\(\)[[:space:]]Ports:\ (.+) ]]; then
            ip=${BASH_REMATCH[1]}
            ports=${BASH_REMATCH[2]}

            for port in "${open_ports[@]}"; do
                if [[ $ports =~ $port/open ]]; then
                    echo "$ip" >> "${open_ips_files["$port"]}"
                fi
            done
        fi
    done < "$output_file"
}

function show_usage() {
  echo "Usage: $0 -t <target_range> -o <output_file> [-v|-f]"
  echo ""
  echo "  -t  target range in CIDR notation (required)"
  echo "  -o  output file (required)"
  echo "  -v  use verbose mode"
  echo "  -f  use fragmentation"
  echo ""
  exit 1
}

verbose=0
fragment=0
while getopts "t:o:vf" opt; do
  case $opt in
    t) target_range="$OPTARG"
    ;;
    o) output_file="$OPTARG"
    ;;
    v) verbose=1
    ;;
    f) fragment=1
    ;;
    \?) show_usage
    ;;
  esac
done

if [ -z "$target_range" ] || [ -z "$output_file" ]; then
  show_usage
fi

# Load a MAC address for spoofing
mac=$(generate_random_mac)

# Load a list of random DNS servers
random_dns_servers=$(generate_random_dns_servers)

# Build nmap command
nmap_command="nmap -n -PE -PP -PS21,22,23,25,80,113,443,31339 -PA80,113,443,10042 -PU40125,161 --source-port 53 --randomize-hosts -T4 --spoof-mac $mac --dns-servers $random_dns_servers --data-length 731 -D 190.173.78.36,186.18.16.7,ME,190.175.27.84 $target_range -oG $output_file"

# Initiate scan
eval $nmap_command

echo "Completed phase one. Your output location: $output_file"

# Call lizard eye
lizard_eye

echo "Completed phase two. Sorted lists created."
