#!/usr/bin/env python3
# https://github.com/empty-circle/empty-circle.git
# The Empty Circle Reconnaissance Framework - 2023


# Wrapper function for Hiss Aggressive Scan
def hiss_wrapper(path):
    hiss_tgt=input("Enter target in CIDR notation:")
    hiss_output=input("Enter output file name:")
    call_process(f"sudo sh ec_hiss.sh -t {hiss_tgt} -o ./{path}/{hiss_output}")
