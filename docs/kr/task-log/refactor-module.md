# CodeSelect 모듈화 작업 계획

## 완료된 작업
- ✅ **utils.py**: 공통 유틸리티 함수 분리 (2025-03-10 완료)
  - `get_language_name()`: 확장자를 언어명으로 변환
  - `try_copy_to_clipboard()`: 클립보드 복사 기능
  - `generate_output_filename()`: 출력 파일명 생성
  - `should_ignore_path()`: 무시할 경로 확인
- ✅ **filetree.py**: 파일 트리 구조 관리 (2025-03-10 완료)
  - `Node` 클래스: 파일/디렉토리 노드 표현
  - `build_file_tree()`: 주어진 디렉토리의 파일 구조를 트리로 구성
  - `flatten_tree()`: 트리를 평탄화하여 UI 표시용 노드 목록으로 변환
  - `count_selected_files()`: 선택된 파일 수 계산
  - `collect_selected_content()`: 선택된 파일들의 내용 수집
  - `collect_all_content()`: 모든 파일의 내용 수집 (skip-selection 옵션용)
- ✅ **selector.py**: 파일 선택 UI (2025-03-10 완료)
  - `FileSelector` 클래스: curses 기반 대화형 파일 선택 UI
  - `interactive_selection()`: 선택 인터페이스 실행 함수
- ✅ **output.py**: 출력 형식 관리 (2025-03-11 완료)
  - `write_file_tree_to_string()`: 파일 트리를 문자열로 변환
  - `write_output_file()`: 여러 형식의 출력 파일 생성 
  - `write_markdown_output()`: 마크다운 형식 출력
  - `write_llm_optimized_output()`: LLM 최적화 형식 출력
- ✅ **dependency.py**: 의존성 분석 (2025-03-11 완료)
  - `analyze_dependencies()`: 파일 간 의존성 분석
- ✅ **cli.py**: 명령행 인터페이스 (2025-03-11 완료)
  - `parse_arguments()`: 명령행 인수 처리
  - `main()`: 메인 실행 함수

## 테스트 코드
- ✅ **test/test_utils.py**: utils.py 기능 테스트 (2025-03-10 완료)
- ✅ **test/test_filetree.py**: filetree.py 기능 테스트 (2025-03-10 완료)
- ✅ **test/test_selector.py**: selector.py 기능 테스트 (2025-03-10 완료)
- ✅ **test/test_output.py**: output.py 기능 테스트 (2025-03-11 완료)
- ✅ **test/test_dependency.py**: dependency.py 기능 테스트 (2025-03-11 완료)
- ✅ **test/test_cli.py**: cli.py 기능 테스트 (2025-03-11 완료)

## 남은 작업 및 파일 구조
```
codeselect/
├── codeselect.py     # 메인 실행 파일
├── utils.py          # 완료: 공통 유틸리티 함수 
├── filetree.py       # 완료: 파일 트리 구조 관리
├── selector.py       # 완료: 파일 선택 UI 
├── output.py         # 완료: 출력 형식 관리
├── dependency.py     # 완료: 의존성 분석
└── cli.py            # 완료: 명령행 인터페이스
```

## 변환 작업 상세
1. **utils.py** ✅
   - `get_language_name()` 함수
   - `try_copy_to_clipboard()` 함수
   - `generate_output_filename()` 함수
   - `should_ignore_path()` 함수 (추가)

2. **filetree.py** ✅
   - `Node` 클래스
   - `build_file_tree()` 함수
   - `flatten_tree()` 함수 
   - `count_selected_files()` 함수
   - `collect_selected_content()` 함수
   - `collect_all_content()` 함수

3. **selector.py** ✅
   - `FileSelector` 클래스
   - `interactive_selection()` 함수

4. **output.py** ✅
   - `write_file_tree_to_string()` 함수
   - `write_output_file()` 함수
   - `write_markdown_output()` 함수
   - `write_llm_optimized_output()` 함수

5. **dependency.py** ✅
   - `analyze_dependencies()` 함수

6. **cli.py** ✅
   - 명령행 인수 처리 (`argparse` 관련 코드)
   - `main()` 함수 리팩토링

7. **codeselect.py** ✅ (리팩토링)
   - 모듈들을 임포트하고 조합하는 간결한 메인 스크립트로 변환