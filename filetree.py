#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
filetree.py - 파일 트리 구조 관리 모듈

파일 트리 구조를 생성하고 관리하는 기능을 제공하는 모듈입니다.
"""

import os
import sys
import fnmatch
from utils import should_ignore_path

class Node:
    """
    파일 트리의 노드를 표현하는 클래스
    
    파일 또는 디렉토리를 나타내며, 디렉토리인 경우 자식 노드를 가질 수 있습니다.
    """
    def __init__(self, name, is_dir, parent=None):
        """
        Node 클래스 초기화
        
        Args:
            name (str): 노드의 이름 (파일/디렉토리 이름)
            is_dir (bool): 디렉토리 여부
            parent (Node, optional): 부모 노드
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
        노드의 전체 경로를 반환합니다.
        
        Returns:
            str: 노드의 전체 경로
        """
        if self.parent is None:
            return self.name
        parent_path = self.parent.path
        if parent_path.endswith(os.sep):
            return parent_path + self.name
        return parent_path + os.sep + self.name

def build_file_tree(root_path, ignore_patterns=None):
    """
    파일 구조를 나타내는 트리를 구축합니다.
    
    Args:
        root_path (str): 루트 디렉토리 경로
        ignore_patterns (list, optional): 무시할 패턴 목록
        
    Returns:
        Node: 파일 트리의 루트 노드
    """
    if ignore_patterns is None:
        ignore_patterns = ['.git', '__pycache__', '*.pyc', '.DS_Store', '.idea', '.vscode']

    def should_ignore(path):
        """
        주어진 경로가 무시해야 할 패턴과 일치하는지 확인합니다.
        
        Args:
            path (str): 확인할 경로
            
        Returns:
            bool: 무시해야 하면 True, 그렇지 않으면 False
        """
        return should_ignore_path(os.path.basename(path), ignore_patterns)

    root_name = os.path.basename(root_path.rstrip(os.sep))
    if not root_name:  # 루트 디렉토리 경우
        root_name = root_path

    root_node = Node(root_name, True)
    root_node.full_path = root_path  # 루트 노드에 절대 경로 저장

    def add_path(current_node, path_parts, full_path):
        """
        경로의 각 부분을 트리에 추가합니다.
        
        Args:
            current_node (Node): 현재 노드
            path_parts (list): 경로 부분 목록
            full_path (str): 전체 경로
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
                if filename not in root_node.children and not should_ignore(filename):
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
                    if not should_ignore(filename) and filename not in current.children:
                        file_node = Node(filename, False, current)
                        current.children[filename] = file_node

    return root_node

def flatten_tree(node, visible_only=True):
    """
    트리를 네비게이션을 위한 노드 목록으로 평탄화합니다.
    
    Args:
        node (Node): 루트 노드
        visible_only (bool, optional): 보이는 노드만 포함할지 여부
        
    Returns:
        list: (노드, 레벨) 튜플의 목록
    """
    flat_nodes = []

    def _traverse(node, level=0):
        """
        트리를 순회하며 평탄화된 노드 목록을 생성합니다.
        
        Args:
            node (Node): 현재 노드
            level (int, optional): 현재 레벨
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
    선택된 파일 수를 계산합니다 (디렉토리 제외).
    
    Args:
        node (Node): 루트 노드
        
    Returns:
        int: 선택된 파일 수
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
    선택된 파일들의 내용을 수집합니다.
    
    Args:
        node (Node): 루트 노드
        root_path (str): 루트 디렉토리 경로
        
    Returns:
        list: (파일 경로, 내용) 튜플의 목록
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
    모든 파일의 내용을 수집합니다 (분석용).
    
    Args:
        node (Node): 루트 노드
        root_path (str): 루트 디렉토리 경로
        
    Returns:
        list: (파일 경로, 내용) 튜플의 목록
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