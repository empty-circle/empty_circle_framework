#!/bin/bash
# empty_circle - 2023
# Feature_SVSC v 2.0
# This is an ancillary module for the Empty Circle Framework for redteamers and
# pentesters. Its meant to provide some of the functionality built into the basker
# module for the service and version scan features of nmap.

function generate_random_mac() {
local oui_list=("00:0C:29" "00:50:56" "00:1C:42" "00:1D:0F" "00:1E:68" "00:1F:29" "00:21:5A" "00:25:B5" "00:26:5E" "00:50:43" "00:26:C7" "00:27:8C" "00:28:45" "00:2A:FA" "00:2B:0E")
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
echo "Usage: $0 -t <target> -i <intensity_level> -p <port_set> -c <timing_level> -o <output_file>"
echo ""
echo "  -t  target IP (required)"
echo "  -o  output file (required)"
echo "  -i  version intensity level (default: 7)"
echo "  -c  timing level (default: 3)"
echo "  -p  port_set (required)"
echo ""
exit 1
}

port_set="default"
i=7
c=3

while getopts "t:i:c:o:p:" opt; do
case $opt in
t) target="$OPTARG"
;;
o) output_file="$OPTARG"
;;
i) i="$OPTARG"
;;
c) c="$OPTARG"
;;
p) port_set="$OPTARG"
;;
\?) show_usage
;;
esac
done

if [ -z "$target" ] || [ -z "$output_file" ] || [ -z "$c" ] || [ -z "$port_set" ]; then
  show_usage
fi

if [[ $port_set == "default" ]]; then
ports=("20,21,22,23,25,53,80,110,143,389,443,445,690,1723,3306,3389,5060")
elif [[ $port_set == "plus" ]]; then
ports=("18,19,20,21,22,23,25,42,43,53,80,102,110,143,389,443,445,465,631,690,1723,3305,3306,3389,5060,5061")
elif [[ $port_set == "all" ]]; then
ports=("18,19,20,21,22,23,25,42,43,49,53,65,66,67,69,79,80,81,102,104,106,109,110,111,113,115,118,119,126,143,153,156,158,179,194,199,201,209,210,220,300,311,312,350,384,389,401,434,443,445,464,465,530,543,544,564,591,631,636,657,690,692,987,989,990,992,994,1010,1119,1234,1433,1527,1723,1755,2049,2210,2222,2375,2376,2377,2638,2967,3001,3305,3306,3389,3396,3659,4486,4569,3872,5025,5060,5061,5190,5432,6516,6566,6697,8009,8074,8080,8081,8194,8195,8243,8280,9119,9150,9389,9785,11371")
fi

# Load a MAC address for spoofing
mac=$(generate_random_mac)

# Load a list of random DNS servers
random_dns_servers=$(generate_random_dns_servers)

# Build nmap command
nmap_command="nmap -Pn -sV -sC -p$ports -T$c --spoof-mac $mac --dns-servers $random_dns_servers --version-intensity $i $target -oG $output_file"

eval $nmap_command

echo "Check output location."
