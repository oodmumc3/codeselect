#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeSelect Utils - 유틸리티 함수 모음
"""

import os
import fnmatch
import sys
import subprocess

def get_language_name(extension):
    """파일 확장자를 언어 이름으로 변환합니다."""
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
    """클립보드에 텍스트를 복사하려고 시도합니다. 실패 시 대체 방법을 사용합니다."""
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

        # 모두 실패하면 홈 디렉토리에 파일 생성 시도
        fallback_path = os.path.expanduser("~/codeselect_output.txt")
        with open(fallback_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"클립보드 복사 실패. 출력이 다음 경로에 저장됨: {fallback_path}")
        return False
    except:
        print("클립보드에 복사하거나 파일로 저장할 수 없습니다.")
        return False

def generate_output_filename(directory_path, output_format='txt'):
    """디렉토리 이름을 기반으로 고유한 출력 파일 이름을 생성합니다."""
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

def should_ignore_path(path, ignore_patterns):
    """주어진 경로가 무시 패턴에 일치하는지 확인합니다."""
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False

# 버전 정보 (다른 모듈에서도 사용)
__version__ = "1.0.0"