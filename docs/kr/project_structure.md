# 📂 프로젝트 구조 (`codeselect`)

## 🏗️ **폴더 및 파일 개요**
```
codeselect/
  ├── codeselect.py        # 메인 실행 스크립트 (CLI 진입점)
  ├── cli.py               # CLI 명령어 처리 및 실행 흐름 제어
  ├── filetree.py          # 파일 트리 탐색 및 계층 구조 관리
  ├── selector.py          # 파일 선택 인터페이스 (진입점 역할)
  ├── selector_ui.py       # curses 기반 UI 구현 (FileSelector 클래스)
  ├── selector_actions.py  # 파일 선택 관련 동작 함수 모음
  ├── output.py            # 선택된 파일의 출력 (txt, md, llm 지원)
  ├── dependency.py        # 파일 간 의존성 분석 (import/include 탐색)
  ├── utils.py             # 공통 유틸리티 함수 (경로 처리, 클립보드 복사 등)
  ├── install.sh           # 프로젝트 설치 스크립트
  ├── uninstall.sh         # 프로젝트 제거 스크립트
  ├── tests/               # 유닛 테스트 폴더
  │   ├── test_filetree.py         # 파일 트리 생성 테스트
  │   ├── test_selector.py         # 파일 선택 인터페이스 테스트
  │   ├── test_selector_actions.py # 파일 선택 액션 테스트
  │   ├── test_selector_ui.py      # UI 컴포넌트 테스트
  │   └── test_dependency.py       # 의존성 분석 테스트
  ├── docs/                # 문서화 폴더 (설계 개요, 사용법 등)
```

## 🛠️ **핵심 모듈 설명**

### 1️⃣ `codeselect.py` (프로그램 실행 진입점)
- `cli.py`를 호출하여 프로그램을 실행
- `argparse`로 CLI 옵션을 파싱 후, `filetree.py`에서 파일을 탐색하고 `selector.py`로 선택 UI 실행

### 2️⃣ `cli.py` (CLI 명령어 및 실행 흐름 관리)
- 명령어 인수(`--format`, `--skip-selection` 등)를 처리
- `filetree.build_file_tree()`를 호출하여 파일 목록 생성
- `selector.interactive_selection()`을 실행해 UI에서 파일 선택
- `dependency.analyze_dependencies()`를 호출해 종속성 분석 수행
- 최종적으로 `output.write_output_file()`로 결과 저장

### 3️⃣ `filetree.py` (파일 트리 탐색 및 관리)
- `build_file_tree(root_path)`: 디렉토리 내부 파일 및 폴더를 계층적으로 분석하여 트리 구조 생성
- `flatten_tree(node)`: 트리를 리스트로 변환해 UI에서 쉽게 탐색 가능하도록 변환

### 4️⃣ 파일 선택 모듈 (분리된 세 개의 파일)
#### a. `selector.py` (외부 인터페이스)
- `interactive_selection(root_node)`: curses 환경 초기화 및 FileSelector 실행
- 간단한 진입점 역할로 외부 모듈과의 인터페이스 제공

#### b. `selector_ui.py` (UI 컴포넌트)
- `FileSelector` 클래스: curses 기반 인터랙티브 UI 구현
- 화면 그리기, 키 입력 처리, 사용자 인터페이스 로직 포함
- `run()`: 선택 인터페이스 실행 루프
- `draw_tree()`: 파일 트리 시각화
- `process_key()`: 키 입력 처리

#### c. `selector_actions.py` (액션 함수)
- `toggle_selection(node)`: 파일/폴더 선택 상태 전환
- `toggle_expand(node)`: 디렉토리 확장/축소
- `apply_search_filter()`: 검색 필터 적용
- `select_all()`: 모든 파일 선택/해제
- `toggle_current_dir_selection()`: 현재 디렉토리 내 파일만 선택/해제

### 5️⃣ `dependency.py` (의존성 분석)
- `analyze_dependencies(root_path, file_contents)`: `import`, `require`, `include` 패턴을 분석하여 파일 간 참조 관계를 추출
- Python, JavaScript, C/C++ 등의 언어를 지원

### 6️⃣ `output.py` (출력 파일 저장)
- `write_output_file(output_path, format)`: 선택된 파일을 다양한 형식(txt, md, llm)으로 변환하여 저장
- `llm` 포맷은 AI 모델이 이해하기 쉬운 구조로 가공

### 7️⃣ `utils.py` (유틸리티 함수)
- `generate_output_filename(root_path, format)`: 출력 파일명을 자동 생성
- `try_copy_to_clipboard(content)`: 선택된 파일 내용을 클립보드에 복사
- `load_gitignore_patterns(directory)`: .gitignore 파일에서 패턴을 로드하고 파싱
- `should_ignore_path(path, ignore_patterns)`: 파일 경로가 무시 패턴과 일치하는지 확인

---
## 🚀 **실행 흐름 요약**
1️⃣ `codeselect.py` 실행 → `cli.py`에서 인자 파싱
2️⃣ `filetree.py`에서 파일 트리 생성
3️⃣ `selector.py`에서 curses 환경 초기화
4️⃣ `selector_ui.py`의 `FileSelector` 클래스가 인터페이스 제공
5️⃣ `selector_actions.py`의 함수들로 사용자 동작 처리
6️⃣ `dependency.py`에서 파일 간 의존성 분석
7️⃣ `output.py`에서 선택된 파일을 저장 및 클립보드 복사