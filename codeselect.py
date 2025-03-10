#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeSelect - 메인 스크립트

AI 어시스턴트와 공유할 파일을 쉽게 선택하고 내보내는 도구입니다.
이 파일은 단순히 cli 모듈의 main 함수를 호출하는 진입점 역할만 수행합니다.

작성자: Anthropic Claude & 사용자
"""

import sys
from cli import main

if __name__ == "__main__":
    sys.exit(main())