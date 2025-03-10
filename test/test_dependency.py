#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dependency.py 모듈에 대한 테스트 코드
"""

import os
import sys
import unittest
import tempfile

# 테스트 대상 모듈 임포트
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import dependency

class TestDependency(unittest.TestCase):
    """dependency.py 모듈의 함수들을 테스트하는 클래스"""

    def setUp(self):
        """테스트 준비"""
        self.temp_dir = tempfile.mkdtemp()
        
        # 다양한 언어로 된 테스트 파일 생성
        self.python_file1 = os.path.join(self.temp_dir, "main.py")
        self.python_file2 = os.path.join(self.temp_dir, "utils.py")
        self.js_file = os.path.join(self.temp_dir, "app.js")
        self.cpp_file = os.path.join(self.temp_dir, "program.cpp")
        
        # 디렉토리 생성
        os.makedirs(os.path.join(self.temp_dir, "lib"), exist_ok=True)
        self.lib_file = os.path.join(self.temp_dir, "lib", "helper.py")
        
        # 파일 내용 정의
        self.python_content1 = """
import os
import sys
from utils import format_string
from lib.helper import Helper
"""
        
        self.python_content2 = """
import os
import datetime

def format_string(s):
    return s.strip()
"""
        
        self.lib_content = """
class Helper:
    def __init__(self):
        pass
"""
        
        self.js_content = """
import React from 'react';
import { useState } from 'react';
const axios = require('axios');
import './styles.css';
"""
        
        self.cpp_content = """
#include <iostream>
#include <vector>
#include "lib/helper.hpp"
"""
        
        # 파일 작성
        with open(self.python_file1, 'w') as f:
            f.write(self.python_content1)
        
        with open(self.python_file2, 'w') as f:
            f.write(self.python_content2)
        
        with open(self.lib_file, 'w') as f:
            f.write(self.lib_content)
        
        with open(self.js_file, 'w') as f:
            f.write(self.js_content)
        
        with open(self.cpp_file, 'w') as f:
            f.write(self.cpp_content)
        
        # 파일 내용 리스트 생성
        self.file_contents = [
            ("main.py", self.python_content1),
            ("utils.py", self.python_content2),
            ("lib/helper.py", self.lib_content),
            ("app.js", self.js_content),
            ("program.cpp", self.cpp_content)
        ]

    def tearDown(self):
        """테스트 정리 - 임시 파일 삭제"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_analyze_dependencies(self):
        """analyze_dependencies 함수 테스트"""
        # 의존성 분석 함수 호출
        dependencies = dependency.analyze_dependencies(self.temp_dir, self.file_contents)
        
        # 결과 검증
        # 1. main.py 확인
        self.assertIn("main.py", dependencies)
        deps = dependencies["main.py"]
        
        # main.py는 utils.py와 lib/helper.py에 의존성이 있어야 함
        self.assertIn("utils.py", deps)
        self.assertIn("lib/helper.py", deps)
        
        # 외부 모듈도 의존성에 포함되어야 함 (실제 파일이 없으므로 문자열로만 존재)
        self.assertTrue(any(dep == "os" for dep in deps))
        self.assertTrue(any(dep == "sys" for dep in deps))
        
        # 2. utils.py 확인
        self.assertIn("utils.py", dependencies)
        deps = dependencies["utils.py"]
        
        # utils.py는 os와 datetime에 의존성이 있어야 함
        self.assertTrue(any(dep == "os" for dep in deps))
        self.assertTrue(any(dep == "datetime" for dep in deps))
        
        # 3. app.js 확인
        self.assertIn("app.js", dependencies)
        deps = dependencies["app.js"]
        
        # app.js는 React, useState, axios, styles.css에 의존성이 있어야 함
        self.assertTrue(any(dep == "react" or dep == "React" for dep in deps))
        self.assertTrue(any("useState" in str(dep) for dep in deps))
        self.assertTrue(any("axios" in str(dep) for dep in deps))
        self.assertTrue(any("styles.css" in str(dep) for dep in deps))
        
        # 4. program.cpp 확인
        self.assertIn("program.cpp", dependencies)
        deps = dependencies["program.cpp"]
        
        # program.cpp는 iostream, vector, lib/helper.hpp에 의존성이 있어야 함
        self.assertTrue(any("iostream" in str(dep) for dep in deps))
        self.assertTrue(any("vector" in str(dep) for dep in deps))
        self.assertTrue(any("helper.hpp" in str(dep) for dep in deps))

if __name__ == "__main__":
    unittest.main()