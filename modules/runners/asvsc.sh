#!/bin/bash
# Automated svsc for ec_framework
# empty_circle - 2023

workspace_location=$1

declare -A open_ips_files
open_ports=(21 22 23 80 110 125 443 3306 5060 8080)

for port in "${open_ports[@]}"; do
    open_ips_files["$port"]="${workspace_location}open_ips_port_$port.txt"
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
    nmap_command="nmap -sV -sC --version-intensity $intensity -iL $target_file -oG $workspace_location$output_file"
    eval $nmap_command
else
    echo "Invalid intensity level. Please enter a value between 0 and 9."
fi
