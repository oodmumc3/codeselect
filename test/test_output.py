#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
output.py 모듈에 대한 테스트 코드
"""

import os
import sys
import unittest
import tempfile
import shutil
from unittest.mock import MagicMock, patch

# 테스트 대상 모듈 임포트
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import output

class TestOutput(unittest.TestCase):
    """output.py 모듈의 함수들을 테스트하는 클래스"""

    def setUp(self):
        """테스트를 위한 mock 객체 및 환경 설정"""
        # Node 클래스 모의 객체 생성
        self.root_node = MagicMock()
        self.root_node.name = "project"
        self.root_node.is_dir = True
        self.root_node.parent = None
        self.root_node.children = {}
        self.root_node.expanded = True
        self.root_node.selected = True

        # 임시 디렉토리 생성
        self.temp_dir = tempfile.mkdtemp()
        self.output_path = os.path.join(self.temp_dir, "output.txt")

    def tearDown(self):
        """테스트 후 임시 디렉토리 제거"""
        shutil.rmtree(self.temp_dir)

    def test_write_file_tree_to_string(self):
        """write_file_tree_to_string 함수 테스트"""
        # 간단한 파일 트리 구조 설정
        child1 = MagicMock()
        child1.name = "file1.py"
        child1.is_dir = False
        child1.parent = self.root_node
        child1.children = None
        
        child2 = MagicMock()
        child2.name = "dir1"
        child2.is_dir = True
        child2.parent = self.root_node
        child2.children = {}
        
        self.root_node.children = {"file1.py": child1, "dir1": child2}
        
        # 자식 디렉토리에 파일 추가
        subchild = MagicMock()
        subchild.name = "file2.py"
        subchild.is_dir = False
        subchild.parent = child2
        subchild.children = None
        
        child2.children = {"file2.py": subchild}
        
        # 함수 실행
        result = output.write_file_tree_to_string(self.root_node)
        
        # 결과 검증 (루트 노드는
        # "file1.py"와 "dir1"가 결과에 포함되어 있어야 함
        self.assertIn("file1.py", result)
        self.assertIn("dir1", result)
        self.assertIn("file2.py", result)

    def test_write_output_file_txt_format(self):
        """write_output_file 함수의 txt 형식 출력 테스트"""
        # 간단한 파일 내용 설정
        file_contents = [
            ("file1.py", "print('Hello, world!')"),
            ("dir1/file2.py", "import os\nprint(os.getcwd())")
        ]
        
        # 함수 호출
        with patch("output.write_file_tree_to_string", return_value="└── file1.py\n└── dir1\n    └── file2.py\n"):
            output_path = output.write_output_file(
                self.output_path, "/path/to/project", self.root_node, file_contents
            )
        
        # 출력 파일이 생성되었는지 확인
        self.assertTrue(os.path.exists(output_path))
        
        # 출력 내용 확인
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 특정 문자열이 출력에 포함되었는지 확인
        self.assertIn("<file_map>", content)
        self.assertIn("<file_contents>", content)
        self.assertIn("File: file1.py", content)
        self.assertIn("print('Hello, world!')", content)
        self.assertIn("File: dir1/file2.py", content)
        self.assertIn("import os", content)

    def test_write_markdown_output(self):
        """write_markdown_output 함수 테스트"""
        # 간단한 파일 내용 설정
        file_contents = [
            ("file1.py", "print('Hello, world!')"),
            ("dir1/file2.py", "import os\nprint(os.getcwd())")
        ]
        
        # 함수 호출
        with patch("output.write_file_tree_to_string", return_value="└── file1.py\n└── dir1\n    └── file2.py\n"):
            output.write_markdown_output(
                self.output_path, "/path/to/project", self.root_node, file_contents
            )
        
        # 출력 파일이 생성되었는지 확인
        self.assertTrue(os.path.exists(self.output_path))
        
        # 출력 내용 확인
        with open(self.output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 마크다운 형식이 올바른지 확인
        self.assertIn("# Project Files:", content)
        self.assertIn("## 📁 File Structure", content)
        self.assertIn("## 📄 File Contents", content)
        self.assertIn("### file1.py", content)
        self.assertIn("```py", content)

    def test_get_language_name(self):
        """get_language_name 함수 테스트"""
        self.assertEqual(output.get_language_name("py"), "Python")
        self.assertEqual(output.get_language_name("js"), "JavaScript")
        self.assertEqual(output.get_language_name("unknown"), "UNKNOWN")

    def test_write_llm_optimized_output(self):
        """write_llm_optimized_output 함수 테스트"""
        # 간단한 파일 내용 및 의존성 설정
        file_contents = [
            ("file1.py", "import file2\nprint('Hello, world!')"),
            ("dir1/file2.py", "import os\nprint(os.getcwd())")
        ]
        
        dependencies = {
            "file1.py": {"dir1/file2.py"},
            "dir1/file2.py": {"os"}
        }
        
        # 함수 호출
        with patch("output.write_file_tree_to_string", return_value="└── file1.py\n└── dir1\n    └── file2.py\n"):
            output.write_llm_optimized_output(
                self.output_path, "/path/to/project", self.root_node, file_contents, dependencies
            )
        
        # 출력 파일이 생성되었는지 확인
        self.assertTrue(os.path.exists(self.output_path))
        
        # 출력 내용 확인
        with open(self.output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # LLM 최적화 형식이 올바른지 확인
        self.assertIn("# PROJECT ANALYSIS FOR AI ASSISTANT", content)
        self.assertIn("## 📦 GENERAL INFORMATION", content)
        self.assertIn("## 🗂️ PROJECT STRUCTURE", content)
        self.assertIn("## 🔄 FILE RELATIONSHIPS", content)
        self.assertIn("## 📄 FILE CONTENTS", content)

if __name__ == "__main__":
    unittest.main()