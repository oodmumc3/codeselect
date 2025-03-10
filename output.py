#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeSelect - Output module

이 모듈은 선택된 파일 트리와 내용을 다양한 형식으로 출력하는 기능을 제공합니다.
다음 출력 형식을 지원합니다:
- txt: 기본 텍스트 형식
- md: 깃허브 호환 마크다운 형식
- llm: 언어 모델 최적화 형식
"""

import os

def write_file_tree_to_string(node, prefix='', is_last=True):
    """
    파일 트리 구조를 문자열로 변환합니다.
    
    Args:
        node: 현재 노드
        prefix: 들여쓰기 접두사
        is_last: 현재 노드가 부모의 마지막 자식인지 여부
        
    Returns:
        str: 파일 트리 문자열 표현
    """
    result = ""

    if node.parent is not None:  # 루트 노드는 건너뜀
        branch = "└── " if is_last else "├── "
        result += f"{prefix}{branch}{node.name}\n"

    if node.is_dir and node.children:
        items = sorted(node.children.items(),
                      key=lambda x: (not x[1].is_dir, x[0].lower()))

        for i, (_, child) in enumerate(items):
            is_last_child = i == len(items) - 1
            new_prefix = prefix + ('    ' if is_last else '│   ')
            result += write_file_tree_to_string(child, new_prefix, is_last_child)

    return result

def write_output_file(output_path, root_path, root_node, file_contents, output_format='txt', dependencies=None):
    """
    파일 트리와 선택된 내용을 출력 파일에 작성합니다.
    
    Args:
        output_path: 출력 파일 경로
        root_path: 프로젝트 루트 경로
        root_node: 파일 트리 루트 노드
        file_contents: 파일 내용 목록 [(경로, 내용), ...]
        output_format: 출력 형식 ('txt', 'md', 'llm')
        dependencies: 파일 간 의존성 정보 (llm 형식에 필요)
        
    Returns:
        str: 출력 파일 경로
    """
    if output_format == 'md':
        write_markdown_output(output_path, root_path, root_node, file_contents)
    elif output_format == 'llm':
        write_llm_optimized_output(output_path, root_path, root_node, file_contents, dependencies)
    else:
        # 기본 txt 형식
        with open(output_path, 'w', encoding='utf-8') as f:
            # 파일 트리 작성
            f.write("<file_map>\n")
            f.write(f"{root_path}\n")

            tree_str = write_file_tree_to_string(root_node)
            f.write(tree_str)

            f.write("</file_map>\n\n")

            # 파일 내용 작성
            f.write("<file_contents>\n")
            for path, content in file_contents:
                f.write(f"File: {path}\n")
                f.write("```")

                # 확장자를 통한 구문 강조 결정
                ext = os.path.splitext(path)[1][1:].lower()
                if ext:
                    f.write(ext)

                f.write("\n")
                f.write(content)
                if not content.endswith('\n'):
                    f.write('\n')
                f.write("```\n\n")

            f.write("</file_contents>\n")

    return output_path

def write_markdown_output(output_path, root_path, root_node, file_contents):
    """
    GitHub 호환 마크다운 형식으로 출력합니다.
    
    Args:
        output_path: 출력 파일 경로
        root_path: 프로젝트 루트 경로
        root_node: 파일 트리 루트 노드
        file_contents: 파일 내용 목록 [(경로, 내용), ...]
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        # 헤더 작성
        f.write(f"# Project Files: `{root_path}`\n\n")

        # 파일 구조 섹션 작성
        f.write("## 📁 File Structure\n\n")
        f.write("```\n")
        f.write(f"{root_path}\n")
        f.write(write_file_tree_to_string(root_node))
        f.write("```\n\n")

        # 파일 내용 섹션 작성
        f.write("## 📄 File Contents\n\n")

        for path, content in file_contents:
            f.write(f"### {path}\n\n")

            # 확장자 기반 구문 강조 추가
            ext = os.path.splitext(path)[1][1:].lower()
            f.write(f"```{ext}\n")
            f.write(content)
            if not content.endswith('\n'):
                f.write('\n')
            f.write("```\n\n")

def get_language_name(extension):
    """
    파일 확장자를 언어 이름으로 변환합니다.
    
    Args:
        extension: 파일 확장자
        
    Returns:
        str: 해당 확장자의 프로그래밍 언어 이름
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

def write_llm_optimized_output(output_path, root_path, root_node, file_contents, dependencies):
    """
    LLM 분석에 최적화된 형식으로 출력합니다.
    
    Args:
        output_path: 출력 파일 경로
        root_path: 프로젝트 루트 경로
        root_node: 파일 트리 루트 노드
        file_contents: 파일 내용 목록 [(경로, 내용), ...]
        dependencies: 파일 간 의존성 정보
    """
    # count_selected_files 함수를 모듈에서 임포트하지 않았기 때문에 필요한 함수를 정의
    def count_selected_files(node):
        """선택된 파일(디렉토리 제외)의 수를 계산합니다."""
        count = 0
        if not node.is_dir and node.selected:
            count = 1
        elif node.is_dir and node.children:
            for child in node.children.values():
                count += count_selected_files(child)
        return count
    
    # flatten_tree 함수를 모듈에서 임포트하지 않았기 때문에 필요한 함수를 정의
    def flatten_tree(node, visible_only=True):
        """트리를 네비게이션용 노드 리스트로 평탄화합니다."""
        flat_nodes = []

        def _traverse(node, level=0):
            if node.parent is not None:  # 루트 노드 제외
                flat_nodes.append((node, level))

            if node.is_dir and node.children and (not visible_only or node.expanded):
                # 디렉토리 먼저, 그다음 파일, 알파벳 순으로 정렬
                items = sorted(node.children.items(),
                              key=lambda x: (not x[1].is_dir, x[0].lower()))

                for _, child in items:
                    _traverse(child, level + 1)

        _traverse(node)
        return flat_nodes

    with open(output_path, 'w', encoding='utf-8') as f:
        # 헤더 및 개요
        f.write("# PROJECT ANALYSIS FOR AI ASSISTANT\n\n")

        # 프로젝트 일반 정보
        total_files = sum(1 for node, _ in flatten_tree(root_node) if not node.is_dir)
        selected_files = count_selected_files(root_node)
        f.write("## 📦 GENERAL INFORMATION\n\n")
        f.write(f"- **Project path**: `{root_path}`\n")
        f.write(f"- **Total files**: {total_files}\n")
        f.write(f"- **Files included in this analysis**: {selected_files}\n")

        # 사용된 언어 감지
        languages = {}
        for path, _ in file_contents:
            ext = os.path.splitext(path)[1].lower()
            if ext:
                ext = ext[1:]  # 점 제거
                languages[ext] = languages.get(ext, 0) + 1

        if languages:
            f.write("- **Main languages used**:\n")
            for ext, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]:
                lang_name = get_language_name(ext)
                f.write(f"  - {lang_name} ({count} files)\n")
        f.write("\n")

        # 프로젝트 구조
        f.write("## 🗂️ PROJECT STRUCTURE\n\n")
        f.write("```\n")
        f.write(f"{root_path}\n")
        f.write(write_file_tree_to_string(root_node))
        f.write("```\n\n")

        # 주요 디렉토리 및 컴포넌트
        main_dirs = [node for node, level in flatten_tree(root_node, False)
                    if node.is_dir and level == 1]

        if main_dirs:
            f.write("### 📂 Main Components\n\n")
            for dir_node in main_dirs:
                dir_files = [p for p, _ in file_contents if p.startswith(f"{dir_node.name}/")]
                f.write(f"- **`{dir_node.name}/`** - ")
                if dir_files:
                    f.write(f"Contains {len(dir_files)} files")

                    # 이 디렉토리의 언어들
                    dir_exts = {}
                    for path in dir_files:
                        ext = os.path.splitext(path)[1].lower()
                        if ext:
                            ext = ext[1:]
                            dir_exts[ext] = dir_exts.get(ext, 0) + 1

                    if dir_exts:
                        main_langs = [get_language_name(ext) for ext, _ in
                                     sorted(dir_exts.items(), key=lambda x: x[1], reverse=True)[:2]]
                        f.write(f" mainly in {', '.join(main_langs)}")

                f.write("\n")
            f.write("\n")

        # 파일 관계 그래프
        f.write("## 🔄 FILE RELATIONSHIPS\n\n")

        # 가장 많이 참조된 파일 찾기
        referenced_by = {}
        for file, deps in dependencies.items():
            for dep in deps:
                if isinstance(dep, str) and os.path.sep in dep:  # 파일 경로인 경우
                    if dep not in referenced_by:
                        referenced_by[dep] = []
                    referenced_by[dep].append(file)

        # 중요한 관계 표시
        if referenced_by:
            f.write("### Core Files (most referenced)\n\n")
            for file, refs in sorted(referenced_by.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
                if len(refs) > 1:  # 여러 번 참조된 파일만
                    f.write(f"- **`{file}`** is imported by {len(refs)} files\n")
            f.write("\n")

        # 파일별 의존성 표시
        f.write("### Dependencies by File\n\n")
        for file, deps in sorted(dependencies.items()):
            if deps:
                internal_deps = [d for d in deps if isinstance(d, str) and os.path.sep in d]
                external_deps = [d for d in deps if d not in internal_deps]

                f.write(f"- **`{file}`**:\n")

                if internal_deps:
                    f.write(f"  - *Internal dependencies*: ")
                    f.write(", ".join(f"`{d}`" for d in sorted(internal_deps)[:5]))
                    if len(internal_deps) > 5:
                        f.write(f" and {len(internal_deps)-5} more")
                    f.write("\n")

                if external_deps:
                    f.write(f"  - *External dependencies*: ")
                    f.write(", ".join(f"`{d}`" for d in sorted(external_deps)[:5]))
                    if len(external_deps) > 5:
                        f.write(f" and {len(external_deps)-5} more")
                    f.write("\n")
        f.write("\n")

        # 파일 내용
        f.write("## 📄 FILE CONTENTS\n\n")
        f.write("*Note: The content below includes only selected files.*\n\n")

        for path, content in file_contents:
            f.write(f"### {path}\n\n")

            # 파일 정보 추가 (가능한 경우)
            file_deps = dependencies.get(path, set())
            if file_deps:
                internal_deps = [d for d in file_deps if isinstance(d, str) and os.path.sep in d]
                external_deps = [d for d in file_deps if d not in internal_deps]

                if internal_deps or external_deps:
                    f.write("**Dependencies:**\n")

                    if internal_deps:
                        f.write("- Internal: " + ", ".join(f"`{d}`" for d in sorted(internal_deps)[:3]))
                        if len(internal_deps) > 3:
                            f.write(f" and {len(internal_deps)-3} more")
                        f.write("\n")

                    if external_deps:
                        f.write("- External: " + ", ".join(f"`{d}`" for d in sorted(external_deps)[:3]))
                        if len(external_deps) > 3:
                            f.write(f" and {len(external_deps)-3} more")
                        f.write("\n")

                    f.write("\n")

            # 확장자 기반 구문 강조
            ext = os.path.splitext(path)[1][1:].lower()
            f.write(f"```{ext}\n")
            f.write(content)
            if not content.endswith('\n'):
                f.write('\n')
            f.write("```\n\n")