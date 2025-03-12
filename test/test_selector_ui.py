#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_selector_ui.py - selector_ui.py 모듈 테스트

selector_ui.py 모듈의 클래스와 메서드들을 테스트하는 코드입니다.
"""

import os
import sys
import unittest
import curses
from unittest.mock import patch, MagicMock
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from filetree import Node
from selector_ui import FileSelector

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
        self.assertEqual(mock_init_pair.call_count, 7)  # 7개의 색상 쌍
        
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
    @patch('selector_ui.toggle_expand')
    def test_handle_vim_navigation(self, mock_toggle_expand, mock_curs_set, mock_use_default_colors, mock_start_color, mock_init_pair, mock_color_pair):
        """handle_vim_navigation 메서드가 vim 스타일 네비게이션 키를 올바르게 처리하는지 테스트합니다."""
        # FileSelector 인스턴스 생성
        selector = FileSelector(self.root_node, self.mock_stdscr)
        
        # j 키 (아래로 이동)
        result = selector.handle_vim_navigation(ord('j'))
        self.assertTrue(result)
        self.assertEqual(selector.current_index, 1)  # 인덱스가 1 증가
        
        # k 키 (위로 이동)
        result = selector.handle_vim_navigation(ord('k'))
        self.assertTrue(result)
        self.assertEqual(selector.current_index, 0)  # 인덱스가 다시 0으로 감소
        
        # 현재 노드 설정
        dir_node = None
        for node, level in selector.visible_nodes:
            if node.is_dir:
                dir_node = node
                break
        
        if dir_node:
            # 디렉토리 노드를 현재 선택으로 설정
            selector.visible_nodes = [(dir_node, 0)]
            selector.current_index = 0
            
            # l 키 (디렉토리 열기)
            dir_node.expanded = False  # 우선 닫은 상태로 설정
            mock_toggle_expand.return_value = selector.visible_nodes
            result = selector.handle_vim_navigation(ord('l'))
            self.assertTrue(result)
            mock_toggle_expand.assert_called_once()
    
    @patch('curses.color_pair')
    @patch('curses.init_pair')
    @patch('curses.start_color')
    @patch('curses.use_default_colors')
    @patch('curses.curs_set')
    def test_toggle_search_mode(self, mock_curs_set, mock_use_default_colors, mock_start_color, mock_init_pair, mock_color_pair):
        """toggle_search_mode 메서드가 검색 모드를 올바르게 전환하는지 테스트합니다."""
        # FileSelector 인스턴스 생성
        selector = FileSelector(self.root_node, self.mock_stdscr)
        
        # 초기 상태 확인
        self.assertFalse(selector.search_mode)
        self.assertEqual(selector.search_buffer, "")
        
        # 검색 모드 활성화
        selector.toggle_search_mode()
        
        # 검색 모드가 활성화되었는지 확인
        self.assertTrue(selector.search_mode)
        self.assertEqual(selector.search_buffer, "")
        self.assertEqual(selector.original_nodes, selector.visible_nodes)
        
        # 검색 모드 비활성화
        selector.toggle_search_mode()
        
        # 검색 모드가 비활성화되었는지 확인
        self.assertFalse(selector.search_mode)
        self.assertEqual(selector.search_buffer, "")
    
    @patch('curses.color_pair')
    @patch('curses.init_pair')
    @patch('curses.start_color')
    @patch('curses.use_default_colors')
    @patch('curses.curs_set')
    @patch('curses.napms')
    @patch('selector_ui.apply_search_filter')
    def test_apply_search_filter(self, mock_apply_search_filter, mock_napms, mock_curs_set, mock_use_default_colors, mock_start_color, mock_init_pair, mock_color_pair):
        """apply_search_filter 메서드가 검색 필터를 올바르게 적용하는지 테스트합니다."""
        # FileSelector 인스턴스 생성
        selector = FileSelector(self.root_node, self.mock_stdscr)
        
        # 검색 쿼리 설정
        selector.search_query = "test"
        selector.original_nodes = []
        
        # apply_search_filter 모의 함수 설정
        mock_apply_search_filter.return_value = (True, "")
        
        # 검색 필터 적용
        selector.apply_search_filter()
        
        # apply_search_filter 함수가 호출되었는지 확인
        mock_apply_search_filter.assert_called_once_with(
            "test", 
            False, 
            selector.root_node, 
            selector.original_nodes, 
            selector.visible_nodes
        )
        
        # 오류 발생 시나리오 테스트
        mock_apply_search_filter.reset_mock()
        mock_apply_search_filter.return_value = (False, "검색 결과 없음")
        
        # 검색 필터 적용
        selector.apply_search_filter()
        
        # 오류 메시지가 표시되었는지 확인
        self.mock_stdscr.addstr.assert_called_with(0, selector.width - 25, "검색 결과 없음", mock_color_pair.return_value)
        self.mock_stdscr.refresh.assert_called_once()

    @patch('curses.color_pair')
    @patch('curses.init_pair')
    @patch('curses.start_color')
    @patch('curses.use_default_colors')
    @patch('curses.curs_set')
    def test_handle_search_input(self, mock_curs_set, mock_use_default_colors, mock_start_color, mock_init_pair, mock_color_pair):
        """handle_search_input 메서드가 검색 입력을 올바르게 처리하는지 테스트합니다."""
        # FileSelector 인스턴스 생성
        selector = FileSelector(self.root_node, self.mock_stdscr)
        selector.search_mode = True
        
        # ESC 키 (검색 취소)
        result = selector.handle_search_input(27)
        self.assertTrue(result)
        self.assertFalse(selector.search_mode)
        self.assertEqual(selector.search_buffer, "")
        self.assertEqual(selector.search_query, "")
        
        # 검색 모드 다시 활성화
        selector.search_mode = True
        selector.search_buffer = "test"
        
        # Enter 키 (검색 실행)
        with patch.object(selector, 'apply_search_filter') as mock_apply_search:
            result = selector.handle_search_input(10)  # Enter 키
            self.assertTrue(result)
            self.assertFalse(selector.search_mode)
            self.assertEqual(selector.search_query, "test")
            mock_apply_search.assert_called_once()
        
        # 검색 모드 다시 활성화
        selector.search_mode = True
        selector.search_buffer = "test"
        
        # Backspace 키 (문자 삭제)
        result = selector.handle_search_input(8)  # Backspace 키
        self.assertTrue(result)
        self.assertEqual(selector.search_buffer, "tes")
        
        # ^ 키 (대소문자 구분 토글)
        result = selector.handle_search_input(ord('^'))
        self.assertTrue(result)
        self.assertTrue(selector.case_sensitive)
        
        # 일반 문자 키 (문자 추가)
        result = selector.handle_search_input(ord('a'))
        self.assertTrue(result)
        self.assertEqual(selector.search_buffer, "tesa")
        
        # 지원되지 않는 키
        result = selector.handle_search_input(255)  # 지원되지 않는 키
        self.assertFalse(result)

    @patch('curses.color_pair')
    @patch('curses.init_pair')
    @patch('curses.start_color')
    @patch('curses.use_default_colors')
    @patch('curses.curs_set')
    @patch('selector_ui.toggle_selection')
    @patch('selector_ui.select_all')
    def test_process_key(self, mock_select_all, mock_toggle_selection, mock_curs_set, mock_use_default_colors, mock_start_color, mock_init_pair, mock_color_pair):
        """process_key 메서드가 키 입력을 올바르게 처리하는지 테스트합니다."""
        # FileSelector 인스턴스 생성
        selector = FileSelector(self.root_node, self.mock_stdscr)
        
        # 검색 모드에서의 키 처리 테스트
        selector.search_mode = True
        with patch.object(selector, 'handle_search_input', return_value=True) as mock_handle_search:
            result = selector.process_key(ord('a'))
            self.assertTrue(result)
            mock_handle_search.assert_called_once_with(ord('a'))
        
        # 일반 모드로 변경
        selector.search_mode = False
        
        # / 키 (검색 모드 진입)
        with patch.object(selector, 'toggle_search_mode') as mock_toggle_search:
            result = selector.process_key(ord('/'))
            self.assertTrue(result)
            mock_toggle_search.assert_called_once()
        
        # Vim 스타일 네비게이션 테스트
        with patch.object(selector, 'handle_vim_navigation', return_value=True) as mock_vim_nav:
            result = selector.process_key(ord('j'))
            self.assertTrue(result)
            mock_vim_nav.assert_called_once_with(ord('j'))
        
        # 화살표 키 테스트 (위로 이동)
        with patch('curses.KEY_UP', 259):
            result = selector.process_key(curses.KEY_UP)
            self.assertTrue(result)
            self.assertEqual(selector.current_index, 0)  # 이미 0이므로 변경 없음
        
        # 화살표 키 테스트 (아래로 이동)
        with patch('curses.KEY_DOWN', 258):
            result = selector.process_key(curses.KEY_DOWN)
            self.assertTrue(result)
            self.assertEqual(selector.current_index, 1)  # 1로 증가
        
        # 공백 키 (선택 토글)
        if selector.visible_nodes and len(selector.visible_nodes) > 0:
            node, _ = selector.visible_nodes[selector.current_index]
            result = selector.process_key(ord(' '))
            self.assertTrue(result)
            mock_toggle_selection.assert_called_once_with(node)
        
        # 'a' 키 (모두 선택)
        result = selector.process_key(ord('a'))
        self.assertTrue(result)
        mock_select_all.assert_called_once_with(selector.root_node, True)
        
        # 종료 키 테스트
        result = selector.process_key(ord('x'))
        self.assertFalse(result)
        
        result = selector.process_key(ord('d'))
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()