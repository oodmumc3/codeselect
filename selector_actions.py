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

def apply_search_filter(search_query, case_sensitive, root_node, original_nodes, visible_nodes_out):
    """
    Filter files based on search terms.
    
    Args:
        search_query (str): The search query
        case_sensitive (bool): Whether the search is case sensitive
        root_node (Node): The root node
        original_nodes (list): The original list of nodes
        visible_nodes_out (list): Output parameter for the filtered nodes
        
    Returns:
        tuple: (success, error_message)
    """
    if not search_query:
        visible_nodes_out[:] = original_nodes
        return True, ""

    try:
        # 정규식 플래그 설정
        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = re.compile(search_query, flags)
        
        # 전체 노드 목록 가져오기
        all_nodes = flatten_tree(root_node)
        
        # 정규식과 일치하는 노드들을 찾음
        matching_nodes = [
            node for node, _ in all_nodes
            if not node.is_dir and pattern.search(node.name)
        ]
        
        # 일치하는 노드가 없으면 알림 표시 후 원래 목록으로 복원
        if not matching_nodes:
            visible_nodes_out[:] = original_nodes
            return False, "검색 결과 없음"
            
        # 일치하는 노드의 모든 부모 노드를 수집
        visible_nodes_set = set(matching_nodes)
        for node in matching_nodes:
            # 노드의 모든 부모 추가
            parent = node.parent
            while parent:
                visible_nodes_set.add(parent)
                parent = parent.parent
        
        # 트리 구조를 유지하며 노드들 정렬
        visible_nodes_out[:] = [
            (node, level) for node, level in all_nodes
            if node in visible_nodes_set or (node.is_dir and node.children and 
                any(child in visible_nodes_set for child in node.children.values()))
        ]
        
        # 루트 노드를 결과에 포함 (테스트 케이스 요구사항)
        if not any(node[0] == root_node for node in visible_nodes_out):
            visible_nodes_out.insert(0, (root_node, 0))
        
        return True, ""
        
    except re.error:
        # 잘못된 정규식
        return False, "잘못된 정규식"

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