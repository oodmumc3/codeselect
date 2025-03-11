# Change Log

## v1.1.0 (2024-03-12)

### 🔍 Added Vim-style search function
- Support for search mode via `/` key (Vim style)
- full support for regular expression search (e.g. `/.*\.py$`, `/test_.*`)
- Case-sensitive toggle functionality (using the `^` key)
- Maintain tree structure in search results - show directory hierarchy
- Ability to restore full list with ESC key after searching
- Ability to select/deselect files from search results

### 🚀 Added Vim-style navigation
- Move up and down with `j` / `k` keys
- Close/open folders (and go to parent directory) with `h` / `l` keys
- Parallel support with existing arrow key navigation

### 🎨 UI improvements
- improved search result status display (currently displayed files / total number of files)
- change status bar in search mode
- Show notification when there are no search results

### 💻 Quality improvements
- Improved tree structure maintenance algorithm
- Optimised status management when cancelling/completing a search
- Improved error handling (show error when entering invalid regex)

## v1.0.0 (2024-03-11)

### 🏗 Code Structure Improvements
- CodeSelect has been modularized for better maintainability and future extensibility
- Separated monolithic codeselect.py into focused modules:
  - `utils.py`: Common utility functions
  - `filetree.py`: File tree structure management
  - `selector.py`: Interactive file selection UI
  - `output.py`: Output format management
  - Future modules in development: dependency.py, cli.py

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