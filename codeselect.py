#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeSelect - Main script

A tool for easily selecting and exporting files to share with the AI assistant.
The file simply serves as an entry point to call the main function of the CLI module.
"""

import sys
from cli import main

if __name__ == "__main__":
    sys.exit(main())