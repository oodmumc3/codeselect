#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py - 공통 유틸리티 함수 모듈

CodeSelect 프로젝트의 공통 유틸리티 함수들을 포함하는 모듈입니다.
"""

import os
import sys
import fnmatch
import subprocess
import tempfile
from pathlib import Path

def get_language_name(extension):
    """
    파일 확장자를 언어 이름으로 변환합니다.
    
    Args:
        extension (str): 언어 확장자 (예: 'py', 'js')
        
    Returns:
        str: 확장자에 해당하는 언어 이름
    """
    language_map = {
        'py': 'Python',
        'c': 'C',
        'cpp': 'C++',
        'h': 'C/C++ Header',
        'hpp': 'C++ Header',
        'js': 'JavaScript',
        'ts': 'TypeScript',
        'java': 'Java',
        'html': 'HTML',
        'css': 'CSS',
        'php': 'PHP',
        'rb': 'Ruby',
        'go': 'Go',
        'rs': 'Rust',
        'swift': 'Swift',
        'kt': 'Kotlin',
        'sh': 'Shell',
        'md': 'Markdown',
        'json': 'JSON',
        'xml': 'XML',
        'yaml': 'YAML',
        'yml': 'YAML',
        'sql': 'SQL',
        'r': 'R',
    }
    return language_map.get(extension, extension.upper())

def try_copy_to_clipboard(text):
    """
    텍스트를 클립보드에 복사하려고 시도합니다. 실패 시 적절한 대체 방법을 사용합니다.
    
    Args:
        text (str): 클립보드에 복사할 텍스트
        
    Returns:
        bool: 클립보드 복사 성공 여부
    """
    try:
        # 플랫폼별 방법 시도
        if sys.platform == 'darwin':  # macOS
            try:
                process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
                process.communicate(text.encode('utf-8'))
                return True
            except:
                pass
        elif sys.platform == 'win32':  # Windows
            try:
                process = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
                process.communicate(text.encode('utf-8'))
                return True
            except:
                pass
        elif sys.platform.startswith('linux'):  # Linux
            for cmd in ['xclip -selection clipboard', 'xsel -ib']:
                try:
                    process = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE)
                    process.communicate(text.encode('utf-8'))
                    return True
                except:
                    continue

        # 모든 방법이 실패하면 홈 디렉토리에 파일 생성 시도
        fallback_path = os.path.expanduser("~/codeselect_output.txt")
        with open(fallback_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"클립보드 복사 실패. 출력이 다음 위치에 저장됨: {fallback_path}")
        return False
    except:
        print("클립보드에 복사하거나 파일에 저장할 수 없습니다.")
        return False

def generate_output_filename(directory_path, output_format='txt'):
    """
    디렉토리 이름을 기반으로 고유한 출력 파일 이름을 생성합니다.
    
    Args:
        directory_path (str): 대상 디렉토리 경로
        output_format (str): 출력 파일 형식 (기본값: 'txt')
        
    Returns:
        str: 생성된 출력 파일 이름
    """
    base_name = os.path.basename(os.path.abspath(directory_path))
    extension = f".{output_format}"

    # 기본 이름으로 시작
    output_name = f"{base_name}{extension}"
    counter = 1

    # 파일이 존재하면 카운터 추가
    while os.path.exists(output_name):
        output_name = f"{base_name}({counter}){extension}"
        counter += 1

    return output_name

def should_ignore_path(path, ignore_patterns=None):
    """
    주어진 경로가 무시해야 할 패턴과 일치하는지 확인합니다.
    
    Args:
        path (str): 확인할 파일 또는 디렉토리 경로
        ignore_patterns (list): 무시할 패턴 목록 (기본값: None)
        
    Returns:
        bool: 경로가 무시되어야 하면 True, 그렇지 않으면 False
    """
    if ignore_patterns is None:
        ignore_patterns = ['.git', '__pycache__', '*.pyc', '.DS_Store', '.idea', '.vscode']

    basename = os.path.basename(path)
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(basename, pattern):
            return True
    return False