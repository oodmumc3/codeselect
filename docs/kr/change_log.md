# Change Log

## v1.3.0 (2025-03-12)

### 🚀 `.gitignore` 지원 기능 추가
- `.gitignore` 파일 자동 인식 및 패턴 처리 기능 구현
- 다양한 `.gitignore` 패턴 지원
  - 와일드카드 패턴 (`*.log`)
  - 디렉토리 특정 패턴 (`ignored_dir/`)
  - 제외 패턴 (`!important.log`)
- 기존 하드코딩 된 무시 목록에 .gitignore 패턴 통합

### 💻 파일 필터링 개선
- 파일 경로 비교 알고리즘 향상
- 전체 경로와 기본 이름 모두 패턴 매칭 지원
- 하위 디렉토리 내 파일에 대한 필터링 정확도 향상

### 🧪 테스트
- `.gitignore` 관련 단위 테스트 추가
- 패턴 로딩 기능 테스트
- 파일 필터링 정확도 테스트

## v1.2.0 (2025-03-12)

### 🏗 코드 구조 개선
- `selector.py` 모듈을 세 개의 모듈로 분리하여 가독성 및 유지보수성 향상
  - `selector_actions.py`: 파일 선택, 검색, 확장/축소 동작 관련 함수들
  - `selector_ui.py`: 사용자 인터페이스 관련 `FileSelector` 클래스
  - `selector.py`: 외부 인터페이스 역할의 `interactive_selection` 함수

### 💻 리팩토링 이점
- 관심사 분리: UI 코드와 동작 로직 간의 명확한 분리
- 테스트 용이성: 각 모듈을 독립적으로 테스트 가능
- 확장성: 새로운 동작이나 UI 요소를 더 쉽게 추가 가능

### 🧪 테스트
- 분리된 모든 모듈에 대한 단위 테스트 추가
- 기존 기능과의 호환성 유지 확인

### 📖 문서화
- 프로젝트 구조 문서 업데이트
- 설계 개요 문서에 모듈 분리 내용 반영

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