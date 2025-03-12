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
    
    # Combine ignore patterns, with .gitignore patterns taking precedence
    if ignore_patterns is None:
        ignore_patterns = default_patterns + gitignore_patterns
    else:
        ignore_patterns = ignore_patterns + gitignore_patterns

    def should_ignore(path):
        """
        Checks if the given path matches a pattern that should be ignored.

        Args:
            path (str): The path to check.

        Returns:
            bool: True if it should be ignored, False otherwise
        """
        return should_ignore_path(path, ignore_patterns)

    root_name = os.path.basename(root_path.rstrip(os.sep))
    if not root_name:  # 루트 디렉토리 경우
        root_name = root_path

    root_node = Node(root_name, True)
    root_node.full_path = root_path  # 루트 노드에 절대 경로 저장

    def add_path(current_node, path_parts, full_path):
        """
        Adds each part of the path to the tree.
        
        Args:
            current_node (Node): Current node
            path_parts (list): List of path parts
            full_path (str): Full path
        """
        if not path_parts:
            return

        part = path_parts[0]
        remaining = path_parts[1:]

        if should_ignore(os.path.join(full_path, part)):
            return

        # 이미 부분이 존재하는지 확인
        if part in current_node.children:
            child = current_node.children[part]
        else:
            is_dir = os.path.isdir(os.path.join(full_path, part))
            child = Node(part, is_dir, current_node)
            current_node.children[part] = child

        # 남은 부분이 있으면 재귀적으로 계속
        if remaining:
            next_path = os.path.join(full_path, part)
            add_path(child, remaining, next_path)

    # 디렉토리 구조 순회
    for dirpath, dirnames, filenames in os.walk(root_path):
        # 필터링된 디렉토리 건너뛰기
        dirnames[:] = [d for d in dirnames if not should_ignore(os.path.join(dirpath, d))]

        rel_path = os.path.relpath(dirpath, root_path)
        if rel_path == '.':
            # 루트에 있는 파일 추가
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                if filename not in root_node.children and not should_ignore(full_path):
                    file_node = Node(filename, False, root_node)
                    root_node.children[filename] = file_node
        else:
            # 디렉토리 추가
            path_parts = rel_path.split(os.sep)
            add_path(root_node, path_parts, root_path)

            # 이 디렉토리에 있는 파일 추가
            current = root_node
            for part in path_parts:
                if part in current.children:
                    current = current.children[part]
                else:
                    # 디렉토리가 필터링된 경우 건너뛰기
                    break
            else:
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    if not should_ignore(full_path) and filename not in current.children:
                        file_node = Node(filename, False, current)
                        current.children[filename] = file_node

    return root_node

def flatten_tree(node, visible_only=True):
    """
    Flattens the tree into a list of nodes for navigation.
    
    Args:
        node (Node): Root node
        visible_only (bool, optional): Whether to include only visible nodes.
        
    Returns:
        list: a list of (node, level) tuples.
    """
    flat_nodes = []

    def _traverse(node, level=0):
        """
        Traverse the tree and generate a flattened list of nodes.
        
        Args:
            node (Node): The current node
            level (int, optional): Current level
        """
        # 루트 노드는 건너뛰되, 루트의 자식부터는 level 0으로 시작
        if node.parent is not None:  # 루트 노드 건너뛰기
            flat_nodes.append((node, level))

        if node.is_dir and node.children and (not visible_only or node.expanded):
            # 먼저 디렉토리, 그 다음 파일, 알파벳 순으로 정렬
            items = sorted(node.children.items(),
                          key=lambda x: (not x[1].is_dir, x[0].lower()))

            for _, child in items:
                # 루트의 직계 자식들은 level 0, 그 아래부터는 level+1
                next_level = 0 if node.parent is None else level + 1
                _traverse(child, next_level)

    _traverse(node)
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
