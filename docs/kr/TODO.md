# 📌 TODO 목록

## 🔍 필터링 및 검색 기능 추가
✅ **Vim 스타일 파일 검색 및 트리 조회 (`/` 입력 후 필터링)**
- vim 스타일 키 바인딩 (j/k로 이동, h/l로 폴더 닫고 열기) 추가
- `/` 입력 후 검색어 입력 → 해당 키워드를 포함하는 파일만 표시
- 정규 표현식 지원 (`/.*\.py$` → `.py` 파일만 필터링)
- 대소문자 구분 옵션 (`/foo` vs `/Foo`)

✅ **더 정교한 `.gitignore` 및 필터링 지원**
- `.gitignore` 자동 반영하여 무시할 파일 결정
- `--include` 및 `--exclude` CLI 옵션 추가 (예: `--include "*.py" --exclude "tests/"`)

✅ **프로젝트별 설정 파일 (`.codeselectrc`) 지원**
- 프로젝트 루트에 `.codeselectrc` 파일 저장하여 설정 자동 로드
- JSON/YAML 지원 (예: `include=["*.py"], exclude=["node_modules/"]`)

---

## 🛠 성능 최적화 및 UI 개선
✅ **탐색 속도 최적화**
- `os.walk()` → `scandir()`로 변경하여 속도 향상
- 다중 스레드 또는 비동기 처리 도입 고려 (대형 프로젝트 지원)

✅ **탐색 시 즉시 선택 기능**
- `/` 검색 후 바로 `Enter`로 파일 선택 가능
- 기존 `Space` 선택 방식과 병행 지원

✅ **탐색 중 선택한 파일을 강조 표시**
- 현재 선택된 파일을 상단에 고정 또는 별도 컬러 강조

✅ **최근 사용한 파일/디렉터리 기록**
- `.codeselect_history` 파일을 저장하여 최근 선택된 파일 유지

✅ **파일 트리 탐색 최적화**
- `os.walk()` 대신 `os.scandir()`를 활용하여 성능 향상
- `.gitignore` 및 필터링 속도 개선

✅ **파일 트리 비동기 처리**
- `asyncio` 기반 비동기 디렉토리 탐색 도입 검토
- 대규모 프로젝트에서도 빠르게 파일 트리 구축 가능

✅ **유연한 필터링 지원**
- `.gitignore` 외에 `.codeselectrc`에서 추가적인 필터링 설정 가능하도록 개선

---

## 🚀 CLI 옵션 개선
✅ **자동 실행 모드 (`--auto-select`)**
- 특정 파일을 자동으로 선택하여 UI 없이 실행 (`codeselect --auto-select "*.py"`)

✅ **결과 미리보기 (`--preview`)**
- 선택된 파일의 내용을 미리 보기 기능 추가

✅ **출력 포맷 확장**
- 현재 `txt`, `md`, `llm` 지원 → `json`, `yaml` 추가 지원

✅ **클립보드 자동 복사 옵션**
- `--no-clipboard` 옵션 추가하여 자동 복사 기능 끄기

---

## 📄 문서화 작업
✅ `project_structure.md` 작성 (프로젝트 구조 설명)
✅ `design_overview.md` 작성 (설계 개요 설명)
✅ `usage_guide.md` 작성 (사용법 가이드)
✅ `file_selection.md` 작성 (파일 선택 로직 설명)
✅ `dependency_analysis.md` 작성 (의존성 분석 문서)
✅ `output_formats.md` 작성 (출력 데이터 형식 설명)

---

### 🏁 **우선순위 정리**
🚀 **1️⃣ Vim 스타일 `/` 검색 기능 추가** (최우선)  
~~📌 **2️⃣ 코드 구조 개선 및 모듈화** (`codeselect.py` → 여러 파일로 분리)~~ (완료)
⚡ **3️⃣ 탐색 속도 최적화 및 UI 개선**  
📦 **4️⃣ `.codeselectrc` 설정 파일 지원**  
📜 **5️⃣ 출력 포맷 확장 (`json`, `yaml` 지원 추가)**  


---

# 완료된 작업

~~## 🏗 코드 구조 개선~~
✅ **코드 분리 및 모듈화** (`codeselect.py` 단일 파일 → 다중 모듈)
- `codeselect.py`가 너무 비대함 → 기능별 모듈로 분리
- 📂 **새로운 모듈 구조**
  - `filetree.py`: 파일 트리 및 탐색 기능
  - `selector.py`: curses 기반 파일 선택 UI
  - `output.py`: 다양한 포맷(txt, md, llm)으로 저장 기능
  - `cli.py`: CLI 명령어 및 옵션 처리
  - `dependency.py`: 프로젝트 내 파일 간 의존성 분석

---
