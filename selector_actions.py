#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selector_actions.py - File selection actions module

A module that provides file selection, expansion, and search functionality.
"""

import re
from filetree import flatten_tree

def toggle_selection(node):
    """
    Toggles the selection state of the node, and if it is a directory, the selection state of its children.
    
    Args:
        node (Node): The node to toggle
    """
    node.selected = not node.selected

    if node.is_dir and node.children:
        for child in node.children.values():
            child.selected = node.selected
            if child.is_dir:
                toggle_selection(child)

def toggle_expand(node, search_mode=False, search_query=None, original_nodes=None, apply_search_filter_func=None):
    """
    Expand or collapse a directory.
    
    Args:
        node (Node): The node to expand or collapse
        search_mode (bool): Whether search mode is active
        search_query (str): The current search query
        original_nodes (list): Original list of nodes before search
        apply_search_filter_func (callable): Function to apply search filter
        
    Returns:
        list: Updated list of visible nodes
    """
    if node.is_dir:
        node.expanded = not node.expanded
        # 검색 모드가 아닐 때만 보이는 노드 목록 업데이트
        if not search_mode and not search_query:
            return flatten_tree(node.parent if node.parent else node)
        elif search_query and apply_search_filter_func:
            # 검색이 활성화된 경우 필터링을 다시 적용
            apply_search_filter_func()
    return None

def select_all(root_node, select=True):
    """
    Select or deselect all nodes.
    
    Args:
        root_node (Node): The root node
        select (bool): Whether to select or deselect
    """
    def _select_recursive(node):
        """
        Recursively sets the selected state of a node and its children.
        
        Args:
            node (Node): The node to set.
        """
        node.selected = select
        if node.is_dir and node.children:
            for child in node.children.values():
                _select_recursive(child)

    _select_recursive(root_node)

def expand_all(root_node, expand=True):
    """
    Expand or collapse all directories.
    
    Args:
        root_node (Node): The root node
        expand (bool): Whether to expand or collapse
        
    Returns:
        list: Updated list of visible nodes
    """
    def _set_expanded(node, expand):
        """
        Sets the expanded state of the node and its children.
        
        Args:
            node (Node): The node to set
            expand (bool): Whether to expand
        """
        if node.is_dir and node.children:
            node.expanded = expand
            for child in node.children.values():
                _set_expanded(child, expand)

    _set_expanded(root_node, expand)
    return flatten_tree(root_node)

def apply_search_filter(search_queries: list[str], case_sensitive: bool, root_node, original_nodes: list, visible_nodes_out: list):
    """
    Filter files based on a list of search queries.
    
    Args:
        search_queries (list[str]): The list of search queries.
        case_sensitive (bool): Whether the search is case sensitive.
        root_node (Node): The root node of the file tree.
        original_nodes (list): The original list of nodes to restore if search is cleared or invalid.
        visible_nodes_out (list): Output parameter for the filtered list of (Node, level) tuples.
        
    Returns:
        tuple: (success, error_message)
               success (bool): True if the filter was applied successfully or cleared, False otherwise.
               error_message (str): An error message if success is False, otherwise an empty string.
    """
    if not search_queries or all(not query or query.isspace() for query in search_queries):
        visible_nodes_out[:] = original_nodes
        return True, ""

    compiled_patterns = []
    flags = 0 if case_sensitive else re.IGNORECASE

    for query in search_queries:
        if query and not query.isspace():
            try:
                compiled_patterns.append(re.compile(query, flags))
            except re.error:
                return False, "잘못된 정규식" # Invalid regular expression

    if not compiled_patterns: # All queries were empty or whitespace
        visible_nodes_out[:] = original_nodes
        return True, ""

    all_nodes = flatten_tree(root_node) # This gives a list of (Node, level) tuples

    matching_file_nodes = []
    for node, level in all_nodes:
        if not node.is_dir: # Only match against file names
            for pattern in compiled_patterns:
                if pattern.search(node.name):
                    matching_file_nodes.append(node)
                    break # OR condition: if one pattern matches, it's a match

    if not matching_file_nodes:
        visible_nodes_out[:] = [] # Empty list as per requirement
        return False, "검색 결과 없음" # No search results
        
    visible_nodes_set = set(matching_file_nodes)
    for node in matching_file_nodes:
        parent = node.parent
        while parent:
            visible_nodes_set.add(parent)
            parent = parent.parent

    # Preserve original tree order and structure for visible nodes
    # all_nodes is already in the correct order
    filtered_visible_nodes = []
    for node, level in all_nodes:
        if node in visible_nodes_set:
            filtered_visible_nodes.append((node, level))
            # Ensure parent directories are expanded if they have visible children
            if node.is_dir and node.children and any(child in visible_nodes_set for child in node.children.values()):
                node.expanded = True


    visible_nodes_out[:] = filtered_visible_nodes

    # It's possible that root_node itself is not in visible_nodes_set (e.g. if it's a dir and has no matching children)
    # However, the prompt implies that original tree structure should be preserved for *these* visible nodes.
    # If visible_nodes_out is not empty, and root_node is an ancestor of some node in visible_nodes_out,
    # it should be included. The current logic with visible_nodes_set and iterating all_nodes should handle this.
    # The old check `if not any(node[0] == root_node for node in visible_nodes_out):` might be too aggressive
    # if the root itself doesn't match and has no direct matching children but is an ancestor.
    # The current construction of `filtered_visible_nodes` should correctly include the root if it's part of the path to a visible node.

    return True, ""

def toggle_current_dir_selection(current_node):
    """
    Toggles the selection status of only files in the current directory (no subdirectories).
    
    Args:
        current_node (Node): The current node
    """
    # 현재 노드가 디렉토리인 경우, 그 직계 자식들만 선택 상태 전환
    if current_node.is_dir and current_node.children:
        # 자식들의 대부분이 선택되었는지 확인하여 동작 결정
        selected_count = sum(1 for child in current_node.children.values() if child.selected)
        select_all = selected_count <= len(current_node.children) / 2

        # 모든 직계 자식들을 새 선택 상태로 설정
        for child in current_node.children.values():
            child.selected = select_all
    # 현재 노드가 파일인 경우, 그 선택 상태만 전환
    else:
        current_node.selected = not current_node.selected