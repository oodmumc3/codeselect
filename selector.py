#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selector.py - 파일 선택 UI 모듈

curses 기반의 대화형 파일 선택 인터페이스를 제공하는 모듈입니다.
"""

import os
import sys
import curses
from filetree import flatten_tree, count_selected_files

class FileSelector:
    """
    curses 기반의 대화형 파일 선택 인터페이스를 제공하는 클래스
    
    사용자가 파일 트리에서 파일을 선택할 수 있는 UI를 제공합니다.
    """
    def __init__(self, root_node, stdscr):
        """
        FileSelector 클래스 초기화
        
        Args:
            root_node (Node): 파일 트리의 루트 노드
            stdscr (curses.window): curses 창 객체
        """
        self.root_node = root_node
        self.stdscr = stdscr
        self.current_index = 0
        self.scroll_offset = 0
        self.visible_nodes = flatten_tree(root_node)
        self.max_visible = 0
        self.height, self.width = 0, 0
        self.copy_to_clipboard = True  # 기본값: 클립보드 복사 활성화
        self.initialize_curses()

    def initialize_curses(self):
        """curses 설정을 초기화합니다."""
        curses.start_color()
        curses.use_default_colors()
        # 색상 쌍 정의
        curses.init_pair(1, curses.COLOR_GREEN, -1)    # 선택된 파일
        curses.init_pair(2, curses.COLOR_BLUE, -1)     # 디렉토리
        curses.init_pair(3, curses.COLOR_YELLOW, -1)   # 선택된 디렉토리
        curses.init_pair(4, curses.COLOR_WHITE, -1)    # 선택되지 않은 파일
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)  # 현재 선택
        curses.init_pair(6, curses.COLOR_RED, -1)      # 도움말 메시지

        # 커서 숨기기
        curses.curs_set(0)

        # 특수 키 활성화
        self.stdscr.keypad(True)

        # 화면 크기 가져오기
        self.update_dimensions()

    def update_dimensions(self):
        """화면 크기를 업데이트합니다."""
        self.height, self.width = self.stdscr.getmaxyx()
        self.max_visible = self.height - 6  # 상단에 통계를 위한 라인 추가

    def expand_all(self, expand=True):
        """모든 디렉토리를 확장하거나 접습니다."""
        def _set_expanded(node, expand):
            """
            노드와 그 자식들의 expanded 상태를 설정합니다.
            
            Args:
                node (Node): 설정할 노드
                expand (bool): 확장 여부
            """
            if node.is_dir and node.children:
                node.expanded = expand
                for child in node.children.values():
                    _set_expanded(child, expand)

        _set_expanded(self.root_node, expand)
        self.visible_nodes = flatten_tree(self.root_node)

    def toggle_current_dir_selection(self):
        """현재 디렉토리의 파일만 선택 상태를 전환합니다 (하위 디렉토리 제외)."""
        if self.current_index < len(self.visible_nodes):
            current_node, _ = self.visible_nodes[self.current_index]

            # 현재 노드가 디렉토리인 경우, 그 직계 자식들만 선택 상태 전환
            if current_node.is_dir and current_node.children:
                # 자식들의 대부분이 선택되었는지 확인하여 동작 결정
                selected_count = sum(1 for child in current_node.children.values() if child.selected)
                select_all = selected_count <= len(current_node.children) / 2

                # 모든 직계 자식들을 새 선택 상태로 설정
                for child in current_node.children.values():
                    child.selected = select_all
            # 현재 노드가 파일인 경우, 그 선택 상태만 전환
            else:
                current_node.selected = not current_node.selected

    def draw_tree(self):
        """파일 트리를 그립니다."""
        self.stdscr.clear()
        self.update_dimensions()

        # 보이는 노드 목록 업데이트
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
        total_count = sum(1 for node, _ in self.visible_nodes if not node.is_dir)
        self.stdscr.addstr(0, 0, f"선택된 파일: {selected_count}/{total_count}", curses.A_BOLD)

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
        self.stdscr.addstr(help_y, 0, "↑/↓: 탐색  SPACE: 선택  ←/→: 폴더 닫기/열기", curses.color_pair(6))
        help_y += 1
        self.stdscr.addstr(help_y, 0, "T: 현재 폴더만 전환  E: 모두 확장  C: 모두 접기", curses.color_pair(6))
        help_y += 1
        clip_status = "ON" if self.copy_to_clipboard else "OFF"
        self.stdscr.addstr(help_y, 0, f"A: 모두 선택  N: 모두 해제  B: 클립보드 ({clip_status})  X: 취소  D: 완료", curses.color_pair(6))

        self.stdscr.refresh()

    def toggle_selection(self, node):
        """노드의 선택 상태를 전환하고, 디렉토리인 경우 그 자식들의 선택 상태도 전환합니다."""
        node.selected = not node.selected

        if node.is_dir and node.children:
            for child in node.children.values():
                child.selected = node.selected
                if child.is_dir:
                    self.toggle_selection(child)

    def toggle_expand(self, node):
        """디렉토리를 확장하거나 접습니다."""
        if node.is_dir:
            node.expanded = not node.expanded
            # 보이는 노드 목록 업데이트
            self.visible_nodes = flatten_tree(self.root_node)

    def select_all(self, select=True):
        """모든 노드를 선택하거나 선택 해제합니다."""
        def _select_recursive(node):
            """
            노드와 그 자식들의 선택 상태를 재귀적으로 설정합니다.
            
            Args:
                node (Node): 설정할 노드
            """
            node.selected = select
            if node.is_dir and node.children:
                for child in node.children.values():
                    _select_recursive(child)

        _select_recursive(self.root_node)

    def run(self):
        """선택 인터페이스를 실행합니다."""
        while True:
            self.draw_tree()
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                # 위로 이동
                self.current_index = max(0, self.current_index - 1)

            elif key == curses.KEY_DOWN:
                # 아래로 이동
                self.current_index = min(len(self.visible_nodes) - 1, self.current_index + 1)

            elif key == curses.KEY_RIGHT:
                # 디렉토리 열기
                if self.current_index < len(self.visible_nodes):
                    node, _ = self.visible_nodes[self.current_index]
                    if node.is_dir and not node.expanded:
                        self.toggle_expand(node)

            elif key == curses.KEY_LEFT:
                # 디렉토리 닫기
                if self.current_index < len(self.visible_nodes):
                    node, _ = self.visible_nodes[self.current_index]
                    if node.is_dir and node.expanded:
                        self.toggle_expand(node)
                    elif node.parent and node.parent.parent:  # 부모로 이동 (루트 제외)
                        # 부모의 인덱스 찾기
                        for i, (n, _) in enumerate(self.visible_nodes):
                            if n == node.parent:
                                self.current_index = i
                                break

            elif key == ord(' '):
                # 선택 전환
                if self.current_index < len(self.visible_nodes):
                    node, _ = self.visible_nodes[self.current_index]
                    self.toggle_selection(node)

            elif key in [ord('a'), ord('A')]:
                # 모두 선택
                self.select_all(True)

            elif key in [ord('n'), ord('N')]:
                # 모두 선택 해제
                self.select_all(False)

            elif key in [ord('e'), ord('E')]:
                # 모두 확장
                self.expand_all(True)

            elif key in [ord('c'), ord('C')]:
                # 모두 접기
                self.expand_all(False)

            elif key in [ord('t'), ord('T')]:
                # 현재 디렉토리만 선택 전환
                self.toggle_current_dir_selection()

            elif key in [ord('b'), ord('B')]:  # 'c'에서 'b'로 변경 (클립보드)
                # 클립보드 전환
                self.copy_to_clipboard = not self.copy_to_clipboard

            elif key in [ord('x'), ord('X'), 27]:  # 27 = ESC
                # 저장하지 않고 종료
                return False

            elif key in [ord('d'), ord('D'), 10, 13]:  # 10, 13 = Enter
                # 완료
                return True

            elif key == curses.KEY_RESIZE:
                # 창 크기 변경 처리
                self.update_dimensions()

        return True

def interactive_selection(root_node):
    """대화형 파일 선택 인터페이스를 시작합니다."""
    return curses.wrapper(lambda stdscr: FileSelector(root_node, stdscr).run())