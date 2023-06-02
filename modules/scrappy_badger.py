#!/usr/bin/env python3
# https://github.com/empty-circle/empty-circle.git
# The Empty Circle Reconnaissance Framework - 2023


# Wrapper function for Darkweb Scraper
def darkweb_wrapper():
    call_process(f"sudo systemctl status tor")
    call_process(f"sudo python3 scrappy_badger.py")
