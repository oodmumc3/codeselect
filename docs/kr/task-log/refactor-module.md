# CodeSelect 모듈화 작업 계획

## 완료된 작업
- ✅ **utils.py**: 공통 유틸리티 함수 분리 (언어 매핑, 클립보드, 파일명 생성 등)
  - `get_language_name()`: 확장자를 언어명으로 변환
  - `try_copy_to_clipboard()`: 클립보드 복사 기능
  - `generate_output_filename()`: 출력 파일명 생성
  - `should_ignore_path()`: 무시할 경로 확인

## 테스트 코드
- ✅ **test/test_utils.py**: utils.py 기능 테스트

## 남은 작업 및 파일 구조
```
codeselect/
├── codeselect.py     # 메인 실행 파일
├── utils.py          # 완료: 공통 유틸리티 함수 
├── filetree.py       # 예정: 파일 트리 구조 관리
├── selector.py       # 예정: 파일 선택 UI 
├── output.py         # 예정: 출력 형식 관리
├── dependency.py     # 예정: 의존성 분석
└── cli.py            # 예정: 명령행 인터페이스
```

## 변환 작업 상세
1. **filetree.py**
   - `Node` 클래스
   - `build_file_tree()` 함수
   - `flatten_tree()` 함수 
   - `count_selected_files()` 함수
   - `collect_selected_content()` 함수
   - `collect_all_content()` 함수

2. **selector.py**
   - `FileSelector` 클래스
   - `interactive_selection()` 함수

3. **output.py**
   - `write_file_tree_to_string()` 함수
   - `write_output_file()` 함수
   - `write_markdown_output()` 함수
   - `write_llm_optimized_output()` 함수

4. **dependency.py**
   - `analyze_dependencies()` 함수

5. **cli.py**
   - 명령행 인수 처리 (`argparse` 관련 코드)
   - `main()` 함수 리팩토링

6. **codeselect.py** (리팩토링)
   - 모듈들을 임포트하고 조합하는 간결한 메인 스크립트로 변환