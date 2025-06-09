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
        'py': 'Python', 'c': 'C', 'cpp': 'C++', 'h': 'C/C++ Header', 'hpp': 'C++ Header',
        'js': 'JavaScript', 'ts': 'TypeScript', 'java': 'Java', 'html': 'HTML', 'css': 'CSS',
        'php': 'PHP', 'rb': 'Ruby', 'go': 'Go', 'rs': 'Rust', 'swift': 'Swift',
        'kt': 'Kotlin', 'sh': 'Shell', 'md': 'Markdown', 'json': 'JSON', 'xml': 'XML',
        'yaml': 'YAML', 'yml': 'YAML', 'sql': 'SQL', 'r': 'R',
    }
    return language_map.get(extension, extension.upper())

def try_copy_to_clipboard(text):
    """
    Attempts to copy the text to the clipboard. On failure, use an appropriate fallback method.

    Args:
        text (str): The text to copy to the clipboard.

    Returns:
        bool: Clipboard copy success or failure
    """
    try:
        if sys.platform == 'darwin':
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            return True
        elif sys.platform == 'win32':
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            return True
        elif sys.platform.startswith('linux'):
            for cmd in ['xclip -selection clipboard', 'xsel -ib']:
                try:
                    process = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    process.communicate(text.encode('utf-8'))
                    return True
                except FileNotFoundError:
                    continue
    except Exception:
        pass

    try:
        fallback_path = os.path.expanduser("~/codeselect_output.txt")
        with open(fallback_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Clipboard unavailable. Output saved to: {fallback_path}", file=sys.stderr)
    except Exception:
        print("Clipboard unavailable and could not write to fallback file.", file=sys.stderr)

    return False

def generate_output_filename(directory_path, output_format='txt'):
    """
    Generate unique output filenames based on directory names.

    Args:
        directory_path (str): Destination directory path
        output_format (str): Output file format (default: ‘txt’)

    Returns:
        str: Generated output file name
    """
    base_name = os.path.basename(os.path.abspath(directory_path))
    extension = f".{output_format}"
    output_name = f"{base_name}{extension}"
    counter = 1
    while os.path.exists(output_name):
        output_name = f"{base_name}({counter}){extension}"
        counter += 1
    return output_name

def load_gitignore_patterns(directory):
    """
    Reads `.gitignore` file and returns a list of valid ignore patterns.

    Args:
        directory (str): The directory containing the .gitignore file.

    Returns:
        list: List of ignore patterns from the .gitignore file.
    """
    gitignore_path = os.path.join(directory, ".gitignore")
    if not os.path.isfile(gitignore_path):
        return []

    patterns = []
    try:
        with open(gitignore_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    except Exception:
        pass # Ignore errors reading gitignore

    return patterns

def should_ignore_path(path, ignore_patterns=None, root_dir="."):
    """
    Checks if a path should be ignored based on .gitignore patterns.
    This version correctly implements the "last match wins" rule.
    """
    if not ignore_patterns:
        return False

    relative_path = os.path.relpath(path, root_dir).replace(os.sep, '/')
    if relative_path == '.':
        return False

    decision = None  # None: no match, True: ignore, False: don't ignore

    for p in ignore_patterns:
        original_pattern = p.strip()

        is_negated = original_pattern.startswith('!')
        if is_negated:
            pattern = original_pattern[1:]
        else:
            pattern = original_pattern

        is_dir_pattern = pattern.endswith('/')
        if is_dir_pattern:
            pattern = pattern.rstrip('/')

        match = False
        # Patterns without a slash match the basename of any path component.
        # Git's behavior is more complex, but this covers the common cases well.
        if '/' not in pattern:
            if fnmatch.fnmatch(os.path.basename(relative_path), pattern):
                match = True
        # Patterns with a slash are matched against the path from the root.
        else:
            if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(relative_path, pattern + '/**'):
                match = True

        if match:
            if is_dir_pattern and not os.path.isdir(path):
                continue
            decision = not is_negated

    return decision if decision is not None else False