#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
filetree.py - 파일 트리 구조 관리 모듈

이 모듈은 프로젝트 디렉토리의 파일 구조를 트리 형태로 구성하고 관리하는 기능을 제공합니다.
"""

import os
import re
from typing import Dict, List, Set, Tuple, Optional, Any, Callable

# utils.py에서 필요한 함수를 임포트 (예상)
from utils import should_ignore_path, get_language_name

class Node:
    """
    파일 트리의 노드를 표현하는 클래스
    
    각 노드는 파일 또는 디렉토리를 나타내며, 디렉토리인 경우 자식 노드들을 가질 수 있습니다.
    """
    def __init__(self, name: str, path: str, is_dir: bool = False):
        """
        Node 객체 초기화
        
        Args:
            name: 파일 또는 디렉토리 이름
            path: 파일 또는 디렉토리의 절대 경로
            is_dir: 디렉토리 여부 (True면 디렉토리, False면 파일)
        """
        self.name = name  # 파일 또는 디렉토리 이름
        self.path = path  # 파일 또는 디렉토리의 절대 경로
        self.is_dir = is_dir  # 디렉토리 여부
        self.children = []  # 자식 노드 목록 (디렉토리인 경우)
        self.parent = None  # 부모 노드
        self.selected = False  # 선택 여부
        self.expanded = False  # 확장 여부 (UI 표시용)
        
    def add_child(self, child: 'Node') -> None:
        """
        자식 노드 추가
        
        Args:
            child: 추가할 자식 노드
        """
        self.children.append(child)
        child.parent = self
        
    def get_children(self) -> List['Node']:
        """
        자식 노드 목록 반환
        
        Returns:
            자식 노드 목록
        """
        return self.children
    
    def __str__(self) -> str:
        """
        노드를 문자열로 표현
        
        Returns:
            노드의 문자열 표현
        """
        return f"{'[D] ' if self.is_dir else '[F] '}{self.name} {'(선택됨)' if self.selected else ''}"


def build_file_tree(directory: str) -> Node:
    """
    주어진 디렉토리의 파일 구조를 트리 형태로 구성
    
    Args:
        directory: 스캔할 디렉토리 경로
    
    Returns:
        루트 노드
    
    예시:
        root = build_file_tree('/path/to/project')
    """
    # 디렉토리 경로 정규화
    directory = os.path.abspath(directory)
    
    # 루트 노드 생성
    root_name = os.path.basename(directory)
    if not root_name:  # 루트 디렉토리인 경우
        root_name = directory
    root = Node(root_name, directory, is_dir=True)
    root.expanded = True  # 루트는 기본적으로 확장
    
    # .gitignore 패턴 로드 (있는 경우)
    gitignore_patterns = []
    gitignore_path = os.path.join(directory, '.gitignore')
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        gitignore_patterns.append(line)
        except Exception:
            pass  # .gitignore 파일을 읽을 수 없는 경우 무시
    
    # 재귀적으로 디렉토리 탐색
    _build_tree_recursive(root, directory, gitignore_patterns)
    
    return root


def _should_ignore(path: str, gitignore_patterns: List[str]) -> bool:
    """
    파일 또는 디렉토리가 무시되어야 하는지 확인
    
    Args:
        path: 파일 또는 디렉토리 경로
        gitignore_patterns: .gitignore 패턴 목록
    
    Returns:
        무시해야 하면 True, 아니면 False
    """
    # 기본적으로 무시할 파일/디렉토리 패턴
    default_ignore = [
        '.*',           # 숨김 파일/디렉토리 (.으로 시작하는 항목)
        '*~',           # 백업 파일
        '__pycache__',  # Python 캐시 디렉토리
        '*.pyc',        # Python 컴파일된 파일
        '*.pyo',        # Python 최적화된 파일
        '*.pyd',        # Python 확장 모듈
        'node_modules', # Node.js 모듈 디렉토리
        'venv',         # Python 가상 환경
        'env',          # Python 가상 환경
        '.venv',        # Python 가상 환경
        '.env',         # 환경 변수 파일
        'build',        # 빌드 디렉토리
        'dist',         # 배포 디렉토리
        '.DS_Store'     # macOS 디렉토리 정보 파일
    ]
    
    # .gitignore 패턴에 기본 무시 패턴 추가
    patterns = default_ignore + gitignore_patterns
    
    # 파일/디렉토리 이름
    name = os.path.basename(path)
    
    # 패턴 매칭
    for pattern in patterns:
        # 패턴이 /로 시작하면 루트 디렉토리부터 매칭
        if pattern.startswith('/'):
            if path.endswith(pattern[1:]):
                return True
        # 디렉토리만 매칭 (/로 끝나는 경우)
        elif pattern.endswith('/'):
            if os.path.isdir(path) and name == pattern[:-1]:
                return True
        # 간단한 와일드카드 매칭
        elif '*' in pattern:
            if pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return True
            elif pattern.endswith('*'):
                if name.startswith(pattern[:-1]):
                    return True
            elif pattern == '*.*':
                if '.' in name:
                    return True
        # 정확한 이름 매칭
        elif name == pattern:
            return True
    
    return False


def _build_tree_recursive(parent_node: Node, directory: str, gitignore_patterns: List[str]) -> None:
    """
    재귀적으로 디렉토리를 탐색하여 트리 구성
    
    Args:
        parent_node: 부모 노드
        directory: 현재 탐색 중인 디렉토리 경로
        gitignore_patterns: .gitignore 패턴 목록
    """
    # 디렉토리 내 항목들을 이름순으로 정렬
    entries = []
    try:
        with os.scandir(directory) as it:
            for entry in it:
                # 무시해야 할 파일/디렉토리는 건너뛰기
                if _should_ignore(entry.path, gitignore_patterns):
                    continue
                entries.append(entry)
        entries.sort(key=lambda e: e.name.lower())  # 대소문자 구분 없이 정렬
    except PermissionError:
        return  # 권한 없음
    
    # 먼저 디렉토리 처리
    for entry in entries:
        if entry.is_dir():            
            # 디렉토리 노드 생성 및 추가
            node = Node(entry.name, entry.path, is_dir=True)
            parent_node.add_child(node)
            
            # 재귀적으로 하위 디렉토리 처리
            _build_tree_recursive(node, entry.path, gitignore_patterns)
    
    # 그 다음 파일 처리
    for entry in entries:
        if entry.is_file():            
            # 파일 노드 생성 및 추가
            node = Node(entry.name, entry.path, is_dir=False)
            parent_node.add_child(node)


def flatten_tree(root: Node) -> List[Node]:
    """
    트리를 평탄화하여 노드 목록으로 변환 (UI 표시용)
    
    Args:
        root: 루트 노드
    
    Returns:
        표시 가능한 노드 목록
    """
    flat_list = []
    
    def _flatten_recursive(node: Node, depth: int = 0) -> None:
        """
        재귀적으로 트리를 평탄화
        
        Args:
            node: 현재 노드
            depth: 현재 깊이
        """
        # 현재 노드 추가
        node.depth = depth  # UI 표시용 깊이 정보 추가
        flat_list.append(node)
        
        # 디렉토리이고 확장된 경우에만 자식 노드 추가
        if node.is_dir and node.expanded:
            for child in node.children:
                _flatten_recursive(child, depth + 1)
    
    _flatten_recursive(root)
    return flat_list


def count_selected_files(root: Node) -> int:
    """
    선택된 파일 수 계산
    
    Args:
        root: 루트 노드
    
    Returns:
        선택된 파일 수
    """
    count = 0
    
    def _count_recursive(node: Node) -> None:
        """
        재귀적으로 선택된 파일 수 계산
        
        Args:
            node: 현재 노드
        """
        nonlocal count
        if node.selected and not node.is_dir:
            count += 1
        
        for child in node.children:
            _count_recursive(child)
    
    _count_recursive(root)
    return count


def collect_selected_content(root: Node) -> Dict[str, Dict[str, Any]]:
    """
    선택된 파일들의 내용 수집
    
    Args:
        root: 루트 노드
    
    Returns:
        선택된 파일들의 내용을 담은 딕셔너리
        {파일경로: {'content': 파일내용, 'language': 언어이름}}
    """
    selected_files = {}
    
    def _collect_recursive(node: Node) -> None:
        """
        재귀적으로 선택된 파일 내용 수집
        
        Args:
            node: 현재 노드
        """
        # 디렉토리가 선택된 경우 모든 하위 파일도 선택
        if node.is_dir and node.selected:
            for child in node.children:
                if not child.selected:  # 이미 선택된 경우 중복 방지
                    child.selected = True
                    _collect_recursive(child)
        
        # 파일이 선택된 경우 내용 수집
        if not node.is_dir and node.selected:
            try:
                with open(node.path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 언어 식별
                ext = os.path.splitext(node.name)[1].lstrip('.')
                
                # 특수 케이스 처리: .txt 파일은 'text'로 매핑
                if ext.lower() == 'txt':
                    language = 'text'
                else:
                    language = get_language_name(ext).lower()  # 소문자로 변환
                
                selected_files[node.path] = {
                    'content': content,
                    'language': language
                }
            except Exception as e:
                # 파일을 읽을 수 없는 경우 오류 메시지 추가
                selected_files[node.path] = {
                    'content': f"// 파일을 읽을 수 없음: {str(e)}",
                    'language': 'text'
                }
        
        # 자식 노드 처리
        for child in node.children:
            _collect_recursive(child)
    
    _collect_recursive(root)
    return selected_files


def collect_all_content(root: Node) -> Dict[str, Dict[str, Any]]:
    """
    모든 파일의 내용 수집 (skip-selection 옵션용)
    
    Args:
        root: 루트 노드
    
    Returns:
        모든 파일의 내용을 담은 딕셔너리
        {파일경로: {'content': 파일내용, 'language': 언어이름}}
    """
    # 모든 노드 선택 상태로 변경
    def _select_all_recursive(node: Node) -> None:
        node.selected = True
        for child in node.children:
            _select_all_recursive(child)
    
    _select_all_recursive(root)
    
    # 선택된 파일 내용 수집 (모든 파일이 선택됨)
    return collect_selected_content(root)


if __name__ == "__main__":
    # 모듈 테스트용 코드 (직접 실행할 경우)
    print("파일 트리 모듈 테스트")
    
    # 현재 디렉토리의 파일 트리 생성
    test_dir = os.path.dirname(os.path.abspath(__file__))
    root = build_file_tree(test_dir)
    
    # 평탄화된 트리 출력
    flat_nodes = flatten_tree(root)
    for node in flat_nodes:
        indent = "  " * node.depth
        print(f"{indent}{node}")
    
    print(f"총 파일 수: {len([n for n in flat_nodes if not n.is_dir])}")