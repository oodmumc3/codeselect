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
        """
        Initialise Node Class

        Args:
            name (str): Name of the node (file/directory name)
            is_dir (bool): Whether it is a directory
            parent (Node, optional): Parent node
        """
        self.name = name
        self.is_dir = is_dir
        self.children = {} if is_dir else None
        self.parent = parent
        self.selected = True  # 기본적으로 선택됨
        self.expanded = True  # 폴더는 기본적으로 확장됨

    @property
    def path(self):
        """
        Returns the full path to the node.

        Returns:
            str: the full path of the node
        """
        if self.parent is None:
            return self.name
        parent_path = self.parent.path
        if parent_path.endswith(os.sep):
            return parent_path + self.name
        return parent_path + os.sep + self.name

def build_file_tree(root_path, ignore_patterns=None):
    """
    Constructs a tree representing the file structure.

    Args:
        root_path (str): Path to the root directory.
        ignore_patterns (list, optional): List of patterns to ignore.

    Returns:
        Node: the root node of the file tree.
    """
    # Default patterns to ignore
    default_patterns = ['.git', '__pycache__', '*.pyc', '.DS_Store', '.idea', '.vscode']

    # Load patterns from .gitignore if it exists
    gitignore_patterns = load_gitignore_patterns(root_path)

    # Combine ignore patterns
    if ignore_patterns is None:
        all_ignore_patterns = default_patterns + gitignore_patterns
    else:
        all_ignore_patterns = ignore_patterns + gitignore_patterns

    def is_ignored(path):
        """Checks if a given path should be ignored."""
        return should_ignore_path(path, all_ignore_patterns)

    root_name = os.path.basename(root_path.rstrip(os.sep))
    if not root_name:  # Handle root directory case like '/'
        root_name = root_path

    root_node = Node(root_name, True)
    root_node.full_path = root_path

    # A map from full directory paths to their corresponding Node objects
    dir_nodes = {root_path: root_node}

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=True):
        # Prune ignored directories from traversal. This is the correct way to use os.walk.
        dirnames[:] = [d for d in dirnames if not is_ignored(os.path.join(dirpath, d))]

        # Get the parent node for the current directory being processed
        parent_node = dir_nodes.get(dirpath)
        if not parent_node:
            continue

        # Add subdirectory nodes to the tree
        for dirname in sorted(dirnames):
            full_dir_path = os.path.join(dirpath, dirname)
            dir_node = Node(dirname, True, parent=parent_node)
            parent_node.children[dirname] = dir_node
            # Add the new directory node to our map so we can find it later
            dir_nodes[full_dir_path] = dir_node

        # Add file nodes to the tree
        for filename in sorted(filenames):
            full_file_path = os.path.join(dirpath, filename)
            if not is_ignored(full_file_path):
                file_node = Node(filename, False, parent=parent_node)
                parent_node.children[filename] = file_node

    return root_node

def flatten_tree(node, visible_only=True):
    """
    Flattens the tree into a list of nodes for navigation.

    Args:
        node (Node): Root node of the subtree to flatten.
        visible_only (bool, optional): Whether to include only visible nodes.

    Returns:
        list: a list of (node, level) tuples.
    """
    flat_nodes = []

    def _traverse(current_node, level):
        """
        Recursively traverse the tree and build a flat list.

        Args:
            current_node (Node): The node to process children of.
            level (int): The level for the children of current_node.
        """
        # We only process children if the directory is expanded
        if not current_node.is_dir or not current_node.children:
            return

        if visible_only and not current_node.expanded:
            return

        items = sorted(current_node.children.items(),
                       key=lambda x: (not x[1].is_dir, x[0].lower()))

        for _, child in items:
            flat_nodes.append((child, level))
            # Recurse for the child's children at the next level
            _traverse(child, level + 1)

    # Start traversal on the root node. Its children will be at level 0.
    _traverse(node, 0)
    return flat_nodes

def count_selected_files(node):
    """
    Count the number of selected files (excluding directories).

    Args:
        node (Node): The root node.

    Returns:
        int: Number of selected files
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

    Args:
        node (Node): Root node
        root_path (str): Root directory path

    Returns:
        list: a list of (file path, content) tuples.
    """
    results = []

    if not node.is_dir and node.selected:
        file_path = node.path

        # 수정: 루트 경로가 중복되지 않도록 보장
        if node.parent and node.parent.parent is None:
            # 노드가 루트 바로 아래에 있으면 파일 이름만 사용
            full_path = os.path.join(root_path, node.name)
        else:
            # 중첩된 파일의 경우 적절한 상대 경로 구성
            rel_path = file_path
            if file_path.startswith(os.path.basename(root_path) + os.sep):
                rel_path = file_path[len(os.path.basename(root_path) + os.sep):]
            full_path = os.path.join(root_path, rel_path)

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            results.append((file_path, content))
        except UnicodeDecodeError:
            print(f"이진 파일 무시: {file_path}")
        except Exception as e:
            print(f"{full_path} 읽기 오류: {e}")
    elif node.is_dir and node.children:
        for child in node.children.values():
            results.extend(collect_selected_content(child, root_path))

    return results

def collect_all_content(node, root_path):
    """
    Collect the contents of all files (for analysis).

    Args:
        node (Node): Root node
        root_path (str): Root directory path

    Returns:
        list: a list of (file path, content) tuples.
    """
    results = []

    if not node.is_dir:
        file_path = node.path

        # 수정: collect_selected_content와 동일한 경로 수정 적용
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
        except UnicodeDecodeError:
            pass  # 이진 파일 조용히 무시
        except Exception:
            pass  # 오류 조용히 무시
    elif node.is_dir and node.children:
        for child in node.children.values():
            results.extend(collect_all_content(child, root_path))

    return results
