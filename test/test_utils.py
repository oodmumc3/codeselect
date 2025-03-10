#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py 테스트
"""

import sys
import os
import tempfile

# 현재 디렉토리의 모듈을 가져오기
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from utils import get_language_name, generate_output_filename, should_ignore_path

def test_get_language_name():
    """get_language_name 함수 테스트"""
    assert get_language_name('py') == 'Python'
    assert get_language_name('cpp') == 'C++'
    assert get_language_name('unknown') == 'UNKNOWN'
    print("get_language_name 테스트 성공!")

def test_generate_output_filename():
    """generate_output_filename 함수 테스트"""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_dir = os.getcwd()
        try:
            os.chdir(temp_dir)
            filename = generate_output_filename(temp_dir)
            assert filename == os.path.basename(temp_dir) + ".txt"
            
            with open(filename, 'w') as f:
                f.write("테스트")
            
            filename2 = generate_output_filename(temp_dir)
            assert filename2 == os.path.basename(temp_dir) + "(1).txt"
            
            md_filename = generate_output_filename(temp_dir, 'md')
            assert md_filename == os.path.basename(temp_dir) + ".md"
            
            print("generate_output_filename 테스트 성공!")
        finally:
            os.chdir(original_dir)

def test_should_ignore_path():
    """should_ignore_path 함수 테스트"""
    ignore_patterns = ['.git', '__pycache__', '*.pyc', '.DS_Store']
    
    assert should_ignore_path('/path/to/.git', ignore_patterns) == True
    assert should_ignore_path('/path/to/__pycache__', ignore_patterns) == True
    assert should_ignore_path('/path/to/file.pyc', ignore_patterns) == True
    assert should_ignore_path('/path/to/.DS_Store', ignore_patterns) == True
    assert should_ignore_path('/path/to/valid_file.py', ignore_patterns) == False
    
    print("should_ignore_path 테스트 성공!")

if __name__ == "__main__":
    test_get_language_name()
    test_generate_output_filename()
    test_should_ignore_path()
    print("모든 utils.py 테스트 성공!")