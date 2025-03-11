#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeSelect - Dependency module

이 모듈은 프로젝트 파일 간의 의존성 분석 기능을 제공합니다.
다양한 프로그래밍 언어의 import, include, require 등의 패턴을 인식하여
파일 간의 참조 관계를 분석합니다.
"""

import re
import os

def analyze_dependencies(root_path, file_contents):
    """
    Analyse dependency relationships between project files.
    
    Recognise patterns such as import, include, and require in various programming languages to analyse dependencies between
    Analyses dependencies between files.
    
    Args:
        root_path (str): Project root path.
        file_contents (list): List of file contents [(path, contents), ...]
        
    Returns:
        dict: file-specific dependency information {filepath: {dependency1, dependency2, ...}, ...}
    """
    dependencies = {}
    imports = {}

    # 다양한 언어별 패턴 정의
    language_patterns = {
        # Python
        '.py': [
            r'^from\s+([\w.]+)\s+import',
            r'^import\s+([\w.]+)',
        ],
        # C/C++
        '.c': [r'#include\s+[<"]([^>"]+)[>"]'],
        '.h': [r'#include\s+[<"]([^>"]+)[>"]'],
        '.cpp': [r'#include\s+[<"]([^>"]+)[>"]'],
        '.hpp': [r'#include\s+[<"]([^>"]+)[>"]'],
        # JavaScript/TypeScript
        '.js': [
            r'(?:import|require)\s*\(?[\'"]([@\w\-./]+)[\'"]',
            r'from\s+[\'"]([@\w\-./]+)[\'"]',
            r'import\s+{[^}]*\b(\w+)\b[^}]*}\s+from',  # Destructured imports
        ],
        '.ts': [
            r'(?:import|require)\s*\(?[\'"]([@\w\-./]+)[\'"]',
            r'from\s+[\'"]([@\w\-./]+)[\'"]',
            r'import\s+{[^}]*\b(\w+)\b[^}]*}\s+from',  # Destructured imports
        ],
        # Java
        '.java': [
            r'import\s+([\w.]+)',
        ],
        # Go
        '.go': [
            r'import\s+\(\s*(?:[_\w]*\s+)?["]([^"]+)["]',
            r'import\s+(?:[_\w]*\s+)?["]([^"]+)["]',
        ],
        # Ruby
        '.rb': [
            r'require\s+[\'"]([^\'"]+)[\'"]',
            r'require_relative\s+[\'"]([^\'"]+)[\'"]',
        ],
        # PHP
        '.php': [
            r'(?:require|include)(?:_once)?\s*\(?[\'"]([^\'"]+)[\'"]',
            r'use\s+([\w\\]+)',
        ],
        # Rust
        '.rs': [
            r'use\s+([\w:]+)',
            r'extern\s+crate\s+([\w]+)',
        ],
        # Swift
        '.swift': [
            r'import\s+(\w+)',
        ],
        # Shell scripts
        '.sh': [
            r'source\s+[\'"]?([^\'"]+)[\'"]?',
            r'\.\s+[\'"]?([^\'"]+)[\'"]?',
        ],
        # Makefile
        'Makefile': [
            r'include\s+([^\s]+)',
        ],
    }

    # 첫 번째 단계: 모든 import 수집
    for file_path, content in file_contents:
        dependencies[file_path] = set()
        imports[file_path] = set()

        ext = os.path.splitext(file_path)[1].lower()
        basename = os.path.basename(file_path)

        # 적절한 패턴 선택
        patterns = []
        if ext in language_patterns:
            patterns = language_patterns[ext]
        elif basename in language_patterns:
            patterns = language_patterns[basename]

        # 모든 관련 패턴 적용
        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                imports[file_path].add(match)

    # 두 번째 단계: 파일 간 참조 관계 해결
    file_mapping = {}  # 가능한 이름과 파일 경로 간의 매핑 생성

    for file_path, _ in file_contents:
        basename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(basename)[0]

        # 파일 이름의 다양한 형태 추가
        file_mapping[basename] = file_path
        file_mapping[name_without_ext] = file_path
        file_mapping[file_path] = file_path

        # 폴더가 있는 경로의 경우 상대 경로 변형도 추가
        if os.path.dirname(file_path):
            rel_path = file_path
            while '/' in rel_path:
                rel_path = rel_path[rel_path.find('/')+1:]
                file_mapping[rel_path] = file_path
                file_mapping[os.path.splitext(rel_path)[0]] = file_path

    # import를 파일 의존성으로 변환
    for file_path, imported in imports.items():
        for imp in imported:
            # 알려진 파일과 import 일치 시도
            matched = False

            # import의 변형을 시도하여 매칭 찾기
            import_variations = [
                imp,
                os.path.basename(imp),
                os.path.splitext(imp)[0],
                imp.replace('.', '/'),
                imp.replace('.', '/') + '.py',  # Python용
                imp + '.h',  # C용
                imp + '.hpp',  # C++용
                imp + '.js',  # JS용
            ]

            for var in import_variations:
                if var in file_mapping:
                    dependencies[file_path].add(file_mapping[var])
                    matched = True
                    break

            # 일치하는 항목이 없으면 import를 그대로 유지
            if not matched:
                dependencies[file_path].add(imp)

    return dependencies