#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeSelect - CLI module

명령행 인터페이스(CLI) 관련 기능을 담당하는 모듈입니다.
사용자의 명령행 인수를 처리하고 적절한 함수를 호출합니다.
"""

import os
import sys
import argparse

# 다른 모듈 임포트
import utils
import filetree
import selector
import output
import dependency

__version__ = "1.0.0"

def parse_arguments():
    """
    Parses command-line arguments.
    
    Returns:
        argparse.Namespace: the parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=f"CodeSelect v{__version__} - Select files to share with AI assistants"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to scan (default: current directory)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: based on directory name)"
    )
    parser.add_argument(
        "--format",
        choices=["txt", "md", "llm"],
        default="llm",
        help="Output format (default: llm - optimized for LLMs)"
    )
    parser.add_argument(
        "--skip-selection",
        action="store_true",
        help="Skip the selection interface and include all files"
    )
    parser.add_argument(
        "--no-clipboard",
        action="store_true",
        help="Disable automatic copy to clipboard"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information"
    )

    return parser.parse_args()

def main():
    """
    Main Function - The entry point for the CodeSelect program.
    
    Returns:
        int: the programme exit code (0: normal exit, 1: error).
    """
    args = parse_arguments()

    # 버전 정보 표시
    if args.version:
        print(f"CodeSelect v{__version__}")
        return 0

    # 디렉토리 경로 확인
    root_path = os.path.abspath(args.directory)
    if not os.path.isdir(root_path):
        print(f"Error: {root_path} is not a valid directory")
        return 1

    # 출력 파일 이름 생성
    if not args.output:
        args.output = utils.generate_output_filename(root_path, args.format)

    # 디렉토리 스캔
    print(f"Scanning directory: {root_path}")
    root_node = filetree.build_file_tree(root_path)

    # 파일 선택 처리
    proceed = True
    if not args.skip_selection:
        # 대화형 선택 인터페이스 실행
        try:
            proceed = selector.interactive_selection(root_node)
            if not proceed:
                print("Selection cancelled. Exiting without saving.")
                return 0
        except Exception as e:
            print(f"Error in selection interface: {e}")
            return 1

    # 선택된 파일 수 확인
    selected_count = filetree.count_selected_files(root_node)
    print(f"\nSelected files: {selected_count}")

    # 선택된 파일이 없으면 종료
    if selected_count == 0:
        print("No files selected. Exiting.")
        return 0

    # 선택된 파일 내용 수집
    file_contents = filetree.collect_selected_content(root_node, root_path)
    print(f"Collected content from {len(file_contents)} files.")

    # 의존성 분석 (LLM 형식인 경우)
    if args.format == 'llm':
        print("Analyzing file relationships...")
        all_files = filetree.collect_all_content(root_node, root_path)
        dependencies = dependency.analyze_dependencies(root_path, all_files)

        # 의존성 정보와 함께 출력 작성
        output_path = output.write_output_file(
            args.output, root_path, root_node, file_contents, args.format, dependencies
        )
    else:
        # 의존성 정보 없이 출력 작성
        output_path = output.write_output_file(
            args.output, root_path, root_node, file_contents, args.format
        )

    print(f"\nOutput written to: {output_path}")

    # 클립보드 복사 (활성화된 경우)
    if not args.no_clipboard:
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if utils.try_copy_to_clipboard(content):
                print("Content copied to clipboard.")
            else:
                print("Could not copy to clipboard (missing dependencies).")
        except Exception as e:
            print(f"Error copying to clipboard: {e}")

    return 0

if __name__ == "__main__":
    sys.exit(main())