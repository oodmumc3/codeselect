#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cli.py 모듈에 대한 테스트 코드
"""

import os
import sys
import unittest
import tempfile
from unittest.mock import patch, MagicMock

# 테스트 대상 모듈 임포트
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cli

class TestCLI(unittest.TestCase):
    """cli.py 모듈의 함수들을 테스트하는 클래스"""

    def setUp(self):
        """테스트 준비"""
        self.temp_dir = tempfile.mkdtemp()
        
        # 테스트용 임시 디렉토리에 파일 생성
        with open(os.path.join(self.temp_dir, "test.py"), "w") as f:
            f.write("print('Hello, world!')")

    def tearDown(self):
        """테스트 정리 - 임시 파일 삭제"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_parse_arguments(self):
        """parse_arguments 함수 테스트"""
        # 명령행 인수를 모의로 설정
        test_args = ["codeselect", self.temp_dir, "--format", "md", "--no-clipboard"]
        
        with patch('sys.argv', test_args):
            args = cli.parse_arguments()
            
            # 인수가 올바르게 파싱되었는지 확인
            self.assertEqual(args.directory, self.temp_dir)
            self.assertEqual(args.format, "md")
            self.assertTrue(args.no_clipboard)
            self.assertFalse(args.skip_selection)
            self.assertFalse(args.version)

    def test_main_version_flag(self):
        """main 함수의 --version 플래그 처리 테스트"""
        # --version 플래그를 설정
        with patch('sys.argv', ["codeselect", "--version"]):
            with patch('builtins.print') as mock_print:
                exit_code = cli.main()
                
                # 종료 코드가 0인지 확인
                self.assertEqual(exit_code, 0)
                
                # 버전 정보가 출력되었는지 확인
                mock_print.assert_called_once_with(f"CodeSelect v{cli.__version__}")

    def test_main_invalid_directory(self):
        """main 함수의 잘못된 디렉토리 처리 테스트"""
        # 존재하지 않는 디렉토리를 인수로 지정
        with patch('sys.argv', ["codeselect", "/nonexistent/directory"]):
            with patch('builtins.print') as mock_print:
                exit_code = cli.main()
                
                # 종료 코드가 1인지 확인
                self.assertEqual(exit_code, 1)
                
                # 오류 메시지가 출력되었는지 확인
                mock_print.assert_called_with(f"Error: {os.path.abspath('/nonexistent/directory')} is not a valid directory")

    @patch('filetree.build_file_tree')
    @patch('selector.interactive_selection')
    @patch('filetree.count_selected_files')
    @patch('filetree.collect_selected_content')
    @patch('filetree.collect_all_content')
    @patch('dependency.analyze_dependencies')
    @patch('output.write_output_file')
    @patch('utils.try_copy_to_clipboard')
    def test_main_normal_flow(self, mock_clipboard, mock_write_output, mock_analyze_dep,
                           mock_collect_all, mock_collect_selected, mock_count_files,
                           mock_selection, mock_build_tree):
        """main 함수의 정상 실행 흐름 테스트"""
        # 모의 객체 설정
        mock_root_node = MagicMock()
        mock_build_tree.return_value = mock_root_node
        mock_selection.return_value = True
        mock_count_files.return_value = 2
        mock_collect_selected.return_value = [("file1.py", "content1"), ("file2.py", "content2")]
        mock_collect_all.return_value = [("file1.py", "content1"), ("file2.py", "content2")]
        mock_analyze_dep.return_value = {"file1.py": set(), "file2.py": set()}
        mock_write_output.return_value = os.path.join(self.temp_dir, "output.txt")
        mock_clipboard.return_value = True
        
        # 임시 파일 생성
        output_path = os.path.join(self.temp_dir, "output.txt")
        with open(output_path, "w") as f:
            f.write("test content")
        
        # 명령행 인수 설정
        with patch('sys.argv', ["codeselect", self.temp_dir, "-o", output_path]):
            with patch('builtins.open', unittest.mock.mock_open(read_data="test content")):
                exit_code = cli.main()
                
                # 종료 코드가 0인지 확인
                self.assertEqual(exit_code, 0)
                
                # 각 함수가 적절하게 호출되었는지 확인
                mock_build_tree.assert_called_once_with(self.temp_dir)
                mock_selection.assert_called_once_with(mock_root_node)
                mock_count_files.assert_called_with(mock_root_node)
                mock_collect_selected.assert_called_with(mock_root_node, self.temp_dir)
                mock_collect_all.assert_called_with(mock_root_node, self.temp_dir)
                mock_analyze_dep.assert_called_with(self.temp_dir, mock_collect_all.return_value)
                mock_write_output.assert_called_with(
                    output_path, self.temp_dir, mock_root_node, 
                    mock_collect_selected.return_value, "llm", mock_analyze_dep.return_value
                )
                mock_clipboard.assert_called_with("test content")

if __name__ == "__main__":
    unittest.main()