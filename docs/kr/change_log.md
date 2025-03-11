# Change Log

## v1.1.0 (2024-03-12)

### 🔍 Vim 스타일 검색 기능 추가
- `/` 키를 통한 검색 모드 지원 (Vim 스타일)
- 정규 표현식 검색 완벽 지원 (예: `/.*\.py$`, `/test_.*`)
- 대소문자 구분 토글 기능 (`^` 키 사용)
- 검색 결과에서 트리 구조 유지 - 디렉토리 계층 표시
- 검색 후 ESC 키로 전체 목록 복원 기능
- 검색 결과에서 파일 선택/해제 기능

### 🚀 Vim 스타일 네비게이션 추가
- `j` / `k` 키로 위아래 이동
- `h` / `l` 키로 폴더 닫기/열기 (및 부모 디렉토리로 이동)
- 기존 화살표 키 네비게이션과 병행 지원

### 🎨 UI 개선
- 검색 결과 상태 표시 개선 (현재 표시된 파일 수/전체 파일 수)
- 검색 모드에서 상태 표시줄 변경
- 검색 결과가 없을 경우 알림 표시

### 💻 품질 개선
- 트리 구조 유지 알고리즘 개선
- 검색 취소/완료 시 상태 관리 최적화
- 오류 처리 강화 (잘못된 정규식 입력 시 에러 표시)

## v1.0.0 (2024-03-11)

### 🏗 Code Structure Improvements
- CodeSelect has been modularized for better maintainability and future extensibility
- Separated monolithic codeselect.py into focused modules:
  - `utils.py`: Common utility functions
  - `filetree.py`: File tree structure management
  - `selector.py`: Interactive file selection UI
  - `output.py`: Output format management
  - `dependency.py`: Project dependency analysis
  - `cli.py`: Command line interface
  - `codeselect.py`: Simple entry point script

### 🔧 Refactoring
- Improved code organization with proper separation of concerns
- Better isolation of functionality into single-responsibility modules
- Enhanced readability through clear module boundaries
- No functional changes to existing behavior

### 🧪 Testing
- Added unit tests for all new modules
- Test coverage for core functionality

### 📖 Documentation
- Updated project_structure.md to reflect new modular architecture
- Added detailed documentation to each module
- Included Korean comments for core functionality