# `.gitignore` 지원 기능 구현

## 📝 작업 개요
프로젝트에서 `.gitignore` 파일을 자동으로 파싱하여 해당 패턴에 맞는 파일과 디렉토리를 파일 트리 구성 시 제외하는 기능을 구현했습니다.

## 🛠️ 구현 내용

### 1. `.gitignore` 패턴 로딩 기능 (`utils.py`)
- `load_gitignore_patterns(directory)` 함수 추가
- `.gitignore` 파일에서 유효한 패턴만 추출 (주석 및 빈 줄 제외)
- 파일이 존재하지 않을 경우 빈 리스트 반환

```python
def load_gitignore_patterns(directory):
    """
    Reads `.gitignore` file and returns a list of valid ignore patterns.

    Args:
        directory (str): The directory containing the .gitignore file.

    Returns:
        list: List of ignore patterns from the .gitignore file.
    """
    gitignore_path = os.path.join(directory, ".gitignore")
    if not os.path.isfile(gitignore_path):
        return []
    
    patterns = []
    with open(gitignore_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith("#"):
                patterns.append(line)
    
    return patterns
```

### 2. 패턴 매칭 알고리즘 개선 (`utils.py`)
- `should_ignore_path` 함수 개선
- `.gitignore` 스타일 패턴 지원:
  - 제외 패턴 (`!pattern`)
  - 디렉토리 특정 패턴 (`dir/`)
  - 와일드카드 패턴 (`*.log`)
- 파일 이름 및 전체 경로 매칭 지원

```python
def should_ignore_path(path, ignore_patterns=None):
    """
    Checks if the given path matches a pattern that should be ignored.
    Implements basic .gitignore style pattern matching.

    Args:
        path (str): The path to the file or directory to check.
        ignore_patterns (list): List of patterns to ignore (default: None)

    Returns:
        Bool: True if the path should be ignored, False otherwise.
    """
    # 패턴 처리 로직 구현
    # ...
```

### 3. 파일 트리 생성 시 `.gitignore` 통합 (`filetree.py`)
- `build_file_tree` 함수 개선
- 기본 무시 패턴과 `.gitignore` 패턴 결합
- 전체 경로 기반 필터링으로 변경

```python
def build_file_tree(root_path, ignore_patterns=None):
    """
    Constructs a tree representing the file structure.

    Args:
        root_path (str): Path to the root directory.
        ignore_patterns (list, optional): List of patterns to ignore.

    Returns:
        Node: the root node of the file tree.
    """
    # 기본 패턴 정의
    default_patterns = ['.git', '__pycache__', '*.pyc', '.DS_Store', '.idea', '.vscode']
    
    # .gitignore 패턴 로드
    gitignore_patterns = load_gitignore_patterns(root_path)
    
    # 패턴 결합
    if ignore_patterns is None:
        ignore_patterns = default_patterns + gitignore_patterns
    else:
        ignore_patterns = ignore_patterns + gitignore_patterns
    
    # 파일 필터링 로직
    # ...
```

### 4. 테스트 케이스 추가
- `.gitignore` 패턴 로딩 테스트 (`test_utils.py`)
- 파일 필터링 동작 테스트 (`test_filetree.py`)
- 다양한 패턴 유형에 대한 테스트

## 📊 개선 효과
1. **자동화된 파일 필터링**: 사용자가 별도의 설정 없이 프로젝트의 `.gitignore` 규칙을 자동으로 적용
2. **정확한 파일 경로 매칭**: 전체 경로 및 파일 이름 기반 매칭으로 필터링 정확도 향상
3. **다양한 패턴 지원**: 여러 패턴 유형을 지원하여 유연한 파일 필터링 가능
4. **코드 가독성 향상**: 패턴 로딩 및 매칭 로직을 별도 함수로 분리하여 유지보수성 개선

## 🔍 후속 개선 사항
- 하위 디렉토리의 `.gitignore` 파일도 지원 (Git 원래 동작 방식과 유사하게)
- 패턴 매칭 성능 최적화 (대규모 프로젝트에서의 속도 개선)
- CLI를 통한 `--include`/`--exclude` 옵션 구현
