# 📂 프로젝트 구조 (`codeselect`)

## 🏗️ **폴더 및 파일 개요**
```
codeselect/
  ├── codeselect.py        # 메인 실행 스크립트 (CLI 진입점)
  ├── cli.py               # CLI 명령어 처리 및 실행 흐름 제어
  ├── filetree.py          # 파일 트리 탐색 및 계층 구조 관리
  ├── selector.py          # curses 기반 파일 선택 UI
  ├── output.py            # 선택된 파일의 출력 (txt, md, llm 지원)
  ├── dependency.py        # 파일 간 의존성 분석 (import/include 탐색)
  ├── utils.py             # 공통 유틸리티 함수 (경로 처리, 클립보드 복사 등)
  ├── install.sh           # 프로젝트 설치 스크립트
  ├── uninstall.sh         # 프로젝트 제거 스크립트
  ├── tests/               # 유닛 테스트 폴더
  ├── docs/                # 문서화 폴더 (설계 개요, 사용법 등)
  └── .codeselectrc        # 사용자 설정 파일 (필터링, 출력 설정)
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

### 4️⃣ `selector.py` (파일 선택 UI)
- `FileSelector` 클래스: curses 기반 인터랙티브 UI 제공
- `run()`: 파일 선택 인터페이스 실행
- `toggle_selection(node)`: Space 키로 파일 선택/해제

### 5️⃣ `dependency.py` (의존성 분석)
- `analyze_dependencies(root_path, file_contents)`: `import`, `require`, `include` 패턴을 분석하여 파일 간 참조 관계를 추출
- Python, JavaScript, C/C++ 등의 언어를 지원

### 6️⃣ `output.py` (출력 파일 저장)
- `write_output_file(output_path, format)`: 선택된 파일을 다양한 형식(txt, md, llm)으로 변환하여 저장
- `llm` 포맷은 AI 모델이 이해하기 쉬운 구조로 가공

### 7️⃣ `utils.py` (유틸리티 함수)
- `generate_output_filename(root_path, format)`: 출력 파일명을 자동 생성
- `try_copy_to_clipboard(content)`: 선택된 파일 내용을 클립보드에 복사

### 8️⃣ `tests/` (테스트 코드)
- `filetree_test.py`: 파일 트리 생성 테스트
- `selector_test.py`: 파일 선택 UI 테스트
- `dependency_test.py`: 의존성 분석 테스트

---
## 🚀 **실행 흐름 요약**
1️⃣ `codeselect.py` 실행 → `cli.py`에서 인자 파싱
2️⃣ `filetree.py`에서 파일 트리 생성
3️⃣ `selector.py`에서 curses UI 실행 (파일 선택)
4️⃣ `dependency.py`에서 파일 간 의존성 분석
5️⃣ `output.py`에서 선택된 파일을 저장 및 클립보드 복사