#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

# 테스트를 위한 더미 노드 클래스 선언
class Node:
    def __init__(self, name, is_dir=False, level=0, parent=None):
        self.name = name
        self.is_dir = is_dir
        self.level = level
        self.parent = parent
        self.children = []
        self.selected = False
        self.expanded = True
        self.path = name

    def add_child(self, child):
        self.children.append(child)
        return child

# 파일 선택기 클래스 임포트
# 실제 테스트에서는 아래 주석을 해제하고 사용합니다
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from selector import FileSelector, interactive_selection

# 테스트용으로 임시 임포트
# from selector import FileSelector, interactive_selection

class TestFileSelector(unittest.TestCase):
    """
    FileSelector 클래스 테스트
    """
    
    def setUp(self):
        """
        테스트용 파일 트리 생성
        
        구조:
        root/
        ├── folder1/
        │   ├── file1.txt
        │   └── file2.py
        └── folder2/
            ├── file3.txt
            └── subfolder/
                └── file4.js
        """
        self.root = Node("root", is_dir=True)
        
        # folder1과 파일들
        folder1 = self.root.add_child(Node("folder1", is_dir=True, level=1, parent=self.root))
        folder1.add_child(Node("file1.txt", level=2, parent=folder1))
        folder1.add_child(Node("file2.py", level=2, parent=folder1))
        
        # folder2와 파일들
        folder2 = self.root.add_child(Node("folder2", is_dir=True, level=1, parent=self.root))
        folder2.add_child(Node("file3.txt", level=2, parent=folder2))
        
        subfolder = folder2.add_child(Node("subfolder", is_dir=True, level=2, parent=folder2))
        subfolder.add_child(Node("file4.js", level=3, parent=subfolder))
        
        # 목 함수를 사용해 flatten_tree의 동작 재현
        self.flat_nodes = []
        self._flatten_helper(self.root)
        
        # FileSelector 인스턴스 생성
        self.selector = FileSelector(self.root, "테스트 선택기")
        # flat_nodes 속성 설정 (실제로는 refresh_flat_nodes()에서 생성됨)
        self.selector.flat_nodes = self.flat_nodes
    
    def _flatten_helper(self, node):
        """
        테스트용 파일 트리 평면화 함수
        """
        if node.is_dir:
            self.flat_nodes.append(node)
            if node.expanded:
                for child in node.children:
                    self._flatten_helper(child)
        else:
            self.flat_nodes.append(node)
    
    def test_init(self):
        """초기화 테스트"""
        self.assertEqual(self.selector.root_node, self.root)
        self.assertEqual(self.selector.title, "테스트 선택기")
        self.assertEqual(self.selector.cursor_index, 0)
        self.assertFalse(self.selector.search_mode)
        self.assertTrue(self.selector.clipboard_enabled)
    
    def test_move_cursor(self):
        """커서 이동 테스트"""
        # 초기 커서 위치
        self.assertEqual(self.selector.cursor_index, 0)
        
        # 아래로 이동
        self.selector.move_cursor(1)
        self.assertEqual(self.selector.cursor_index, 1)
        
        # 다시 아래로 이동
        self.selector.move_cursor(1)
        self.assertEqual(self.selector.cursor_index, 2)
        
        # 위로 이동
        self.selector.move_cursor(-1)
        self.assertEqual(self.selector.cursor_index, 1)
    
    def test_toggle_node_selected(self):
        """노드 선택 토글 테스트"""
        # 파일 선택
        self.selector.cursor_index = 2  # file1.txt 노드
        self.assertFalse(self.flat_nodes[2].selected)
        
        # 선택 토글
        self.selector.toggle_node_selected()
        self.assertTrue(self.flat_nodes[2].selected)
        
        # 다시 토글하여 선택 해제
        self.selector.toggle_node_selected()
        self.assertFalse(self.flat_nodes[2].selected)
    
    def test_toggle_directory_expanded(self):
        """디렉토리 확장/축소 토글 테스트"""
        # folder1 선택
        self.selector.cursor_index = 1  # folder1 노드
        self.assertTrue(self.flat_nodes[1].expanded)
        
        # 축소 토글
        with patch.object(self.selector, 'refresh_flat_nodes') as mock_refresh:
            self.selector.toggle_directory_expanded()
            self.assertFalse(self.flat_nodes[1].expanded)
            mock_refresh.assert_called_once()
    
    def test_toggle_all_selected(self):
        """모든 파일 선택/해제 테스트"""
        # 모든 파일이 선택되지 않은 상태 확인
        for node in self.flat_nodes:
            if not node.is_dir:
                self.assertFalse(node.selected)
        
        # 모두 선택
        self.selector.toggle_all_selected(True)
        
        # 모든 파일이 선택된 상태 확인
        for node in self.flat_nodes:
            if not node.is_dir:
                self.assertTrue(node.selected, f"{node.name} 선택되지 않음")
        
        # 모두 해제
        self.selector.toggle_all_selected(False)
        
        # 모든 파일이 선택 해제된 상태 확인
        for node in self.flat_nodes:
            if not node.is_dir:
                self.assertFalse(node.selected)
    
    def test_toggle_clipboard(self):
        """클립보드 활성화/비활성화 토글 테스트"""
        self.assertTrue(self.selector.clipboard_enabled)
        
        # 클립보드 비활성화
        self.selector.toggle_clipboard()
        self.assertFalse(self.selector.clipboard_enabled)
        
        # 클립보드 다시 활성화
        self.selector.toggle_clipboard()
        self.assertTrue(self.selector.clipboard_enabled)
    
    def test_process_normal_key(self):
        """일반 모드에서 키 입력 처리 테스트"""
        # 모의 curses 키 코드
        KEY_UP = 259
        KEY_DOWN = 258
        KEY_SPACE = 32
        KEY_ENTER = 10
        KEY_ESC = 27
        
        # 위로 이동 키
        with patch.object(self.selector, 'move_cursor') as mock_move:
            self.selector.process_normal_key(KEY_UP)
            mock_move.assert_called_once_with(-1)
        
        # 아래로 이동 키
        with patch.object(self.selector, 'move_cursor') as mock_move:
            self.selector.process_normal_key(KEY_DOWN)
            mock_move.assert_called_once_with(1)
        
        # 선택 토글 키
        with patch.object(self.selector, 'toggle_node_selected') as mock_toggle:
            self.selector.process_normal_key(KEY_SPACE)
            mock_toggle.assert_called_once()
        
        # 완료 키
        result = self.selector.process_normal_key(KEY_ENTER)
        self.assertTrue(result)
        
        # 취소 키
        result = self.selector.process_normal_key(KEY_ESC)
        self.assertFalse(result)
    
    def test_search_mode(self):
        """검색 모드 테스트"""
        # 검색 모드 시작
        with patch.object(self.selector, 'refresh_flat_nodes') as mock_refresh:
            self.selector.search_mode = True
            self.selector.search_term = "file"
            
            # 검색어 추가
            self.selector.process_search_key(ord('1'))
            self.assertEqual(self.selector.search_term, "file1")
            mock_refresh.assert_called_once_with("file1")
            
            # 백스페이스 처리
            mock_refresh.reset_mock()
            self.selector.process_search_key(127)  # Backspace 키
            self.assertEqual(self.selector.search_term, "file")
            mock_refresh.assert_called_once()
            
            # 검색 완료
            self.selector.process_search_key(10)  # Enter 키
            self.assertFalse(self.selector.search_mode)
    
    @patch('curses.wrapper')
    def test_interactive_selection(self, mock_wrapper):
        """대화형 선택 함수 테스트"""
        # curses.wrapper 함수가 True를 반환하도록 설정
        mock_wrapper.return_value = True
        
        # 대화형 선택 함수 호출
        result = interactive_selection(self.root, "테스트 타이틀")
        
        # curses.wrapper가 호출됐는지 확인
        mock_wrapper.assert_called_once()
        
        # 결과가 예상대로인지 확인
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()