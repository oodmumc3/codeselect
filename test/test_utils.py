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

from utils import get_language_name, generate_output_filename, should_ignore_path, load_gitignore_patterns

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
        
        # gitignore 스타일 패턴으로 테스트
        gitignore_patterns = ['*.log', 'ignored_dir/', 'ignored_file.txt', '!important.log']
        self.assertTrue(should_ignore_path('error.log', gitignore_patterns))
        self.assertTrue(should_ignore_path('ignored_file.txt', gitignore_patterns))
        # 부정 패턴 테스트
        self.assertFalse(should_ignore_path('important.log', gitignore_patterns))
        # 디렉토리 패턴 테스트 (디렉토리 경로로 설정)
        temp_dir = tempfile.TemporaryDirectory()
        ignored_dir = os.path.join(temp_dir.name, 'ignored_dir')
        os.makedirs(ignored_dir)
        self.assertTrue(should_ignore_path(ignored_dir, gitignore_patterns))
        temp_dir.cleanup()
        
    def test_load_gitignore_patterns(self):
        """load_gitignore_patterns 함수가 .gitignore 파일에서 패턴을 올바르게 로드하는지 테스트합니다."""
        # 임시 디렉토리 생성
        with tempfile.TemporaryDirectory() as temp_dir:
            # 테스트용 .gitignore 파일 생성
            gitignore_content = """
# 주석 라인
*.log
ignored_dir/

# 빈 라인

ignored_file.txt
!important.log
            """
            gitignore_path = os.path.join(temp_dir, ".gitignore")
            with open(gitignore_path, "w") as f:
                f.write(gitignore_content)
            
            # 패턴 로드
            patterns = load_gitignore_patterns(temp_dir)
            
            # 예상 패턴 확인
            self.assertEqual(len(patterns), 4)
            self.assertIn("*.log", patterns)
            self.assertIn("ignored_dir/", patterns)
            self.assertIn("ignored_file.txt", patterns)
            self.assertIn("!important.log", patterns)
            
            # 주석과 빈 라인은 포함되지 않아야 함
            self.assertNotIn("# 주석 라인", patterns)
            self.assertNotIn("# 빈 라인", patterns)
            self.assertNotIn("", patterns)
            
            # .gitignore 파일이 없는 경우
            non_gitignore_dir = os.path.join(temp_dir, "subdir")
            os.makedirs(non_gitignore_dir)
            self.assertEqual(load_gitignore_patterns(non_gitignore_dir), [])

if __name__ == '__main__':
    unittest.main()
