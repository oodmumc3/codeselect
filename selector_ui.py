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
        self.search_input_str = ""  # Stores the raw string the user types for the search
        self.search_patterns_list = []  # Stores the list of processed patterns
        self.search_buffer = ""     # Live buffer for typing search query
        self.case_sensitive = False
        # self.filtered_nodes = [] # This seems unused, consider removing if not needed later
        self.original_nodes = []  # 검색 전 노드 상태 저장
        self.search_had_no_results = False # Flag for "검색 결과 없음"
        
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
            # Do not clear self.search_buffer here, it might be needed if user re-enters search mode
            # Do not clear self.search_input_str or self.search_patterns_list here.
        else:
            # 검색 모드 시작
            self.search_mode = True
            if self.search_input_str: # If there was a previous search query
                self.search_buffer = self.search_input_str # Initialize buffer with it
            else:
                self.search_buffer = "" # Start with an empty buffer

            if not self.original_nodes and not self.search_input_str: # Only save original_nodes if no search is active
                 # This logic might need refinement: original_nodes should be the true unfiltered list.
                 # If a search is active, original_nodes should already hold the full list.
                 # Let's assume original_nodes is set once when the first search begins or when cleared.
                 # A better place to set original_nodes might be when a search is *applied* or *cleared*.
                self.original_nodes = list(self.visible_nodes)


    def handle_search_input(self, ch):
        """Process input in search mode."""
        if ch == 27:  # ESC
            # Store if a filter was active before clearing
            was_filter_active = bool(self.search_input_str)

            self.search_mode = False
            self.search_buffer = "" # Clear live buffer

            # Only clear applied filter if ESC is pressed *while not actively typing a new one from scratch*
            # Or if the user intended to clear the existing filter by pressing ESC.
            # The main ESC logic in run() handles clearing an *applied* filter when not in search_mode.
            # This ESC in handle_search_input is for when search_mode is true.
            if not self.search_input_str: # If no search was previously applied (buffer was empty or not submitted)
                if self.original_nodes:
                    self.visible_nodes = list(self.original_nodes)
                # self.original_nodes = [] # Don't clear original_nodes yet, might be needed if user re-enters search

            # If user presses ESC in search mode, we always clear current input string and patterns
            self.search_input_str = ""
            self.search_patterns_list = []
            self.search_had_no_results = False

            # If no filter was active, and ESC is pressed in search mode, restore original full list.
            if not was_filter_active and self.original_nodes:
                 self.visible_nodes = list(self.original_nodes)
                 self.original_nodes = [] # Now clear, as we've reverted to pre-search state.

            return True
        elif ch in (10, 13):  # Enter
            self.search_input_str = self.search_buffer
            # Split by comma or space, and filter out empty strings
            raw_patterns = re.split(r'[, ]+', self.search_input_str)
            self.search_patterns_list = [p for p in raw_patterns if p]

            self.search_mode = False  # Exit search mode after submitting
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
        """Filter files based on the current search_patterns_list."""
        self.search_had_no_results = False # Reset flag

        if not self.search_input_str or not self.search_patterns_list: # If search input is empty or resulted in no patterns
            if self.original_nodes:
                self.visible_nodes = list(self.original_nodes)
            # Potentially clear self.original_nodes = [] if we consider this a "filter cleared" state
            # However, original_nodes should persist if user clears search then types a new one.
            # Clearing of original_nodes is handled by ESC in run() or handle_search_input.
            self.search_input_str = "" # Ensure consistency
            self.search_patterns_list = []
            return

        # If this is the first real search operation (original_nodes is not yet set),
        # store the current complete list of nodes.
        if not self.original_nodes:
            # This assumes visible_nodes currently holds the full, unfiltered list.
            # This should be true if original_nodes is empty.
            self.original_nodes = list(flatten_tree(self.root_node)) # Ensure it's the full list

        # self.visible_nodes is passed as an output parameter and will be modified in place.
        success, error_message = apply_search_filter(
            self.search_patterns_list,
            self.case_sensitive, 
            self.root_node, 
            self.original_nodes, # Pass the true original list for reference
            self.visible_nodes  # This list will be modified
        )
        
        if not success:
            if error_message == "검색 결과 없음":
                self.search_had_no_results = True
                # self.visible_nodes is already set to [] by selector_actions.apply_search_filter

            # Display error message (e.g., "잘못된 정규식" or "검색 결과 없음")
            # For "검색 결과 없음", draw_tree will handle the specific message.
            # For other errors like "잘못된 정규식", show a temporary message.
            if error_message != "검색 결과 없음": # Avoid double messaging for "no results"
                self.stdscr.addstr(self.height - 2, 1, f"Error: {error_message}", curses.color_pair(6))
                self.stdscr.refresh()
                curses.napms(1500) # Show message for a bit
        # No explicit return needed if success is True, visible_nodes is updated.

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
                    result = toggle_expand(node, self.search_mode, self.search_input_str,
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
                    result = toggle_expand(node, self.search_mode, self.search_input_str,
                                         self.original_nodes, self.apply_search_filter)
                    if result:
                        self.visible_nodes = result
                    return True
        return False

    def draw_tree(self):
        """Draw a file tree."""
        self.stdscr.clear()
        self.update_dimensions()

        # Update visible_nodes based on current state
        if not self.search_mode and not self.search_input_str:
            if not self.original_nodes: # No prior search or search fully cleared
                self.visible_nodes = flatten_tree(self.root_node)
            # If self.original_nodes exists, visible_nodes should have been restored by clear/ESC logic
        # If a search IS active (self.search_input_str is not empty), visible_nodes is managed by apply_search_filter

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
        # Line 0 for search status / general status
        if self.search_mode or self.search_input_str:
            search_text_display = self.search_buffer if self.search_mode else self.search_input_str
            search_display_line = f"Search: {search_text_display}"
            case_status = "Case-sensitive" if self.case_sensitive else "Ignore case"

            # Truncate search_display_line if too long
            max_search_len = self.width - len(f" ({case_status})") - len(f"Show: {visible_count}/{total_count}") - 5
            if len(search_display_line) > max_search_len:
                search_display_line = search_display_line[:max_search_len-3] + "..."

            self.stdscr.addstr(0, 0, search_display_line, curses.color_pair(7) | curses.A_BOLD)
            self.stdscr.addstr(0, len(search_display_line) + 2, f"({case_status})", curses.color_pair(7))

            # Show "Show: X/Y" to the right
            stats_show_text = f"Show: {visible_count}/{total_count}"
            self.stdscr.addstr(0, self.width - len(stats_show_text) -1 , stats_show_text, curses.A_BOLD)

            # Line 1 for selected files count (always shown)
            self.stdscr.addstr(1, 0, f"Selected Files: {selected_count}/{total_count}", curses.A_BOLD)
        else:
            self.stdscr.addstr(0, 0, f"Selected Files: {selected_count}/{total_count}", curses.A_BOLD)

        # Display "일치하는 파일 없음" if applicable (line 2 or 3 based on layout)
        if self.search_input_str and self.search_had_no_results and not self.visible_nodes:
            message_y = 2 # Start message on line 2
            self.stdscr.addstr(message_y, 0, "일치하는 파일 없음", curses.color_pair(6))
        else:
            # Draw the tree starting from line 2
            for i, (node, level) in enumerate(self.visible_nodes[self.scroll_offset:self.scroll_offset + self.max_visible]):
                y = i + 2  # Start tree drawing from line 2
                if y >= self.max_visible + 2: # Adjust boundary
                    break

                # 유형 및 선택 상태에 따라 색상 결정
                if i + self.scroll_offset == self.current_index:
                    attr = curses.color_pair(5) # Highlight
                elif node.is_dir:
                    attr = curses.color_pair(3) if node.selected else curses.color_pair(2)
                else:
                    attr = curses.color_pair(1) if node.selected else curses.color_pair(4)

                indent = "  " * level
                prefix = "+ " if node.is_dir and node.expanded else ("- " if node.is_dir else ("✓ " if node.selected else "☐ "))

                name_space = self.width - len(indent) - len(prefix) - 1 # Adjusted for potential border
                name_display = node.name[:name_space] + ("..." if len(node.name) > name_space else "")

                self.stdscr.addstr(y, 0, f"{indent}{prefix}{name_display}", attr)

        # 화면 하단에 도움말 표시
        help_y = self.height - 4 # Adjusted for potentially one less line due to stats/search display
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
                    result = toggle_expand(node, self.search_mode, self.search_input_str,
                                         self.original_nodes, self.apply_search_filter)
                    if result:
                        self.visible_nodes = result
                    # 검색 모드에서는 필터링 다시 적용
                    if self.search_input_str: # Use search_input_str
                        self.apply_search_filter()
                    return True
        elif key == curses.KEY_LEFT:
            # 디렉토리 닫기
            if self.current_index < len(self.visible_nodes):
                node, _ = self.visible_nodes[self.current_index]
                if node.is_dir and node.expanded:
                    result = toggle_expand(node, self.search_mode, self.search_input_str,
                                         self.original_nodes, self.apply_search_filter)
                    if result:
                        self.visible_nodes = result
                    # 검색 모드에서는 필터링 다시 적용
                    if self.search_input_str: # Use search_input_str
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
                    # Call handle_search_input with ESC, which will manage search state
                    self.handle_search_input(key)
                    # handle_search_input now sets search_mode to False.
                    # It also handles restoring nodes if search_buffer was empty.
                elif self.search_input_str: # Not in search mode, but a filter is active
                    # Clear all search state and restore original nodes
                    self.search_input_str = ""
                    self.search_patterns_list = []
                    self.search_buffer = ""
                    self.search_had_no_results = False
                    if self.original_nodes:
                         self.visible_nodes = list(self.original_nodes) # Restore from original_nodes
                    else: # Fallback if original_nodes somehow not set
                         self.visible_nodes = flatten_tree(self.root_node)
                    self.original_nodes = [] # Clear original_nodes as the filter is now cleared
                else:
                    # No active filter, not in search mode: exit
                    return False # Exit application
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