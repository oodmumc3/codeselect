#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_selector_updated.py - 리팩토링된 selector.py 모듈 테스트

리팩토링된 selector.py 모듈의 함수들을 테스트하는 코드입니다.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from filetree import Node
from selector import interactive_selection

class TestSelector(unittest.TestCase):
    """selector 모듈의 함수들을 테스트하는 클래스"""
    
    def setUp(self):
        """테스트 전에 파일 트리 구조를 설정합니다."""
        # 루트 노드 생성
        self.root_node = Node("test_root", True)
        
        # 디렉토리 추가
        dir1 = Node("dir1", True, self.root_node)
        dir2 = Node("dir2", True, self.root_node)
        self.root_node.children["dir1"] = dir1
        self.root_node.children["dir2"] = dir2
        
        # 파일 추가
        file1 = Node("file1.txt", False, self.root_node)
        file2 = Node("file2.py", False, dir1)
        file3 = Node("file3.md", False, dir2)
        
        self.root_node.children["file1.txt"] = file1
        dir1.children["file2.py"] = file2
        dir2.children["file3.md"] = file3
    
    @patch('curses.wrapper')
    def test_interactive_selection(self, mock_wrapper):
        """interactive_selection 함수가 올바르게 curses를 초기화하고 FileSelector를 실행하는지 테스트합니다."""
        # 모의 결과 설정
        file_selector_mock = MagicMock()
        file_selector_mock.run.return_value = True
        
        # mock_wrapper가 호출될 때 file_selector_mock.run을 반환하도록 설정
        mock_wrapper.side_effect = lambda func: func(MagicMock())
        
        # FileSelector 클래스 모의
        with patch('selector.FileSelector', return_value=file_selector_mock):
            # interactive_selection 함수 호출
            result = interactive_selection(self.root_node)
            
            # curses.wrapper가 호출되었는지 확인
            mock_wrapper.assert_called_once()
            
            # FileSelector가 생성되고 run 메서드가 호출되었는지 확인
            file_selector_mock.run.assert_called_once()
            
            # 결과가 올바른지 확인
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()