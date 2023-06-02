#!/bin/bash
# empty_circle - 2023
# python3 framework version of scan_hub

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

    nmap -Pn --source-port 80 --script="$script_name" "$tgt" -oG "$outfile"
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
