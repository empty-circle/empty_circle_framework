#!/bin/bash
# Scan Center - David Kuszmar - 2023
# v2.0
# Allows quick, user-friendly access to nmap scripts and safeties for the NSE.

# Validate IPv4 address
is_valid_ip() {
    local ip=$1
    if [[ $ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        IFS='.' read -ra octets <<< "$ip"
        for octet in "${octets[@]}"; do
            [[ $octet -le 255 ]] || return 1
        done
        return 0
    fi
    return 1
}

# Validate hostname
is_valid_hostname() {
    local host=$1
    [[ $host =~ ^[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$ ]]
}

# Execute NMAP scan
run_scan() {
    local scan_type=$1
    local aggressive=$2
    local script_name="$scan_type-*"

    [[ $aggressive -eq 0 ]] && script_name="not intrusive and $script_name"

    nmap -Pn --source-port 80 --script="$script_name" "$tgt" -oG "$outfile"
}

# Main program logic
main() {
    echo "Welcome to the scanning tool"
    read -rp "Enter the target IP or hostname: " tgt

    # Validate target
    if ! is_valid_ip "$tgt" && ! is_valid_hostname "$tgt"; then
        echo "Invalid target"
        exit 1
    fi

    read -rp "Enter output file name (leave blank for no output file): " outfile

    # Validate output file
    if [[ -n $outfile && ! -w $(dirname "$outfile") ]]; then
        echo "Invalid output file"
        exit 1
    fi

    local scan_types=("http" "mssql" "pop3" "smb" "ftp" "sip" "ssh" "ajp")
    local selection_index=1

    echo "Select a scan to run:"
    for scan_type in "${scan_types[@]}"; do
        echo "$selection_index) FULL ${scan_type} script scan (Safe)"
        echo "$((selection_index + 1)) FULL ${scan_type} script scan (Aggressive)"
        selection_index=$((selection_index + 2))
    done

    read -rp "Enter selection: " selection

    if [[ $selection -lt 1 || $selection -gt $((selection_index - 1)) ]]; then
        echo "Invalid selection"
        exit 1
    fi

    local scan_index=$(( (selection - 1) / 2 ))
    local aggressive=$(( selection % 2 ))

    run_scan "${scan_types[$scan_index]}" "$aggressive"
}

# Entry point
main
