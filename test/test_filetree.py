#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_filetree.py - filetree.py 모듈 테스트
"""

import os
import sys
import unittest
import tempfile
import shutil
from typing import List

# 테스트 대상 모듈 임포트
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from filetree import Node, build_file_tree, flatten_tree, count_selected_files, collect_selected_content

class TestFileTree(unittest.TestCase):
    """filetree.py 모듈 테스트 클래스"""
    
    def setUp(self):
        """각 테스트 전에 실행되는 설정"""
        # 임시 디렉토리 생성
        self.temp_dir = tempfile.mkdtemp()
        
        # 테스트용 파일 구조 생성
        os.mkdir(os.path.join(self.temp_dir, "dir1"))
        os.mkdir(os.path.join(self.temp_dir, "dir2"))
        os.mkdir(os.path.join(self.temp_dir, "dir1", "subdir"))
        
        # 파일 생성
        with open(os.path.join(self.temp_dir, "file1.txt"), "w") as f:
            f.write("File 1 content")
        
        with open(os.path.join(self.temp_dir, "file2.py"), "w") as f:
            f.write("print('File 2 content')")
        
        with open(os.path.join(self.temp_dir, "dir1", "file3.js"), "w") as f:
            f.write("console.log('File 3 content');")
        
        with open(os.path.join(self.temp_dir, "dir1", "subdir", "file4.txt"), "w") as f:
            f.write("File 4 content")
        
        # .gitignore 파일 생성
        with open(os.path.join(self.temp_dir, ".gitignore"), "w") as f:
            f.write("*.log\n")
            f.write("temp/\n")
        
        # 무시해야 할 파일/디렉토리 생성
        os.mkdir(os.path.join(self.temp_dir, "temp"))
        with open(os.path.join(self.temp_dir, "debug.log"), "w") as f:
            f.write("Debug log content")
    
    def tearDown(self):
        """각 테스트 후에 실행되는 정리"""
        # 임시 디렉토리 삭제
        shutil.rmtree(self.temp_dir)
    
    def test_node_class(self):
        """Node 클래스 테스트"""
        # 노드 생성
        parent = Node("parent", "/path/to/parent", is_dir=True)
        child1 = Node("child1", "/path/to/parent/child1", is_dir=False)
        child2 = Node("child2", "/path/to/parent/child2", is_dir=True)
        
        # 자식 추가
        parent.add_child(child1)
        parent.add_child(child2)
        
        # 검증
        self.assertEqual(len(parent.get_children()), 2)
        self.assertEqual(child1.parent, parent)
        self.assertEqual(child2.parent, parent)
        self.assertTrue("[D]" in str(parent))
        self.assertTrue("[F]" in str(child1))
    
    def test_build_file_tree(self):
        """build_file_tree 함수 테스트"""
        root = build_file_tree(self.temp_dir)
        
        # 루트 노드 검증
        self.assertEqual(root.name, os.path.basename(self.temp_dir))
        self.assertTrue(root.is_dir)
        self.assertTrue(root.expanded)
        
        # 자식 노드 확인 (정확한 갯수는 테스트 환경에 따라 다를 수 있음)
        # 따라서 필수 항목이 포함되어 있는지만 확인
        child_names = [child.name for child in root.children]
        
        # 필수 파일/디렉토리 존재 확인
        self.assertIn("dir1", child_names)
        self.assertIn("dir2", child_names)
        self.assertIn("file1.txt", child_names)
        self.assertIn("file2.py", child_names)
        
        # 무시해야 할 파일/디렉토리 확인
        self.assertNotIn("temp", child_names)
        self.assertNotIn("debug.log", child_names)
    
    def test_flatten_tree(self):
        """flatten_tree 함수 테스트"""
        root = build_file_tree(self.temp_dir)
        
        # 모든 디렉토리 확장
        def expand_all(node: Node) -> None:
            if node.is_dir:
                node.expanded = True
                for child in node.children:
                    expand_all(child)
        
        expand_all(root)
        
        # 트리 평탄화
        flat_nodes = flatten_tree(root)
        
        # 평탄화된 트리에 모든 항목이 포함되어 있는지 확인
        # 테스트 환경에 따라 다를 수 있으므로 정확한 개수 대신 최소한의 필수 항목 확인
        node_paths = [node.path for node in flat_nodes]
        
        # 필수 경로 포함 확인
        self.assertIn(self.temp_dir, node_paths)  # 루트
        self.assertIn(os.path.join(self.temp_dir, "dir1"), node_paths)  # dir1
        self.assertIn(os.path.join(self.temp_dir, "dir2"), node_paths)  # dir2
        self.assertIn(os.path.join(self.temp_dir, "file1.txt"), node_paths)  # file1.txt
        self.assertIn(os.path.join(self.temp_dir, "file2.py"), node_paths)  # file2.py
        self.assertIn(os.path.join(self.temp_dir, "dir1", "file3.js"), node_paths)  # dir1/file3.js
        self.assertIn(os.path.join(self.temp_dir, "dir1", "subdir"), node_paths)  # dir1/subdir
        self.assertIn(os.path.join(self.temp_dir, "dir1", "subdir", "file4.txt"), node_paths)  # dir1/subdir/file4.txt
    
    def test_count_selected_files(self):
        """count_selected_files 함수 테스트"""
        root = build_file_tree(self.temp_dir)
        
        # 초기에는 선택된 파일이 없어야 함
        self.assertEqual(count_selected_files(root), 0)
        
        # 일부 파일 선택
        file_nodes = [node for node in flatten_tree(root) if not node.is_dir]
        for i, node in enumerate(file_nodes):
            if i % 2 == 0:  # 짝수 인덱스만 선택
                node.selected = True
        
        # 선택된 파일 수 확인
        selected_count = sum(1 for node in file_nodes if node.selected)
        self.assertEqual(count_selected_files(root), selected_count)
    
    def test_collect_selected_content(self):
        """collect_selected_content 함수 테스트"""
        root = build_file_tree(self.temp_dir)
        
        # 파일 하나 선택
        file_node = None
        for node in flatten_tree(root):
            if not node.is_dir and node.name == "file1.txt":
                file_node = node
                break
        
        self.assertIsNotNone(file_node, "file1.txt를 찾을 수 없음")
        file_node.selected = True
        
        # 선택된 파일 내용 수집
        selected_content = collect_selected_content(root)
        
        # 하나의 파일만 선택되어 있어야 함
        self.assertEqual(len(selected_content), 1)
        
        # 파일 경로와 내용 검증
        file_path = os.path.join(self.temp_dir, "file1.txt")
        self.assertIn(file_path, selected_content)
        self.assertEqual(selected_content[file_path]['content'], "File 1 content")
        self.assertEqual(selected_content[file_path]['language'], "text")
    
    def test_directory_selection(self):
        """디렉토리 선택 시 하위 파일들도 선택되는지 테스트"""
        root = build_file_tree(self.temp_dir)
        
        # dir1 디렉토리 찾기
        dir_node = None
        for node in flatten_tree(root):
            if node.is_dir and node.name == "dir1":
                dir_node = node
                break
        
        self.assertIsNotNone(dir_node, "dir1 디렉토리를 찾을 수 없음")
        
        # dir1 디렉토리 선택
        dir_node.selected = True
        
        # 파일 내용 수집
        selected_content = collect_selected_content(root)
        
        # dir1 디렉토리 아래의 파일들이 포함되어 있는지 확인
        dir1_files = [
            os.path.join(self.temp_dir, "dir1", "file3.js"),
            os.path.join(self.temp_dir, "dir1", "subdir", "file4.txt")
        ]
        
        for file_path in dir1_files:
            self.assertIn(file_path, selected_content)
        
        # 선택되지 않은 파일들은 포함되지 않아야 함
        not_expected_files = [
            os.path.join(self.temp_dir, "file1.txt"),
            os.path.join(self.temp_dir, "file2.py")
        ]
        
        for file_path in not_expected_files:
            self.assertNotIn(file_path, selected_content)


if __name__ == "__main__":
    unittest.main()