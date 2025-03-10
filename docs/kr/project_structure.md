# 프로젝트 구조

## 📂 루트 디렉터리

```
codeselect/
│── codeselect.py      # 파일을 선택하는 메인 스크립트
│── install.sh         # 설치 스크립트
│── uninstall.sh       # 제거 스크립트
│── README.md          # 프로젝트 문서화 파일
```

## 📄 주요 파일

- `codeselect.py`: 프로젝트의 메인 스크립트로, 파일을 분석하고 선택하는 역할을 담당합니다.
- `install.sh`: `CodeSelect`를 설치하는 쉘 스크립트로, 사용자 홈 디렉터리에 실행 파일을 배치합니다.
- `uninstall.sh`: `CodeSelect`를 시스템에서 제거하는 쉘 스크립트입니다.
- `README.md`: 프로젝트 개요 및 사용법을 설명하는 문서입니다.

## 🏗 디렉터리 구조

디렉터리 구조는 사용자의 프로젝트에 따라 동적으로 생성됩니다. `codeselect.py`를 실행하면 대상 디렉터리를 스캔하고, 파일 선택을 위한 인터페이스를 구축합니다.

### 샘플 프로젝트 구조 예시

```
my_project/
├── src/
│   ├── main.py
│   ├── utils.py
│   ├── helpers/
│   │   ├── data_processor.py
│   │   ├── config_loader.py
│   └── __init__.py
├── tests/
│   ├── test_main.py
│   ├── test_utils.py
├── README.md
└── requirements.txt
```

### CodeSelect와의 연동 방식

- `codeselect`는 프로젝트를 스캔하여 파일 트리 형태로 표시합니다.
- 사용자는 UI를 통해 원하는 파일을 선택할 수 있습니다.
- `.git/`, `__pycache__/`, `.DS_Store`와 같은 불필요한 파일은 자동으로 제외됩니다.
- 선택된 파일은 특정 형식(`txt`, `md`, `llm`)으로 출력됩니다.

## 📑 향후 개선 사항

- **사용자 정의 무시 패턴:** 추가적인 파일 제외 규칙을 사용자가 설정할 수 있도록 지원.
- **의존성 매핑:** 내부 및 외부 종속성을 보다 효과적으로 탐지.
- **UI 탐색 기능 향상:** 검색 및 필터링 기능 개선을 통해 파일 선택 과정 최적화.