#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
filetree.py - File tree structure management module

This module provides functionality to create and manage file tree structures.
"""

import os
import sys
import fnmatch
from utils import should_ignore_path, load_gitignore_patterns

class Node:
    """
    Classes that represent nodes in a file tree

    Represents a file or directory, which, if a directory, can have child nodes.
    """
    def __init__(self, name, is_dir, parent=None):
        self.name = name
        self.is_dir = is_dir
        self.children = {} if is_dir else None
        self.parent = parent
        self.selected = True
        self.expanded = True

    @property
    def path(self):
        if self.parent is None:
            return self.name
        parent_path = self.parent.path
        if parent_path.endswith(os.sep):
            return parent_path + self.name
        return parent_path + os.sep + self.name

def build_file_tree(root_path):
    """
    Constructs a tree representing the file structure.

    Args:
        root_path (str): Path to the root directory.

    Returns:
        Node: the root node of the file tree.
    """
    default_patterns = ['.git', '__pycache__', '*.pyc', '.DS_Store', '.idea', '.vscode']
    gitignore_patterns = load_gitignore_patterns(root_path)
    all_patterns = default_patterns + gitignore_patterns

    def should_ignore(path):
        # Pass the root_path to enable correct relative path matching
        return should_ignore_path(path, all_patterns, root_dir=root_path)

    root_name = os.path.basename(root_path.rstrip(os.sep)) or root_path
    root_node = Node(root_name, True)

    # Use a more robust single-pass approach with os.walk
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=True):
        # Prune ignored directories in-place so os.walk doesn't descend into them
        dirnames[:] = [d for d in dirnames if not should_ignore(os.path.join(dirpath, d))]

        # Find the parent node in our tree to attach children to
        rel_dirpath = os.path.relpath(dirpath, root_path)
        parent_node = root_node
        if rel_dirpath != '.':
            for part in rel_dirpath.split(os.sep):
                parent_node = parent_node.children.get(part)
                if not parent_node:
                    break

        if not parent_node:
            continue

        for dirname in dirnames:
            if dirname not in parent_node.children:
                parent_node.children[dirname] = Node(dirname, True, parent_node)

        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if not should_ignore(full_path):
                if filename not in parent_node.children:
                    parent_node.children[filename] = Node(filename, False, parent_node)

    return root_node

def flatten_tree(node, visible_only=True):
    """
    Flattens the tree into a list of nodes for navigation.
    """
    flat_nodes = []

    def _traverse(node, level=0):
        if node.parent is not None:
            flat_nodes.append((node, level))

        if node.is_dir and node.children and (not visible_only or node.expanded):
            items = sorted(node.children.items(), key=lambda x: (not x[1].is_dir, x[0].lower()))
            for _, child in items:
                next_level = 0 if node.parent is None else level + 1
                _traverse(child, next_level)

    _traverse(node)
    return flat_nodes

def count_selected_files(node):
    """
    Count the number of selected files (excluding directories).
    """
    count = 0
    if not node.is_dir and node.selected:
        count = 1
    elif node.is_dir and node.children:
        for child in node.children.values():
            count += count_selected_files(child)
    return count

def collect_selected_content(node, root_path):
    """
    Gather the contents of the selected files.
    """
    results = []

    if not node.is_dir and node.selected:
        file_path = node.path
        if node.parent and node.parent.parent is None:
            full_path = os.path.join(root_path, node.name)
        else:
            rel_path = file_path
            if file_path.startswith(os.path.basename(root_path) + os.sep):
                rel_path = file_path[len(os.path.basename(root_path) + os.sep):]
            full_path = os.path.join(root_path, rel_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            results.append((file_path, content))
        except Exception:
            # Silently ignore files that can't be read (e.g., binary files)
            pass
    elif node.is_dir and node.children:
        for child in node.children.values():
            results.extend(collect_selected_content(child, root_path))

    return results

def collect_all_content(node, root_path):
    """
    Collect the contents of all files (for analysis).
    """
    results = []

    if not node.is_dir:
        file_path = node.path
        if node.parent and node.parent.parent is None:
            full_path = os.path.join(root_path, node.name)
        else:
            rel_path = file_path
            if file_path.startswith(os.path.basename(root_path) + os.sep):
                rel_path = file_path[len(os.path.basename(root_path) + os.sep):]
            full_path = os.path.join(root_path, rel_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            results.append((file_path, content))
        except Exception:
            pass
    elif node.is_dir and node.children:
        for child in node.children.values():
            results.extend(collect_all_content(child, root_path))

    return results