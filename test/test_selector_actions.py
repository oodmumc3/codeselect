#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_selector_actions.py - selector_actions.py 모듈 테스트

selector_actions.py 모듈의 함수들을 테스트하는 코드입니다.
"""

import os
import sys
import unittest
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from filetree import Node
from selector_actions import (
    toggle_selection, toggle_expand, select_all, 
    expand_all, apply_search_filter, toggle_current_dir_selection
)

class TestSelectorActions(unittest.TestCase):
    """selector_actions 모듈의 함수들을 테스트하는 클래스"""
    
    def setUp(self):
        """테스트 전에 파일 트리 구조를 설정합니다."""
        # 루트 노드 생성
        self.root_node = Node("test_root", True)
        
        # 디렉토리 추가
        dir1 = Node("dir1", True, self.root_node)
        dir2 = Node("dir2", True, self.root_node)
        self.root_node.children["dir1"] = dir1
        self.root_node.children["dir2"] = dir2
        
        # 파일 추가
        file1 = Node("file1.txt", False, self.root_node)
        file2 = Node("file2.py", False, dir1)
        file3 = Node("file3.md", False, dir2)
        
        self.root_node.children["file1.txt"] = file1
        dir1.children["file2.py"] = file2
        dir2.children["file3.md"] = file3
        
        # 기본적으로 모든 노드가 선택됨
        for node_name, node in self.root_node.children.items():
            node.selected = True
            if node.is_dir and node.children:
                for child_name, child in node.children.items():
                    child.selected = True
    
    def test_toggle_selection(self):
        """toggle_selection 함수가 노드와 하위 노드의 선택 상태를 올바르게 전환하는지 테스트합니다."""
        # 모든 노드의 선택 상태 확인
        self.assertTrue(self.root_node.selected)
        self.assertTrue(self.root_node.children["dir1"].selected)
        self.assertTrue(self.root_node.children["dir1"].children["file2.py"].selected)
        
        # dir1의 선택 상태 토글
        toggle_selection(self.root_node.children["dir1"])
        
        # dir1과 그 하위 노드의 선택 상태가 모두 변경되었는지 확인
        self.assertFalse(self.root_node.children["dir1"].selected)
        self.assertFalse(self.root_node.children["dir1"].children["file2.py"].selected)
        
        # 다른 노드들은 영향을 받지 않았는지 확인
        self.assertTrue(self.root_node.selected)
        self.assertTrue(self.root_node.children["dir2"].selected)
        self.assertTrue(self.root_node.children["dir2"].children["file3.md"].selected)
    
    def test_select_all(self):
        """select_all 함수가 모든 노드의 선택 상태를 올바르게 설정하는지 테스트합니다."""
        # 모든 노드 선택 해제
        select_all(self.root_node, False)
        
        # 모든 노드가 선택 해제되었는지 확인
        def check_selection_state(node, expected_state):
            self.assertEqual(node.selected, expected_state)
            if node.is_dir and node.children:
                for child in node.children.values():
                    check_selection_state(child, expected_state)
        
        check_selection_state(self.root_node, False)
        
        # 모든 노드 선택
        select_all(self.root_node, True)
        
        # 모든 노드가 선택되었는지 확인
        check_selection_state(self.root_node, True)
    
    def test_expand_all(self):
        """expand_all 함수가 모든 디렉토리의 확장 상태를 올바르게 설정하는지 테스트합니다."""
        # 모든 디렉토리 접기
        expand_all(self.root_node, False)
        
        # 모든 디렉토리가 접혀있는지 확인
        def check_expanded_state(node, expected_state):
            if node.is_dir:
                self.assertEqual(node.expanded, expected_state)
                if node.children:
                    for child in node.children.values():
                        check_expanded_state(child, expected_state)
        
        check_expanded_state(self.root_node, False)
        
        # 모든 디렉토리 펼치기
        expand_all(self.root_node, True)
        
        # 모든 디렉토리가 펼쳐있는지 확인
        check_expanded_state(self.root_node, True)
    
    def test_toggle_expand(self):
        """toggle_expand 함수가 디렉토리의 확장 상태를 올바르게 전환하는지 테스트합니다."""
        dir1 = self.root_node.children["dir1"]
        
        # 초기 상태 확인
        self.assertTrue(dir1.expanded)
        
        # 확장 상태 토글
        toggle_expand(dir1)
        
        # 토글 후 상태 확인
        self.assertFalse(dir1.expanded)
        
        # 다시 토글
        toggle_expand(dir1)
        
        # 다시 원래 상태로 돌아왔는지 확인
        self.assertTrue(dir1.expanded)
    
    def test_toggle_current_dir_selection(self):
        """toggle_current_dir_selection 함수가 현재 디렉토리의 파일들만 선택 상태를 전환하는지 테스트합니다."""
        dir1 = self.root_node.children["dir1"]
        
        # dir1의 자식들이 모두 선택되어 있는지 확인
        self.assertTrue(dir1.children["file2.py"].selected)
        
        # 현재 디렉토리 선택 상태 토글
        toggle_current_dir_selection(dir1)
        
        # dir1의 자식들이 선택 해제되었는지 확인
        self.assertFalse(dir1.children["file2.py"].selected)
        
        # 다른 노드들은 영향을 받지 않았는지 확인
        self.assertTrue(self.root_node.children["file1.txt"].selected)
        self.assertTrue(self.root_node.children["dir2"].children["file3.md"].selected)
        
        # 다시 토글
        toggle_current_dir_selection(dir1)
        
        # dir1의 자식들이 다시 선택되었는지 확인
        self.assertTrue(dir1.children["file2.py"].selected)
    
    def test_apply_search_filter(self):
        """apply_search_filter 함수가 검색어에 따라 올바르게 필터링하는지 테스트합니다."""
        # 'py' 확장자 파일만 검색
        search_query = r"\.py$"
        visible_nodes = []
        original_nodes = [(node, 0) for node in [self.root_node]]
        
        # 검색 필터 적용
        success, error_message = apply_search_filter(
            search_query, False, self.root_node, original_nodes, visible_nodes
        )
        
        # 검색 성공 여부 확인
        self.assertTrue(success)
        self.assertEqual(error_message, "")
        
        # 필터링된 노드 수 확인 (file2.py와 그 부모 노드들이 포함되어야 함)
        # 루트, dir1, file2.py가 보여야 함
        self.assertEqual(len(visible_nodes), 3)
        
        # file2.py가 결과에 포함되었는지 확인
        node_names = [node[0].name for node in visible_nodes]
        self.assertIn("file2.py", node_names)
        self.assertIn("dir1", node_names)
        self.assertIn("test_root", node_names)
        
        # file1.txt와 file3.md는 결과에 포함되지 않아야 함
        self.assertNotIn("file1.txt", node_names)
        self.assertNotIn("file3.md", node_names)
        
        # 존재하지 않는 패턴으로 검색
        search_query = "nonexistent"
        visible_nodes = []
        
        # 검색 필터 적용
        success, error_message = apply_search_filter(
            search_query, False, self.root_node, original_nodes, visible_nodes
        )
        
        # 검색 결과가 없을 때의 처리 확인
        self.assertFalse(success)
        self.assertEqual(error_message, "검색 결과 없음")
        self.assertEqual(visible_nodes, original_nodes)

if __name__ == '__main__':
    unittest.main()