#!/usr/bin/env python3
# https://github.com/empty-circle/empty-circle.git
# The Empty Circle Reconnaissance Framework - 2023
# v 0.2

import subprocess
import shlex

# Function to call a process with the given command
def call_process(command):
    subprocess.call(shlex.split(command))
