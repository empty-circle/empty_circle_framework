#!/usr/bin/env python3
# https://github.com/empty-circle/empty-circle.git
# The Empty Circle Reconnaissance Framework - 2023



# Wrapper function for Automated Version/Service Scan
def avs_wrapper(path):
    call_process(f"sudo sh ec_asvsc.sh {path}")
