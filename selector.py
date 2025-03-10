#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import sys
import re
from typing import List, Dict, Optional, Tuple, Any, Callable

# filetree.py에서 가져올 타입과 함수들
# 실제 임포트는 아래와 같이 처리합니다
# from filetree import Node, flatten_tree, count_selected_files

"""
파일 선택 UI 모듈 - 커서 기반 인터페이스로 파일을 선택할 수 있는 기능 제공
"""

class FileSelector:
    """
    커서 기반 파일 선택기 클래스
    
    이 클래스는 사용자가 파일 트리에서 파일을 선택할 수 있는 
    인터페이스를 제공합니다.
    """
    
    def __init__(self, root_node: 'Node', title: str = "파일 선택"):
        """
        파일 선택기 초기화
        
        Args:
            root_node: 파일 트리의 루트 노드
            title: 화면 상단에 표시될 제목
        """
        self.root_node = root_node
        self.title = title
        self.flat_nodes: List['Node'] = []  # 화면에 표시될 평면화된 노드 목록
        self.cursor_index = 0  # 현재 커서 위치
        self.top_line = 0  # 현재 표시 영역의 상단 라인
        self.screen_height = 0  # 화면 높이
        self.screen_width = 0  # 화면 너비
        self.search_mode = False  # 검색 모드 상태
        self.search_term = ""  # 검색어
        self.filtered_indices: List[int] = []  # 검색 결과 인덱스 목록
        self.clipboard_enabled = True  # 클립보드 복사 활성화 여부
        self.status_message = ""  # 상태 메시지
        self.previous_key = 0  # 이전에 누른 키
        
    def init_curses(self, stdscr) -> None:
        """
        curses 초기화
        
        Args:
            stdscr: curses 표준 화면
        """
        # 기본 색상 설정
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, -1)  # 기본 텍스트
        curses.init_pair(2, curses.COLOR_GREEN, -1)  # 디렉토리
        curses.init_pair(3, curses.COLOR_CYAN, -1)   # 파일
        curses.init_pair(4, curses.COLOR_YELLOW, -1) # 선택됨
        curses.init_pair(5, curses.COLOR_RED, -1)    # 오류/경고
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)  # 반전 (검색 결과)
        
        # 커서 숨기기 및 키 입력 대기 시간 설정
        curses.curs_set(0)
        curses.halfdelay(10)  # 100ms 대기 (키 입력 대기 시간)
        
        # 화면 크기 가져오기
        self.screen_height, self.screen_width = stdscr.getmaxyx()
    
    def refresh_flat_nodes(self, filter_term: Optional[str] = None) -> None:
        """
        평면화된 노드 목록 갱신
        
        Args:
            filter_term: 검색어 (설정 시 해당 검색어가 포함된 노드만 표시)
        """
        # 실제 구현에서는 filetree 모듈의 flatten_tree 함수를 사용
        # self.flat_nodes = flatten_tree(self.root_node)
        
        # 검색 모드일 경우 검색어로 필터링
        if filter_term:
            try:
                pattern = re.compile(filter_term, re.IGNORECASE)
                self.filtered_indices = [
                    i for i, node in enumerate(self.flat_nodes)
                    if pattern.search(node.name)
                ]
                
                # 검색 결과가 없으면 상태 메시지 설정
                if not self.filtered_indices:
                    self.status_message = f"검색 결과 없음: '{filter_term}'"
                else:
                    self.status_message = f"{len(self.filtered_indices)}개 항목 찾음"
                    
                    # 첫 번째 검색 결과로 커서 이동
                    if self.filtered_indices:
                        self.cursor_index = self.filtered_indices[0]
                        self.ensure_cursor_visible()
            except re.error:
                self.status_message = f"잘못된 정규식: '{filter_term}'"
        else:
            # 검색 모드가 아닐 경우 필터링 초기화
            self.filtered_indices = []
            self.status_message = ""
    
    def ensure_cursor_visible(self) -> None:
        """
        커서가 현재 화면에 보이도록 스크롤 조정
        """
        # 표시 가능한 라인 수 (헤더, 도움말 영역 제외)
        visible_lines = self.screen_height - 5
        
        # 커서가 화면 상단보다 위에 있으면 스크롤 업
        if self.cursor_index < self.top_line:
            self.top_line = self.cursor_index
        # 커서가 화면 하단보다 아래에 있으면 스크롤 다운
        elif self.cursor_index >= self.top_line + visible_lines:
            self.top_line = self.cursor_index - visible_lines + 1
    
    def move_cursor(self, direction: int) -> None:
        """
        커서 이동
        
        Args:
            direction: 이동 방향 (1: 아래, -1: 위)
        """
        if self.filtered_indices:
            # 검색 결과 내에서 이동
            current_pos = self.filtered_indices.index(self.cursor_index)
            new_pos = (current_pos + direction) % len(self.filtered_indices)
            self.cursor_index = self.filtered_indices[new_pos]
        else:
            # 일반 모드에서 이동
            self.cursor_index = (self.cursor_index + direction) % len(self.flat_nodes)
        
        self.ensure_cursor_visible()
    
    def toggle_node_selected(self) -> None:
        """
        현재 커서 위치의 노드 선택/해제 토글
        """
        if 0 <= self.cursor_index < len(self.flat_nodes):
            node = self.flat_nodes[self.cursor_index]
            
            # 디렉토리인 경우 하위 모든 파일 선택/해제
            if node.is_dir:
                selected = not all(child.selected for child in node.children if not child.is_dir)
                self._toggle_directory_recursive(node, selected)
            else:
                # 파일인 경우 단일 파일만 선택/해제
                node.selected = not node.selected
    
    def _toggle_directory_recursive(self, node: 'Node', selected: bool) -> None:
        """
        디렉토리와 그 하위 모든 파일의 선택 상태를 재귀적으로 변경
        
        Args:
            node: 대상 노드
            selected: 설정할 선택 상태
        """
        if node.is_dir:
            for child in node.children:
                if child.is_dir:
                    self._toggle_directory_recursive(child, selected)
                else:
                    child.selected = selected
    
    def toggle_directory_expanded(self) -> None:
        """
        현재 커서 위치의 디렉토리 확장/축소 토글
        """
        if 0 <= self.cursor_index < len(self.flat_nodes):
            node = self.flat_nodes[self.cursor_index]
            if node.is_dir:
                node.expanded = not node.expanded
                # 노드 목록 갱신
                self.refresh_flat_nodes(self.search_term if self.search_mode else None)
    
    def toggle_all_selected(self, selected: bool) -> None:
        """
        모든 파일 선택/해제
        
        Args:
            selected: 모든 파일을 선택할지(True) 해제할지(False) 여부
        """
        self._toggle_all_selected_recursive(self.root_node, selected)
        
        if selected:
            self.status_message = "모든 파일이 선택되었습니다"
        else:
            self.status_message = "모든 파일이 선택 해제되었습니다"
    
    def _toggle_all_selected_recursive(self, node: 'Node', selected: bool) -> None:
        """
        노드와 그 하위 모든 노드의 선택 상태를 재귀적으로 변경
        
        Args:
            node: 대상 노드
            selected: 설정할 선택 상태
        """
        if node.is_dir:
            for child in node.children:
                self._toggle_all_selected_recursive(child, selected)
        else:
            node.selected = selected
    
    def toggle_clipboard(self) -> None:
        """
        클립보드 복사 기능 활성화/비활성화 토글
        """
        self.clipboard_enabled = not self.clipboard_enabled
        self.status_message = f"클립보드 복사: {'활성화' if self.clipboard_enabled else '비활성화'}"
    
    def draw_screen(self, stdscr) -> None:
        """
        화면 그리기
        
        Args:
            stdscr: curses 표준 화면
        """
        stdscr.clear()
        
        # 타이틀 표시
        title_text = f" {self.title} "
        stdscr.addstr(0, 0, "=" * self.screen_width)
        stdscr.addstr(0, (self.screen_width - len(title_text)) // 2, title_text)
        
        # 선택된 파일 수 표시
        selected_count = 0  # count_selected_files(self.root_node)
        info_text = f"선택됨: {selected_count} 파일"
        if self.clipboard_enabled:
            info_text += " | 클립보드 복사: 활성화"
        else:
            info_text += " | 클립보드 복사: 비활성화"
        stdscr.addstr(1, 0, info_text)
        
        # 검색 모드일 경우 검색창 표시
        if self.search_mode:
            search_text = f"검색: {self.search_term}"
            stdscr.addstr(2, 0, search_text, curses.color_pair(6))
        
        # 파일 목록 표시
        visible_lines = self.screen_height - 5  # 헤더, 도움말 영역 제외
        for i in range(min(visible_lines, len(self.flat_nodes))):
            line_index = self.top_line + i
            if line_index < len(self.flat_nodes):
                node = self.flat_nodes[line_index]
                
                # 들여쓰기 레벨
                indent = "  " * node.level
                
                # 폴더/파일 표시
                if node.is_dir:
                    prefix = "+ " if node.expanded else "- "
                    color = curses.color_pair(2)  # 폴더 색상
                else:
                    prefix = "  "
                    color = curses.color_pair(3)  # 파일 색상
                
                # 선택 상태 표시
                if node.selected and not node.is_dir:
                    select_mark = "[*]"
                    color = curses.color_pair(4)  # 선택됨 색상
                else:
                    select_mark = "[ ]"
                
                # 현재 커서 위치 하이라이트
                if line_index == self.cursor_index:
                    attr = curses.A_REVERSE
                else:
                    attr = 0
                
                # 검색 결과 하이라이트
                if self.filtered_indices and line_index in self.filtered_indices:
                    attr |= curses.A_BOLD
                
                # 노드 정보 출력
                line_text = f"{select_mark} {indent}{prefix}{node.name}"
                stdscr.addnstr(3 + i, 0, line_text, self.screen_width - 1, color | attr)
        
        # 상태 메시지 표시
        if self.status_message:
            stdscr.addstr(self.screen_height - 2, 0, self.status_message)
        
        # 도움말 표시
        help_text = "↑/↓: 이동 | Space: 선택 | ←/→: 접기/펼치기 | A: 모두 선택 | N: 모두 해제 | C: 클립보드 | D/Enter: 완료 | Esc: 취소"
        help_text = help_text[:self.screen_width - 1]
        stdscr.addstr(self.screen_height - 1, 0, help_text)
        
        # 화면 갱신
        stdscr.refresh()
    
    def process_normal_key(self, key: int) -> Optional[bool]:
        """
        일반 모드에서 키 입력 처리
        
        Args:
            key: 입력된 키 코드
            
        Returns:
            None: 계속 진행
            True: 선택 완료
            False: 선택 취소
        """
        if key == curses.KEY_UP:
            self.move_cursor(-1)
        elif key == curses.KEY_DOWN:
            self.move_cursor(1)
        elif key == curses.KEY_LEFT:
            # 접기
            if 0 <= self.cursor_index < len(self.flat_nodes):
                node = self.flat_nodes[self.cursor_index]
                if node.is_dir and node.expanded:
                    node.expanded = False
                    self.refresh_flat_nodes(self.search_term if self.search_mode else None)
                elif node.level > 0:
                    # 부모 노드로 이동
                    parent_level = node.level - 1
                    for i in range(self.cursor_index - 1, -1, -1):
                        if self.flat_nodes[i].level == parent_level:
                            self.cursor_index = i
                            self.ensure_cursor_visible()
                            break
        elif key == curses.KEY_RIGHT:
            # 펼치기
            if 0 <= self.cursor_index < len(self.flat_nodes):
                node = self.flat_nodes[self.cursor_index]
                if node.is_dir and not node.expanded:
                    node.expanded = True
                    self.refresh_flat_nodes(self.search_term if self.search_mode else None)
        elif key == ord(' '):
            # 선택/해제 토글
            self.toggle_node_selected()
        elif key in (ord('a'), ord('A')):
            # 모두 선택
            self.toggle_all_selected(True)
        elif key in (ord('n'), ord('N')):
            # 모두 해제
            self.toggle_all_selected(False)
        elif key in (ord('c'), ord('C')):
            # 클립보드 토글
            self.toggle_clipboard()
        elif key in (ord('/'), ord('?')):
            # 검색 모드 시작
            self.search_mode = True
            self.search_term = ""
            self.status_message = "검색 모드 (Esc로 취소)"
        elif key in (ord('d'), ord('D'), 10, 13):  # Enter 키(10, 13)
            # 선택 완료
            return True
        elif key in (27, ord('q'), ord('Q')):  # Esc 키(27)
            # 선택 취소
            return False
        
        return None
    
    def process_search_key(self, key: int) -> Optional[bool]:
        """
        검색 모드에서 키 입력 처리
        
        Args:
            key: 입력된 키 코드
            
        Returns:
            None: 계속 진행
            True: 선택 완료
            False: 선택 취소
        """
        if key == 27:  # Esc 키
            # 검색 모드 취소
            self.search_mode = False
            self.search_term = ""
            self.filtered_indices = []
            self.status_message = "검색이 취소되었습니다"
        elif key in (10, 13):  # Enter 키
            # 검색 완료
            self.search_mode = False
            self.status_message = ""
        elif key == curses.KEY_BACKSPACE or key == 127:  # Backspace 키
            # 검색어 지우기
            self.search_term = self.search_term[:-1]
            self.refresh_flat_nodes(self.search_term if self.search_term else None)
        elif 32 <= key <= 126:  # 일반 문자
            # 검색어에 문자 추가
            self.search_term += chr(key)
            self.refresh_flat_nodes(self.search_term)
        
        return None
    
    def run(self, stdscr) -> bool:
        """
        파일 선택기 실행
        
        Args:
            stdscr: curses 표준 화면
            
        Returns:
            선택 완료 여부 (True: 완료, False: 취소)
        """
        # curses 초기화
        self.init_curses(stdscr)
        
        # 평면화된 노드 목록 초기화
        self.refresh_flat_nodes()
        
        # 메인 루프
        while True:
            # 화면 그리기
            self.draw_screen(stdscr)
            
            # 키 입력 대기
            try:
                key = stdscr.getch()
            except:
                # 예외 발생 시 (터미널 크기 변경 등) 화면 갱신
                self.screen_height, self.screen_width = stdscr.getmaxyx()
                continue
            
            # 검색 모드 여부에 따라 다른 키 처리 함수 호출
            result = self.process_search_key(key) if self.search_mode else self.process_normal_key(key)
            
            # 처리 결과에 따라 종료 여부 결정
            if result is not None:
                return result
            
            # 이전 키 저장
            self.previous_key = key


def interactive_selection(root_node: 'Node', title: str = "파일 선택") -> bool:
    """
    대화형 파일 선택 인터페이스를 실행
    
    Args:
        root_node: 파일 트리의 루트 노드
        title: 화면 상단에 표시될 제목
        
    Returns:
        선택 완료 여부 (True: 완료, False: 취소)
    """
    try:
        # FileSelector 인스턴스 생성
        selector = FileSelector(root_node, title)
        
        # curses 실행
        result = curses.wrapper(selector.run)
        
        # curses 종료 후 화면 초기화
        print("\033c", end="")
        
        return result
    except Exception as e:
        # 예외 발생 시 curses 종료 및 화면 초기화
        print("\033c", end="")
        print(f"오류 발생: {e}")
        return False