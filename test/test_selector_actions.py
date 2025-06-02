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
        
        # 검색 결과가 없을 때의 처리 확인 (새로운 동작 방식: visible_nodes는 빈 리스트가 되어야 함)
        self.assertFalse(success)
        self.assertEqual(error_message, "검색 결과 없음")
        # self.assertEqual(visible_nodes, original_nodes) # 이전 동작
        self.assertEqual(len(visible_nodes), 0) # 수정된 동작: 빈 리스트여야 함


# Helper to get node names from a list of (Node, level) tuples
def get_node_names(nodes_with_levels):
    return sorted([node.name for node, level in nodes_with_levels])

class TestApplySearchFilterMultiPattern(unittest.TestCase):
    def setUp(self):
        # test_root
        # ├── common_utils
        # │   ├── script.py
        # │   └── Helper.PY
        # ├── data_files
        # │   ├── report.md
        # │   └── DATA.log
        # ├── another_empty_dir
        # ├── main_test.py
        # └── notes.txt
        self.root = Node("test_root", is_dir=True)
        self.common_utils = Node("common_utils", is_dir=True, parent=self.root)
        self.script_py = Node("script.py", is_dir=False, parent=self.common_utils)
        self.helper_PY = Node("Helper.PY", is_dir=False, parent=self.common_utils) # Uppercase extension
        self.common_utils.children = {"script.py": self.script_py, "Helper.PY": self.helper_PY}

        self.data_files = Node("data_files", is_dir=True, parent=self.root)
        self.report_md = Node("report.md", is_dir=False, parent=self.data_files)
        self.data_log = Node("DATA.log", is_dir=False, parent=self.data_files) # Uppercase name
        self.data_files.children = {"report.md": self.report_md, "DATA.log": self.data_log}

        self.another_empty_dir = Node("another_empty_dir", is_dir=True, parent=self.root) # Empty dir

        self.main_test_py = Node("main_test.py", is_dir=False, parent=self.root)
        self.notes_txt = Node("notes.txt", is_dir=False, parent=self.root)

        self.root.children = {
            "common_utils": self.common_utils,
            "data_files": self.data_files,
            "another_empty_dir": self.another_empty_dir,
            "main_test.py": self.main_test_py,
            "notes.txt": self.notes_txt
        }

        # Manually set expanded for testing parent expansion logic later
        self.root.expanded = False
        self.common_utils.expanded = False
        self.data_files.expanded = False

        # Original nodes for reference (full tree)
        # Correctly import flatten_tree from filetree module
        current_dir = Path(__file__).resolve().parent
        project_root = current_dir.parent
        sys.path.append(str(project_root)) # Add project root to sys.path
        from filetree import flatten_tree # Now this import should work

        self.original_nodes = flatten_tree(self.root)
        # Ensure all nodes in original_nodes have their parents set for the functions to work
        for node, _ in self.original_nodes:
            if node.parent: # if not root
                # this is already handled by Node class structure, but good to be aware
                pass


    def test_or_logic_multiple_patterns(self):
        visible_nodes_out = []
        queries = ["*.txt", "*.md"] # Case-insensitive by default
        success, msg = apply_search_filter(queries, False, self.root, self.original_nodes, visible_nodes_out)
        self.assertTrue(success)
        self.assertEqual(msg, "")
        self.assertEqual(get_node_names(visible_nodes_out), sorted(["test_root", "data_files", "report.md", "notes.txt"]))

    def test_wildcard_usage_multiple_patterns(self):
        visible_nodes_out = []
        queries = ["*util*", "test*.py"] # common_utils, main_test.py
        success, msg = apply_search_filter(queries, False, self.root, self.original_nodes, visible_nodes_out)
        self.assertTrue(success)
        self.assertEqual(msg, "")
        # common_utils and its children (script.py, Helper.PY) + main_test.py + root
        expected_nodes = ["test_root", "common_utils", "script.py", "Helper.PY", "main_test.py"]
        self.assertEqual(get_node_names(visible_nodes_out), sorted(expected_nodes))

    def test_case_sensitive_search(self):
        visible_nodes_out = []
        queries = ["DATA.*", "*.PY"] # DATA.log, Helper.PY
        success, msg = apply_search_filter(queries, True, self.root, self.original_nodes, visible_nodes_out) # case_sensitive = True
        self.assertTrue(success)
        self.assertEqual(msg, "")
        expected_nodes = ["test_root", "common_utils", "Helper.PY", "data_files", "DATA.log"]
        self.assertEqual(get_node_names(visible_nodes_out), sorted(expected_nodes))

    def test_case_insensitive_search(self):
        visible_nodes_out = []
        # Using same queries as sensitive, but expecting more matches
        queries = ["DATA.*", "*.PY"] # data.log, DATA.log, script.py, Helper.PY
        success, msg = apply_search_filter(queries, False, self.root, self.original_nodes, visible_nodes_out) # case_sensitive = False
        self.assertTrue(success)
        self.assertEqual(msg, "")
        expected_nodes = ["test_root", "common_utils", "script.py", "Helper.PY", "data_files", "DATA.log"]
        self.assertEqual(get_node_names(visible_nodes_out), sorted(expected_nodes))

    def test_no_matching_results(self):
        visible_nodes_out = []
        queries = ["nonexistent.file", "*.foo"]
        success, msg = apply_search_filter(queries, False, self.root, self.original_nodes, visible_nodes_out)
        self.assertFalse(success)
        self.assertEqual(msg, "검색 결과 없음")
        self.assertEqual(len(visible_nodes_out), 0) # Should be an empty list

    def test_empty_query_list(self):
        visible_nodes_out = []
        queries = []
        success, msg = apply_search_filter(queries, False, self.root, self.original_nodes, visible_nodes_out)
        self.assertTrue(success)
        self.assertEqual(msg, "")
        self.assertEqual(get_node_names(visible_nodes_out), get_node_names(self.original_nodes)) # Should be original_nodes

    def test_query_list_with_empty_whitespace_strings(self):
        visible_nodes_out = []
        queries = ["", " *.py ", " "] # Should behave like ["*.py"]
        success, msg = apply_search_filter(queries, False, self.root, self.original_nodes, visible_nodes_out)
        self.assertTrue(success)
        self.assertEqual(msg, "")
        # Expecting script.py, Helper.PY (due to case-insensitivity), main_test.py and their parents
        expected_nodes = ["test_root", "common_utils", "script.py", "Helper.PY", "main_test.py"]
        self.assertEqual(get_node_names(visible_nodes_out), sorted(expected_nodes))

    def test_invalid_regular_expression(self):
        visible_nodes_out = []
        queries = ["*[.py"] # Invalid regex
        success, msg = apply_search_filter(queries, False, self.root, self.original_nodes, visible_nodes_out)
        self.assertFalse(success)
        self.assertEqual(msg, "잘못된 정규식")
        # visible_nodes_out might be undefined or empty, not strictly specified for this error.
        # The primary check is the return tuple.

    def test_parent_directory_inclusion_and_expansion(self):
        # Reset expansion states for this specific test
        self.root.expanded = False
        self.common_utils.expanded = False
        self.data_files.expanded = False

        visible_nodes_out = []
        # Match one file in common_utils and one in data_files
        queries = ["script.py", "report.md"]
        success, msg = apply_search_filter(queries, False, self.root, self.original_nodes, visible_nodes_out)
        self.assertTrue(success)
        self.assertEqual(msg, "")

        expected_node_names = ["test_root", "common_utils", "script.py", "data_files", "report.md"]
        self.assertEqual(get_node_names(visible_nodes_out), sorted(expected_node_names))

        # Check expansion status
        # Create a map of nodes from visible_nodes_out for easy lookup
        result_nodes_map = {node.name: node for node, level in visible_nodes_out}

        self.assertTrue(result_nodes_map["test_root"].expanded, "Root node should be expanded")
        self.assertTrue(result_nodes_map["common_utils"].expanded, "common_utils should be expanded")
        self.assertTrue(result_nodes_map["data_files"].expanded, "data_files should be expanded")
        # another_empty_dir should not be in results and thus its expansion state is not set by this function
        self.assertFalse(self.another_empty_dir.expanded, "another_empty_dir should not be expanded by this search")


if __name__ == '__main__':
    unittest.main()