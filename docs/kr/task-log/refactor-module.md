# CodeSelect 모듈화 작업 계획

## 완료된 작업
- ✅ **utils.py**: 공통 유틸리티 함수 분리 (언어 매핑, 클립보드, 파일명 생성 등)
  - `get_language_name()`: 확장자를 언어명으로 변환
  - `try_copy_to_clipboard()`: 클립보드 복사 기능
  - `generate_output_filename()`: 출력 파일명 생성
  - `should_ignore_path()`: 무시할 경로 확인
- ✅ **filetree.py**: 파일 트리 구조 관리
  - `Node` 클래스: 파일/디렉토리 노드 표현
  - `build_file_tree()`: 주어진 디렉토리의 파일 구조를 트리로 구성
  - `flatten_tree()`: 트리를 평탄화하여 UI 표시용 노드 목록으로 변환
  - `count_selected_files()`: 선택된 파일 수 계산
  - `collect_selected_content()`: 선택된 파일들의 내용 수집
  - `collect_all_content()`: 모든 파일의 내용 수집 (skip-selection 옵션용)
  - `_should_ignore()`: 파일/디렉토리 무시 여부 확인 (내부 함수)

## 테스트 코드
- ✅ **test/test_utils.py**: utils.py 기능 테스트
- ✅ **test/test_filetree.py**: filetree.py 기능 테스트

## 남은 작업 및 파일 구조
```
codeselect/
├── codeselect.py     # 메인 실행 파일
├── utils.py          # 완료: 공통 유틸리티 함수 
├── filetree.py       # 완료: 파일 트리 구조 관리
├── selector.py       # 예정: 파일 선택 UI 
├── output.py         # 예정: 출력 형식 관리
├── dependency.py     # 예정: 의존성 분석
└── cli.py            # 예정: 명령행 인터페이스
```

## 변환 작업 상세
1. **filetree.py** ✅
   - `Node` 클래스
   - `build_file_tree()` 함수
   - `flatten_tree()` 함수 
   - `count_selected_files()` 함수
   - `collect_selected_content()` 함수
   - `collect_all_content()` 함수
   - `_should_ignore()` 함수 (추가)

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