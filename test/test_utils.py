#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_utils.py - utils.py 모듈 테스트

utils.py 모듈의 함수들을 테스트하는 코드입니다.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import get_language_name, generate_output_filename, should_ignore_path

class TestUtils(unittest.TestCase):
    """utils.py 모듈에 있는 함수들을 테스트하는 클래스"""
    
    def test_get_language_name(self):
        """get_language_name 함수가 올바른 언어 이름을 반환하는지 테스트합니다."""
        self.assertEqual(get_language_name('py'), 'Python')
        self.assertEqual(get_language_name('js'), 'JavaScript')
        self.assertEqual(get_language_name('cpp'), 'C++')
        self.assertEqual(get_language_name('unknown'), 'UNKNOWN')  # 알 수 없는 확장자
    
    def test_generate_output_filename(self):
        """generate_output_filename 함수가 올바른 출력 파일 이름을 생성하는지 테스트합니다."""
        # 임시 디렉토리 생성
        with tempfile.TemporaryDirectory() as temp_dir:
            # 기본 이름 확인
            output_name = generate_output_filename(temp_dir, 'txt')
            self.assertEqual(output_name, f"{os.path.basename(temp_dir)}.txt")
            
            # 이미 존재하는 파일이 있는 경우 확인
            Path(output_name).touch()  # 파일 생성
            output_name_2 = generate_output_filename(temp_dir, 'txt')
            self.assertEqual(output_name_2, f"{os.path.basename(temp_dir)}(1).txt")
            
            # 다른 형식 확인
            md_output = generate_output_filename(temp_dir, 'md')
            self.assertEqual(md_output, f"{os.path.basename(temp_dir)}.md")
    
    def test_should_ignore_path(self):
        """should_ignore_path 함수가 올바르게 무시할 경로를 식별하는지 테스트합니다."""
        # 기본 무시 패턴으로 테스트
        self.assertTrue(should_ignore_path('.git'))
        self.assertTrue(should_ignore_path('__pycache__'))
        self.assertTrue(should_ignore_path('example.pyc'))
        self.assertTrue(should_ignore_path('.DS_Store'))
        
        # 무시하지 않아야 할 경로
        self.assertFalse(should_ignore_path('main.py'))
        self.assertFalse(should_ignore_path('README.md'))
        
        # 사용자 정의 패턴으로 테스트
        custom_patterns = ['*.log', 'temp_*', 'backup']
        self.assertTrue(should_ignore_path('example.log', custom_patterns))
        self.assertTrue(should_ignore_path('temp_file', custom_patterns))
        self.assertTrue(should_ignore_path('backup', custom_patterns))
        self.assertFalse(should_ignore_path('main.py', custom_patterns))

if __name__ == '__main__':
    unittest.main()