#!/usr/bin/env python3
# https://github.com/empty-circle/empty-circle.git
# The Empty Circle Reconnaissance Framework - 2023


# Wrapper function for Basker Stealth Scan
def bss_wrapper(path):
    basker_tgt=input("Enter target in CIDR notation:")
    basker_output=input("Enter output file name:")
    call_process(f"sudo sh ec_basker.sh -t {basker_tgt} -o ./{path}/{basker_output}")
