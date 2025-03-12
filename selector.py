#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selector.py - File selection UI module

A module that provides a curses-based interactive file selection interface.
"""

import curses
from selector_ui import FileSelector

def interactive_selection(root_node):
    """Launch the interactive file selection interface."""
    return curses.wrapper(lambda stdscr: FileSelector(root_node, stdscr).run())