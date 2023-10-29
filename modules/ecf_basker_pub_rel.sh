#!/bin/bash
# Basker Reptillian Recon Scanner - David Kuszmar - 2023
# v3.0
# B4sk34 Sc4nn3r is a stealthy recon scanner using the power of nmap.
# It is the 'prime' module of the Empty Circle Framework for pentesters
# and redteams. It should only be used in accordance with applicable permissions
# and laws.

function print_banner() {
local banner="\e[44m\e[97m########################################\e[0m\n"
banner+="\e[44m\e[97m#    B4sk3r Sc4nn3r  -  empty_circle   #\e[0m\n"
banner+="\e[44m\e[97m#        b4sk3r is cold-blooded        #\e[0m\n"
banner+="\e[44m\e[97m#        this could take awhile        #\e[0m\n"
banner+="\e[44m\e[97m########################################\e[0m"
echo -e "${banner}"
}

function generate_random_mac() {
local oui_list=("00:0C:29" "00:50:56" "00:1C:42" "00:1D:0F" "00:1E:68" "00:1F:29" "00:21:5A" "00:25:B5" "00:26:5E" "00:50:43" "00:26:C7" "00:16:3E" "00:28:45" "00:2A:FA" "00:2B:0E")
local oui=${oui_list[$((RANDOM % ${#oui_list[@]}))]}
local nic=$(openssl rand -hex 3 | sed 's/\(..\)/\1:/g; s/.$//')
echo "$oui:$nic"
}

function generate_random_dns_servers() {
local dns_servers=("208.67.222.222" "208.67.220.220" "8.8.8.8" "8.8.4.4" "9.9.9.9" "149.112.112.112" "1.1.1.1" "1.0.0.1" "64.6.64.6" "64.6.65.6" "185.228.168.168" "185.228.169.168" "156.154.70.1" "156.154.71.1" "84.200.69.80" "84.200.70.40")
local random_dns_servers=($(shuf -e "${dns_servers[@]}"))
local random_dns_servers_list=$(IFS=,; echo "${random_dns_servers[*]}")
echo "$random_dns_servers_list"
}

function show_usage() {
echo "Usage: $0 -t <target_range> -c <timing> -p <port_set> -h <host_grouping> -o <output_file>"
echo ""
echo "  -t  target range in CIDR notation (required)"
echo "  -o  output file (required)"
echo "  -c  nmap Timing (required)"
echo "  -p  port set (required: default, plus, all)"
echo "  -h  host grouping (required: stealth, normal, aggressive)"
echo ""
exit 1
}

# Function to shuffle and select 3-7 IPs from a given pool
function shuffle_ips() {
  local pool=("$@")
  local count=$((3 + RANDOM % 5)) # Select random count between 3 and 7
  local selected_ips=$(shuf -e "${pool[@]}" | head -n $count | tr '\n' ' ')
  echo "$selected_ips"
}

#Decoy IPs are currently set to BRICKS nations
turkish_ips=("78.186.191.40" "88.233.44.203" "81.213.142.156" "95.9.128.180")
chinese_ips=("58.19.24.13" "123.125.115.110" "220.181.108.77" "120.92.4.1")
russian_ips=("92.63.64.0" "92.63.64.12" "92.63.64.113" "92.63.65.10")
south_african_ips=("41.13.112.152" "105.4.8.155" "197.83.240.85" "196.38.40.179")
north_korea_ips=("175.45.176.1" "175.45.176.3" "175.45.176.85" "175.45.176.99")
india_ips=("106.51.56.23" "182.76.144.66" "106.51.56.23" "117.195.40.6")

# Shuffle and select IPs from each pool
selected_turkish_ips=$(shuffle_ips "${turkish_ips[@]}")
selected_chinese_ips=$(shuffle_ips "${chinese_ips[@]}")
selected_russian_ips=$(shuffle_ips "${russian_ips[@]}")
selected_south_african_ips=$(shuffle_ips "${south_african_ips[@]}")
selected_north_korea_ips=$(shuffle_ips "${north_korea_ips[@]}")
selected_india_ips=$(shuffle_ips "${india_ips[@]}")

# Convert selected IPs to comma-separated strings
selected_turkish_ips=$(echo "$selected_turkish_ips" | tr ' ' ',')
selected_chinese_ips=$(echo "$selected_chinese_ips" | tr ' ' ',')
selected_russian_ips=$(echo "$selected_russian_ips" | tr ' ' ',')
selected_south_african_ips=$(echo "$selected_south_african_ips" | tr ' ' ',')
selected_north_korea_ips=$(echo "$selected_north_korea_ips" | tr ' ' ',')
selected_india_ips=$(echo "$selected_india_ips" | tr ' ' ',')

combined_ips=""
separator=""

# A list of all the selected IPs for easy looping
all_selected=("$selected_turkish_ips" "$selected_chinese_ips" "$selected_russian_ips" "$selected_south_african_ips" "$selected_north_korea_ips" "$selected_india_ips")

# Loop through and append to the combined_ips string, with appropriate comma separators
for selected in "${all_selected[@]}"; do
  if [[ ! -z "$selected" ]]; then
    combined_ips="${combined_ips:+$combined_ips,}${selected}"
  fi
done

combined_ips=$(echo "$combined_ips" | tr -s ',' | sed 's/^,//' | sed 's/,$//')

# Insert 'ME' randomly
num_elements=$(echo "$combined_ips" | awk -F ',' '{print NF}')
if [ "$num_elements" -eq 0 ]; then
  # If no elements, just set the decoy as ME
  combined_ips_with_me="ME"
else
  position=$((RANDOM % num_elements))
  if [ "$position" -eq 0 ]; then
    combined_ips_with_me="ME,$combined_ips"
  else
    pre_me=$(echo "$combined_ips" | cut -d ',' -f 1-"$position")
    post_me=$(echo "$combined_ips" | cut -d ',' -f $((position + 1))-)
    combined_ips_with_me="${pre_me},ME,${post_me}"
  fi
fi

combined_ips=${combined_ips%,}

if [ -z "$combined_ips" ]; then
  echo "Error: combined_ips is empty. Exiting."
  exit 1
fi

nmap_output=$(nmap -sS -Pn --source-port 53 --randomize-hosts -p$ports -T$c --max-retries 2 --spoof-mac $mac --dns-servers $random_dns_servers --data-length 731 -D $combined_ips_with_me --min-hostgroup $min_host_num --max-hostgroup $max_host_num $target_range -oG $output_file)

if [[ "$nmap_output" == *"Failed to resolve"* ]]; then
  echo "Error in Nmap command."
fi

c=""
port_set=""
ports=""
host_grouping=""
min_host_num=""
max_host_num=""

while getopts "t:c:o:p:h:" opt; do
case $opt in
t) target_range="$OPTARG"
;;
c) c="$OPTARG"
;;
o) output_file="$OPTARG"
;;
p) port_set="$OPTARG"
;;
h) host_grouping="$OPTARG"
;;
\?) show_usage
;;
esac
done

if ! [[ $target_range =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}/[0-9]{1,2}$ ]]; then
  echo "Invalid target range format."
  exit 1
fi

if ! [[ $c -ge 1 && $c -le 5 ]]; then
  echo "Invalid timing value. Must be between 1 and 5."
  exit 1
fi

if ! [[ $port_set == "default" || $port_set == "plus" || $port_set == "all" ]]; then
  echo "Invalid port set. Choose default, plus, or all."
  exit 1
fi

if ! [[ $host_grouping == "stealth" || $host_grouping == "normal" || $host_grouping == "aggressive" ]]; then
  echo "Invalid host grouping. Choose stealth, normal, or aggressive."
  exit 1
fi

touch $output_file 2>/dev/null
if [ $? -ne 0 ]; then
  echo "Invalid output file path or permissions."
  exit 1
fi


if [ -z "$target_range" ] || [ -z "$output_file" ] || [ -z "$c" ] || [ -z "$port_set" ] || [ -z "$host_grouping" ]; then
  show_usage
fi

# Rep it
print_banner

# Load a MAC address for spoofing
mac=$(generate_random_mac)

# Load a list of random DNS servers
random_dns_servers=$(generate_random_dns_servers)

if [[ $port_set == "default" ]]; then
ports=("20,21,22,23,25,53,80,110,143,443,445,690,1723,3306,3389,5060")
elif [[ $port_set == "plus" ]]; then
ports=("18,19,20,21,22,23,25,42,43,53,80,102,110,143,389,443,445,465,631,690,1723,3305,3306,3389,5060,5061")
elif [[ $port_set == "all" ]]; then
ports=("18,19,20,21,22,23,25,42,43,49,53,65,66,67,69,79,80,81,102,104,106,109,110,111,113,115,118,119,126,143,153,156,158,179,194,199,201,209,210,220,300,311,312,350,384,389,401,434,443,445,464,465,530,543,544,564,591,631,636,657,690,692,987,989,990,992,994,1010,1119,1234,1433,1527,1723,1755,2049,2210,2222,2375,2376,2377,2638,2967,3001,3305,3306,3389,3396,3659,4486,4569,3872,5025,5060,5061,5190,5432,6516,6566,6697,8009,8074,8080,8081,8194,8195,8243,8280,9119,9150,9389,9785,11371")
fi

if [[ $host_grouping == "stealth" ]]; then
min_host_num="8"
max_host_num="16"
elif [[ $host_grouping == "normal" ]]; then
min_host_num="64"
max_host_num="128"
elif [[ $host_grouping == "aggressive" ]]; then
min_host_num="256"
max_host_num="512"
fi

# Execute scan
nmap -sS -Pn --source-port 53 --randomize-hosts -p$ports -T$c --max-retries 2 --spoof-mac $mac --dns-servers $random_dns_servers --data-length 731 -D $combined_ips_with_me --min-hostgroup $min_host_num --max-hostgroup $max_host_num $target_range -oG $output_file

echo "Completed scan. Your output location is: $output_file"
