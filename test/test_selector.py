#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_selector.py - selector.py 모듈 테스트

selector.py 모듈의 클래스와 함수들을 테스트하는 코드입니다.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from filetree import Node, build_file_tree
from selector import FileSelector

class TestFileSelector(unittest.TestCase):
    """FileSelector 클래스를 테스트하는 클래스"""
    
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
        
        # curses 스크린 모의 객체 생성
        self.mock_stdscr = MagicMock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)  # 24행 80열의 화면
    
    @patch('curses.color_pair')
    @patch('curses.init_pair')
    @patch('curses.start_color')
    @patch('curses.use_default_colors')
    @patch('curses.curs_set')
    def test_initialize_curses(self, mock_curs_set, mock_use_default_colors, mock_start_color, mock_init_pair, mock_color_pair):
        """initialize_curses 메서드가 올바르게 curses를 초기화하는지 테스트합니다."""
        # FileSelector 인스턴스 생성
        selector = FileSelector(self.root_node, self.mock_stdscr)
        
        # curses 초기화 함수들이 호출되었는지 확인
        mock_start_color.assert_called_once()
        mock_use_default_colors.assert_called_once()
        mock_curs_set.assert_called_once_with(0)  # 커서 숨기기
        
        # 색상 쌍 초기화 확인
        self.assertEqual(mock_init_pair.call_count, 6)  # 6개의 색상 쌍
        
        # keypad 함수 호출 확인
        self.mock_stdscr.keypad.assert_called_once_with(True)
    
    @patch('curses.color_pair')
    @patch('curses.init_pair')
    @patch('curses.start_color')
    @patch('curses.use_default_colors')
    @patch('curses.curs_set')
    def test_update_dimensions(self, mock_curs_set, mock_use_default_colors, mock_start_color, mock_init_pair, mock_color_pair):
        """update_dimensions 메서드가 올바르게 화면 크기를 업데이트하는지 테스트합니다."""
        # FileSelector 인스턴스 생성
        selector = FileSelector(self.root_node, self.mock_stdscr)
        
        # 화면 크기 설정
        self.mock_stdscr.getmaxyx.return_value = (30, 100)  # 변경된 화면 크기
        
        # 크기 업데이트
        selector.update_dimensions()
        
        # 업데이트된 크기 확인
        self.assertEqual(selector.height, 30)
        self.assertEqual(selector.width, 100)
        self.assertEqual(selector.max_visible, 24)  # 30 - 6
    
    @patch('curses.color_pair')
    @patch('curses.init_pair')
    @patch('curses.start_color')
    @patch('curses.use_default_colors')
    @patch('curses.curs_set')
    def test_expand_all(self, mock_curs_set, mock_use_default_values, mock_start_color, mock_init_pair, mock_color_pair):
        """expand_all 메서드가 모든 디렉토리의 확장 상태를 올바르게 설정하는지 테스트합니다."""
        # FileSelector 인스턴스 생성
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        selector = FileSelector(self.root_node, mock_stdscr)
        
        # 모든 디렉토리 접기
        selector.expand_all(False)
        
        # 모든 디렉토리가 접혀있는지 확인
        self.assertFalse(self.root_node.expanded)
        for child_name, child in self.root_node.children.items():
            if child.is_dir:
                self.assertFalse(child.expanded)
        
        # 모든 디렉토리 펼치기
        selector.expand_all(True)
        
        # 모든 디렉토리가 펼쳐있는지 확인
        self.assertTrue(self.root_node.expanded)
        for child_name, child in self.root_node.children.items():
            if child.is_dir:
                self.assertTrue(child.expanded)
    
    @patch('curses.color_pair')
    @patch('curses.init_pair')
    @patch('curses.start_color')
    @patch('curses.use_default_colors')
    @patch('curses.curs_set')
    def test_select_all(self, mock_curs_set, mock_use_default_values, mock_start_color, mock_init_pair, mock_color_pair):
        """select_all 메서드가 모든 노드의 선택 상태를 올바르게 설정하는지 테스트합니다."""
        # FileSelector 인스턴스 생성
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        selector = FileSelector(self.root_node, mock_stdscr)
        
        # 모든 노드 선택 해제
        selector.select_all(False)
        
        # 모든 노드가 선택 해제되었는지 확인
        def check_selection_state(node, expected_state):
            self.assertEqual(node.selected, expected_state)
            if node.is_dir and node.children:
                for child in node.children.values():
                    check_selection_state(child, expected_state)
        
        check_selection_state(self.root_node, False)
        
        # 모든 노드 선택
        selector.select_all(True)
        
        # 모든 노드가 선택되었는지 확인
        check_selection_state(self.root_node, True)

if __name__ == '__main__':
    unittest.main()