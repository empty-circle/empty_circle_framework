#!/usr/bin/env python3
# https://github.com/empty-circle/empty-circle.git
# The Empty Circle Reconnaissance Framework - 2023
# v 0.2

# Developed by David Kuszmar & Nikita Kotlyarov
# https://github.com/empty-circle
# https://github.com/thenikitakotlyarov

# The Empty Circle is a recon framework for pentesters and
# redteamers. It is meant to be simple, easy to use, and easy
# to modify. Check the readme for exact instructions and a
# walkthrough.

import subprocess
import shlex

# Function to call a process with the given command
def call_process(command):
    subprocess.call(shlex.split(command))

# Wrapper function for Basker Stealth Scan
def bss_wrapper(path):
    basker_tgt=input("Enter target in CIDR notation:")
    basker_output=input("Enter output file name:")
    call_process(f"sudo sh ec_basker.sh -t {basker_tgt} -o ./{path}/{basker_output}")

# Wrapper function for Hiss Aggressive Scan
def hiss_wrapper(path):
    hiss_tgt=input("Enter target in CIDR notation:")
    hiss_output=input("Enter output file name:")
    call_process(f"sudo sh ec_hiss.sh -t {hiss_tgt} -o ./{path}/{hiss_output}")

# Wrapper function for Automated Version/Service Scan
def avs_wrapper(path):
    call_process(f"sudo sh ec_asvsc.sh {path}")

# Wrapper function for Clearweb Scraper
def clearweb_wrapper():
    call_process(f"python3 scrappy_pup.py")

# Wrapper function for Darkweb Scraper
def darkweb_wrapper():
    call_process(f"sudo systemctl status tor")
    call_process(f"sudo python3 scrappy_badger.py")

# Wrapper function for Script Scanning Hub
def script_scan_wrapper():
    call_process(f"sudo sh ec_scanhub.sh")

# Wrapper function for Pastebin Crawler
def pastebin_crawler_wrapper():
    call_process(f"python3 pastebin_scraper.py")
