#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_filetree.py - filetree.py 모듈 테스트

filetree.py 모듈의 클래스와 함수들을 테스트하는 코드입니다.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from filetree import Node, build_file_tree, flatten_tree, count_selected_files, collect_selected_content, collect_all_content

class TestNode(unittest.TestCase):
    """Node 클래스를 테스트하는 클래스"""
    
    def test_node_initialization(self):
        """Node 클래스 초기화가 올바르게 되는지 테스트합니다."""
        # 파일 노드 테스트
        file_node = Node("test.py", False)
        self.assertEqual(file_node.name, "test.py")
        self.assertFalse(file_node.is_dir)
        self.assertIsNone(file_node.children)
        self.assertIsNone(file_node.parent)
        self.assertTrue(file_node.selected)
        
        # 디렉토리 노드 테스트
        dir_node = Node("test_dir", True)
        self.assertEqual(dir_node.name, "test_dir")
        self.assertTrue(dir_node.is_dir)
        self.assertEqual(dir_node.children, {})
        self.assertIsNone(dir_node.parent)
        self.assertTrue(dir_node.selected)
        self.assertTrue(dir_node.expanded)
    
    def test_node_path(self):
        """Node의 path 프로퍼티가 올바른 경로를 반환하는지 테스트합니다."""
        # 루트 노드
        root = Node("root", True)
        self.assertEqual(root.path, "root")
        
        # 자식 노드
        child = Node("child", True, root)
        self.assertEqual(child.path, "root" + os.sep + "child")
        
        # 손자 노드
        grandchild = Node("grandchild.py", False, child)
        self.assertEqual(grandchild.path, "root" + os.sep + "child" + os.sep + "grandchild.py")

class TestFileTree(unittest.TestCase):
    """파일 트리 관련 함수들을 테스트하는 클래스"""

    def setUp(self):
        """테스트 전에 임시 디렉토리와 파일 구조를 생성합니다."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = self.temp_dir.name

        # 기본 디렉토리 구조 생성
        os.makedirs(os.path.join(self.test_dir, "dir1"))
        os.makedirs(os.path.join(self.test_dir, "dir2", "subdir"))

        # 몇 가지 파일 생성
        Path(os.path.join(self.test_dir, "file1.txt")).write_text("File 1 content")
        Path(os.path.join(self.test_dir, "dir1", "file2.py")).write_text("File 2 content")
        Path(os.path.join(self.test_dir, "dir2", "file3.md")).write_text("File 3 content")
        Path(os.path.join(self.test_dir, "dir2", "subdir", "file4.js")).write_text("File 4 content")

        # 무시할 파일과 디렉토리 생성
        os.makedirs(os.path.join(self.test_dir, ".git"))
        os.makedirs(os.path.join(self.test_dir, "__pycache__"))
        Path(os.path.join(self.test_dir, ".DS_Store")).touch()
        Path(os.path.join(self.test_dir, "dir1", "temp.pyc")).touch()
        
        # .gitignore 테스트를 위한 추가 파일 생성
        Path(os.path.join(self.test_dir, "ignored_file.txt")).touch()
        Path(os.path.join(self.test_dir, "error.log")).touch()
        Path(os.path.join(self.test_dir, "important.log")).touch()
        os.makedirs(os.path.join(self.test_dir, "ignored_dir"))
        Path(os.path.join(self.test_dir, "ignored_dir", "some_file.txt")).touch()
    
    def tearDown(self):
        """테스트 후에 임시 디렉토리를 정리합니다."""
        self.temp_dir.cleanup()
    
    def test_build_file_tree(self):
        """build_file_tree 함수가 올바른 파일 트리를 생성하는지 테스트합니다."""
        root_node = build_file_tree(self.test_dir)
        
        # 루트 노드 확인
        self.assertEqual(root_node.name, os.path.basename(self.test_dir))
        self.assertTrue(root_node.is_dir)
        
        # 필터링 확인 - 무시된 파일/디렉토리는 포함되지 않아야 함
        root_children = list(root_node.children.keys())
        self.assertIn("dir1", root_children)
        self.assertIn("dir2", root_children)
        self.assertIn("file1.txt", root_children)
        self.assertNotIn(".git", root_children)
        self.assertNotIn("__pycache__", root_children)
        self.assertNotIn(".DS_Store", root_children)
        
        # 중첩된 구조 확인
        dir1_node = root_node.children["dir1"]
        self.assertTrue(dir1_node.is_dir)
        self.assertIn("file2.py", dir1_node.children)
        self.assertNotIn("temp.pyc", dir1_node.children)
        
        dir2_node = root_node.children["dir2"]
        self.assertTrue(dir2_node.is_dir)
        self.assertIn("file3.md", dir2_node.children)
        self.assertIn("subdir", dir2_node.children)
        
        subdir_node = dir2_node.children["subdir"]
        self.assertTrue(subdir_node.is_dir)
        self.assertIn("file4.js", subdir_node.children)
    
    def test_flatten_tree(self):
        """flatten_tree 함수가 트리를 올바르게 평탄화하는지 테스트합니다."""
        root_node = build_file_tree(self.test_dir)

        # 모든 노드 포함 (visible_only=False)
        flat_nodes = flatten_tree(root_node, visible_only=False)

        # 노드 수 확인 (루트 제외)
        # 실제 테스트된 파일 시스템에 있는 노드 수
        self.assertEqual(len(flat_nodes), 12)

        # 레벨 확인
        level_0_nodes = [node for node, level in flat_nodes if level == 0]
        level_1_nodes = [node for node, level in flat_nodes if level == 1]
        level_2_nodes = [node for node, level in flat_nodes if level == 2]

        # 레벨별 노드 수도 조정
        self.assertEqual(len(level_0_nodes), 7)  # 최상위 노드들
        self.assertEqual(len(level_1_nodes), 4)  # 중간 레벨 노드들
        self.assertEqual(len(level_2_nodes), 1)  # 최하위 노드들

        # 노드 접힘 테스트
        root_node.children["dir2"].expanded = False
        flat_nodes_visible = flatten_tree(root_node, visible_only=True)

        # dir2 내부 노드들(file3.md, subdir, file4.js)은 보이지 않아야 함
        # 접힌 노드를 제외한 노드 수
        self.assertEqual(len(flat_nodes_visible), 9)  # dir2 내부 노드 3개 제외
    
    def test_count_selected_files(self):
        """count_selected_files 함수가 올바르게 선택된 파일 수를 계산하는지 테스트합니다."""
        root_node = build_file_tree(self.test_dir)

        # 기본적으로 모든 파일이 선택됨
        self.assertEqual(count_selected_files(root_node), 8)  # 실제 테스트 환경의 파일 수

        # 일부 파일 선택 해제
        root_node.children["file1.txt"].selected = False
        root_node.children["dir1"].children["file2.py"].selected = False

        self.assertEqual(count_selected_files(root_node), 6)  # 2개 파일 선택 해제됨

        # 디렉토리 선택 해제 (하위 파일 포함)
        root_node.children["dir2"].selected = False

        # 디렉토리 자체는 포함되지 않고, 내부 파일만 계산됨
        # dir2를 선택 해제했지만 그 안의 파일들의 selected 상태는 변경되지 않음
        self.assertEqual(count_selected_files(root_node), 6)  # dir2 선택 해제는 파일 수에 영향 없음
    
    def test_collect_selected_content(self):
        """collect_selected_content 함수가 선택된 파일의 내용을 올바르게 수집하는지 테스트합니다."""
        root_node = build_file_tree(self.test_dir)

        # 일부 파일만 선택
        root_node.children["dir1"].children["file2.py"].selected = False

        contents = collect_selected_content(root_node, self.test_dir)

        # 선택된 파일 수 확인 (하나 선택 해제됨)
        self.assertEqual(len(contents), 7)  # 총 8개 파일 중 file2.py 제외한 7개

        # 파일 경로와 내용 확인
        paths = [path for path, _ in contents]

        base_name = os.path.basename(self.test_dir)
        
        # 주요 파일들이 포함되어 있는지만 확인
        expected_paths = [
            "file1.txt",
            f"{base_name}{os.sep}dir2{os.sep}file3.md",
            f"{base_name}{os.sep}dir2{os.sep}subdir{os.sep}file4.js",
            "important.log"
        ]

        # 각 파일이 포함되어 있는지 확인
        for exp_path in expected_paths:
            self.assertTrue(any(exp_path in p for p in paths), f"경로 {exp_path}가 결과에 없습니다")

        # 선택되지 않은 파일이 포함되지 않는지 확인
        self.assertFalse(any("file2.py" in p for p in paths))
    
    def test_collect_all_content(self):
        """collect_all_content 함수가 모든 파일의 내용을 올바르게 수집하는지 테스트합니다."""
        root_node = build_file_tree(self.test_dir)

        # 일부 파일 선택 해제 (영향을 주지 않아야 함)
        root_node.children["dir1"].children["file2.py"].selected = False

        contents = collect_all_content(root_node, self.test_dir)

        # 모든 파일이 포함되어야 함
        self.assertEqual(len(contents), 8)  # 실제 테스트 환경의 총 파일 수

        # 파일 경로와 내용 확인
        paths = [path for path, _ in contents]

        base_name = os.path.basename(self.test_dir)
        
        # 주요 파일들이 포함되어 있는지만 확인
        expected_paths = [
            "file1.txt",
            f"{base_name}{os.sep}dir1{os.sep}file2.py",
            f"{base_name}{os.sep}dir2{os.sep}file3.md",
            f"{base_name}{os.sep}dir2{os.sep}subdir{os.sep}file4.js",
            "important.log"
        ]

        # 각 파일이 포함되어 있는지 확인
        for exp_path in expected_paths:
            self.assertTrue(any(exp_path in p for p in paths), f"경로 {exp_path}가 결과에 없습니다")
            
    def test_gitignore_filtering(self):
        """`.gitignore` 패턴이 파일과 디렉토리를 올바르게 제외하는지 테스트합니다."""
        # 테스트용 .gitignore 파일 생성
        with open(os.path.join(self.test_dir, ".gitignore"), "w") as f:
            f.write("*.log\nignored_dir/\nignored_file.txt\n!important.log")
        
        # 파일 트리 빌드
        root_node = build_file_tree(self.test_dir)
        
        # .gitignore에 의해 필터링되는지 확인
        root_children = list(root_node.children.keys())
        
        # 무시되어야 하는 파일들 확인
        self.assertNotIn("ignored_dir", root_children)
        self.assertNotIn("ignored_file.txt", root_children)
        self.assertNotIn("error.log", root_children)
        
        # 제외된 파일은 포함되어야 함
        self.assertIn("important.log", root_children)
        
        # 기본 필터링도 여전히 적용되는지 확인
        self.assertNotIn(".git", root_children)
        self.assertNotIn("__pycache__", root_children)
        self.assertNotIn(".DS_Store", root_children)

if __name__ == '__main__':
    unittest.main()
