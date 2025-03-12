#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selector_ui.py - File selection UI components

A module that provides UI components for file selection.
"""

import curses
import re
from filetree import flatten_tree, count_selected_files
from selector_actions import (
    toggle_selection, toggle_expand, select_all, 
    expand_all, apply_search_filter, toggle_current_dir_selection
)

class FileSelector:
    """
    Classes that provide an interactive file selection interface based on curses
    
    Provides a UI that allows the user to select a file from a file tree.
    """
    def __init__(self, root_node, stdscr):
        """
        Initialising the FileSelector Class
        
        Args:
            root_node (Node): The root node of the file tree
            stdscr (curses.window): curses window object
        """
        self.root_node = root_node
        self.stdscr = stdscr
        self.current_index = 0
        self.scroll_offset = 0
        self.visible_nodes = flatten_tree(root_node)
        self.max_visible = 0
        self.height, self.width = 0, 0
        self.copy_to_clipboard = True  # 기본값: 클립보드 복사 활성화
        
        # 검색 관련 변수
        self.search_mode = False
        self.search_query = ""
        self.search_buffer = ""
        self.case_sensitive = False
        self.filtered_nodes = []
        self.original_nodes = []  # 검색 전 노드 상태 저장
        
        self.initialize_curses()

    def initialize_curses(self):
        """Initialise curses settings."""
        curses.start_color()
        curses.use_default_colors()
        # 색상 쌍 정의
        curses.init_pair(1, curses.COLOR_GREEN, -1)    # 선택된 파일
        curses.init_pair(2, curses.COLOR_BLUE, -1)     # 디렉토리
        curses.init_pair(3, curses.COLOR_YELLOW, -1)   # 선택된 디렉토리
        curses.init_pair(4, curses.COLOR_WHITE, -1)    # 선택되지 않은 파일
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)  # 현재 선택
        curses.init_pair(6, curses.COLOR_RED, -1)      # 도움말 메시지
        curses.init_pair(7, curses.COLOR_CYAN, -1)     # 검색 모드 표시

        # 커서 숨기기
        curses.curs_set(0)

        # 특수 키 활성화
        self.stdscr.keypad(True)

        # 화면 크기 가져오기
        self.update_dimensions()

    def update_dimensions(self):
        """Update the screen size."""
        self.height, self.width = self.stdscr.getmaxyx()
        self.max_visible = self.height - 6  # 상단에 통계를 위한 라인 추가

    def expand_all(self, expand=True):
        """Expand or collapse all directories."""
        result = expand_all(self.root_node, expand)
        self.visible_nodes = result

    def toggle_current_dir_selection(self):
        """Toggles the selection status of only files in the current directory (no subdirectories)."""
        if self.current_index < len(self.visible_nodes):
            current_node, _ = self.visible_nodes[self.current_index]
            toggle_current_dir_selection(current_node)

    def toggle_search_mode(self):
        """Turn search mode on or off."""
        if self.search_mode:
            # 검색 모드 종료
            self.search_mode = False
            self.search_buffer = ""
            # 검색 결과 유지 (검색 취소 시에만 원래 목록으로 복원)
        else:
            # 검색 모드 시작
            self.search_mode = True
            self.search_buffer = ""
            if not self.original_nodes:
                self.original_nodes = self.visible_nodes

    def handle_search_input(self, ch):
        """Process input in search mode."""
        if ch == 27:  # ESC
            # 검색 모드 취소 및 원래 목록으로 복원
            self.search_mode = False
            self.search_buffer = ""
            self.search_query = ""
            self.visible_nodes = self.original_nodes if self.original_nodes else flatten_tree(self.root_node)
            self.original_nodes = []
            return True
        elif ch in (10, 13):  # Enter
            # 검색 실행
            self.search_mode = False  # 검색 모드 종료
            self.search_query = self.search_buffer
            self.apply_search_filter()
            return True
        elif ch == curses.KEY_BACKSPACE or ch == 127 or ch == 8:  # Backspace
            # 검색어에서 한 글자 삭제
            self.search_buffer = self.search_buffer[:-1]
            return True
        elif ch == ord('^'):  # ^ 키로 대소문자 구분 토글
            self.case_sensitive = not self.case_sensitive
            return True
        elif 32 <= ch <= 126:  # ASCII 문자
            # 검색어에 문자 추가
            self.search_buffer += chr(ch)
            return True
        return False

    def apply_search_filter(self):
        """Filter files based on search terms."""
        if not self.search_query:
            self.visible_nodes = self.original_nodes
            return

        success, error_message = apply_search_filter(
            self.search_query, 
            self.case_sensitive, 
            self.root_node, 
            self.original_nodes, 
            self.visible_nodes
        )
        
        if not success:
            self.stdscr.addstr(0, self.width - 25, error_message, curses.color_pair(6))
            self.stdscr.refresh()
            curses.napms(1000)
            return

    def handle_vim_navigation(self, ch):
        """Handles IM-style navigation keys."""
        if ch == ord('j'):  # 아래로 이동
            self.current_index = min(len(self.visible_nodes) - 1, self.current_index + 1)
            return True
        elif ch == ord('k'):  # 위로 이동
            self.current_index = max(0, self.current_index - 1)
            return True
        elif ch == ord('h'):  # 디렉토리 닫기 또는 부모로 이동
            if self.current_index < len(self.visible_nodes):
                node, _ = self.visible_nodes[self.current_index]
                if node.is_dir and node.expanded:
                    result = toggle_expand(node, self.search_mode, self.search_query, 
                                        self.original_nodes, self.apply_search_filter)
                    if result:
                        self.visible_nodes = result
                    return True
                elif node.parent and node.parent.parent:  # 부모로 이동 (루트 제외)
                    # 부모의 인덱스 찾기
                    for i, (n, _) in enumerate(self.visible_nodes):
                        if n == node.parent:
                            self.current_index = i
                            return True
        elif ch == ord('l'):  # 디렉토리 열기
            if self.current_index < len(self.visible_nodes):
                node, _ = self.visible_nodes[self.current_index]
                if node.is_dir and not node.expanded:
                    result = toggle_expand(node, self.search_mode, self.search_query, 
                                         self.original_nodes, self.apply_search_filter)
                    if result:
                        self.visible_nodes = result
                    return True
        return False

    def draw_tree(self):
        """Draw a file tree."""
        self.stdscr.clear()
        self.update_dimensions()

        # 검색 모드가 아니고 검색 쿼리도 없을 때만 노드 목록 업데이트
        if not self.search_mode and not self.search_query:
            self.visible_nodes = flatten_tree(self.root_node)

        # 범위 확인
        if self.current_index >= len(self.visible_nodes):
            self.current_index = len(self.visible_nodes) - 1
        if self.current_index < 0:
            self.current_index = 0

        # 필요시 스크롤 조정
        if self.current_index < self.scroll_offset:
            self.scroll_offset = self.current_index
        elif self.current_index >= self.scroll_offset + self.max_visible:
            self.scroll_offset = self.current_index - self.max_visible + 1

        # 1번째 줄에 통계 표시 (첫 번째 항목을 가리지 않도록)
        selected_count = count_selected_files(self.root_node)
        total_count = sum(1 for node, _ in flatten_tree(self.root_node) if not node.is_dir)
        visible_count = len([1 for node, _ in self.visible_nodes if not node.is_dir])

        # 검색 모드 상태 표시
        if self.search_mode or self.search_query:
            search_display = f"Search: {self.search_buffer if self.search_mode else self.search_query}"
            case_status = "Case-sensitive" if self.case_sensitive else "Ignore case"
            self.stdscr.addstr(0, 0, search_display, curses.color_pair(7) | curses.A_BOLD)
            self.stdscr.addstr(0, len(search_display) + 2, f"({case_status})", curses.color_pair(7))
            self.stdscr.addstr(0, self.width - 30, f"Show: {visible_count}/{total_count}", curses.A_BOLD)
            # 검색 모드에서도 선택된 파일 개수 표시
            self.stdscr.addstr(1, 0, f"Selected Files: {selected_count}/{total_count}", curses.A_BOLD)
        else:
            self.stdscr.addstr(0, 0, f"Selected Files: {selected_count}/{total_count}", curses.A_BOLD)

        # 1번째 줄부터 시작하여 보이는 노드 그리기
        for i, (node, level) in enumerate(self.visible_nodes[self.scroll_offset:self.scroll_offset + self.max_visible]):
            y = i + 1  # 1번째 줄부터 시작 (통계 아래)
            if y >= self.max_visible + 1:
                break

            # 유형 및 선택 상태에 따라 색상 결정
            if i + self.scroll_offset == self.current_index:
                # 활성 노드 (하이라이트)
                attr = curses.color_pair(5)
            elif node.is_dir:
                # 디렉토리
                attr = curses.color_pair(3) if node.selected else curses.color_pair(2)
            else:
                # 파일
                attr = curses.color_pair(1) if node.selected else curses.color_pair(4)

            # 표시할 줄 준비
            indent = "  " * level
            if node.is_dir:
                prefix = "+ " if node.expanded else "- "
            else:
                prefix = "✓ " if node.selected else "☐ "

            # 이름이 너무 길면 잘라내기
            name_space = self.width - len(indent) - len(prefix) - 2
            name_display = node.name[:name_space] + ("..." if len(node.name) > name_space else "")

            # 줄 표시
            self.stdscr.addstr(y, 0, f"{indent}{prefix}{name_display}", attr)

        # 화면 하단에 도움말 표시
        help_y = self.height - 5
        self.stdscr.addstr(help_y, 0, "━" * self.width)
        help_y += 1
        if self.search_mode:
            self.stdscr.addstr(help_y, 0, "Search mode: type and press Enter to execute search, ESC to cancel, ^ to toggle case", curses.color_pair(7))
        else:
            self.stdscr.addstr(help_y, 0, "↑/↓/j/k: Navigate SPACE: Select ←/→/h/l: Close/open folder /: Search", curses.color_pair(6))
        help_y += 1
        self.stdscr.addstr(help_y, 0, "T: Toggle current folder only E: Expand all C: Collapse all", curses.color_pair(6))
        help_y += 1
        clip_status = "ON" if self.copy_to_clipboard else "OFF"
        self.stdscr.addstr(help_y, 0, f"A: Select all N: Deselect all B: Clipboard ({clip_status})  X: Cancel  D: Complete", curses.color_pair(6))

        self.stdscr.refresh()

    def process_key(self, key):
        """키 입력을 처리합니다."""
        # 검색 모드일 때는 검색 입력 처리
        if self.search_mode:
            return self.handle_search_input(key)
            
        # ESC 키는 run() 메서드에서 특별 처리
        if key == 27:  # ESC
            return False
            
        # 검색 모드 진입
        if key == ord('/'):
            self.toggle_search_mode()
            return True
            
        # Vim 스타일 네비게이션 처리
        if self.handle_vim_navigation(key):
            return True
            
        # 화살표 키 처리
        if key == curses.KEY_UP:
            # 위로 이동
            self.current_index = max(0, self.current_index - 1)
            return True
        elif key == curses.KEY_DOWN:
            # 아래로 이동
            self.current_index = min(len(self.visible_nodes) - 1, self.current_index + 1)
            return True
        elif key == curses.KEY_RIGHT:
            # 디렉토리 열기
            if self.current_index < len(self.visible_nodes):
                node, _ = self.visible_nodes[self.current_index]
                if node.is_dir and not node.expanded:
                    result = toggle_expand(node, self.search_mode, self.search_query, 
                                         self.original_nodes, self.apply_search_filter)
                    if result:
                        self.visible_nodes = result
                    # 검색 모드에서는 필터링 다시 적용
                    if self.search_query:
                        self.apply_search_filter()
                    return True
        elif key == curses.KEY_LEFT:
            # 디렉토리 닫기
            if self.current_index < len(self.visible_nodes):
                node, _ = self.visible_nodes[self.current_index]
                if node.is_dir and node.expanded:
                    result = toggle_expand(node, self.search_mode, self.search_query, 
                                         self.original_nodes, self.apply_search_filter)
                    if result:
                        self.visible_nodes = result
                    # 검색 모드에서는 필터링 다시 적용
                    if self.search_query:
                        self.apply_search_filter()
                    return True
                elif node.parent and node.parent.parent:  # 부모로 이동 (루트 제외)
                    # 부모의 인덱스 찾기
                    for i, (n, _) in enumerate(self.visible_nodes):
                        if n == node.parent:
                            self.current_index = i
                            return True
        elif key == ord(' '):
            # 선택 전환 (검색 모드에서도 작동하도록 함)
            if self.current_index < len(self.visible_nodes):
                node, _ = self.visible_nodes[self.current_index]
                toggle_selection(node)
                return True
        elif key in [ord('a'), ord('A')]:
            # 모두 선택
            select_all(self.root_node, True)
            return True
        elif key in [ord('n'), ord('N')]:
            # 모두 선택 해제
            select_all(self.root_node, False)
            return True
        elif key in [ord('e'), ord('E')]:
            # 모두 확장
            self.expand_all(True)
            return True
        elif key in [ord('c'), ord('C')]:
            # 모두 접기
            self.expand_all(False)
            return True
        elif key in [ord('t'), ord('T')]:
            # 현재 디렉토리만 선택 전환
            self.toggle_current_dir_selection()
            return True
        elif key in [ord('b'), ord('B')]:  # 'c'에서 'b'로 변경 (클립보드)
            # 클립보드 전환
            self.copy_to_clipboard = not self.copy_to_clipboard
            return True
        elif key in [ord('x'), ord('X'), 27]:  # 27 = ESC
            # ESC는 검색 모드에서만 처리하므로 여기서는 종료로 처리
            return False
        elif key in [ord('d'), ord('D'), 10, 13]:  # 10, 13 = Enter
            # 검색 모드가 아닐 때만 완료로 처리
            return False
            
        return True

    def run(self):
        """Launch the selection interface."""
        while True:
            self.draw_tree()
            key = self.stdscr.getch()
            
            # ESC 키 특별 처리: 검색 모드일 때와 검색 결과가 있을 때
            if key == 27:  # 27 = ESC
                if self.search_mode:
                    # 검색 모드 취소
                    self.search_mode = False
                    self.search_buffer = ""
                    if self.search_query:
                        # 이전 검색 결과는 유지
                        pass
                    else:
                        # 원래 목록으로 복원
                        self.visible_nodes = self.original_nodes if self.original_nodes else flatten_tree(self.root_node)
                        self.original_nodes = []
                elif self.search_query:
                    # 검색 결과가 있는 상태에서 ESC - 전체 목록으로 복원
                    self.search_query = ""
                    self.visible_nodes = self.original_nodes if self.original_nodes else flatten_tree(self.root_node)
                    self.original_nodes = []
                else:
                    # 일반 상태에서의 ESC - 종료
                    return False
                continue
            
            # 키 처리 결과에 따라 분기
            if key == curses.KEY_RESIZE:
                # 창 크기 변경 처리
                self.update_dimensions()
                continue
            
            # 키 처리
            key_handled = self.process_key(key)
            
            # 종료 조건
            if not key_handled:
                if key in [ord('x'), ord('X')]:
                    # 저장하지 않고 종료
                    return False
                elif key in [ord('d'), ord('D'), 10, 13]:  # 10, 13 = Enter
                    # 완료
                    return True

        return True