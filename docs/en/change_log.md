# Change Log

## v1.3.0 (2025-03-12)

### 🚀 Added `.gitignore` support
- Implemented automatic recognition of `.gitignore` files and pattern processing
- Supports various `.gitignore` patterns
  - Wildcard pattern (`*.log`)
  - Directory-specific pattern (`ignored_dir/`)
  - Exclusion pattern (`!important.log`)
- Integration of .gitignore patterns into existing hardcoded ignore lists

### 💻 Improved file filtering
- Improved file path comparison algorithm
- Support pattern matching both full paths and base names
- Improved filtering accuracy for files in subdirectories

### 🧪 Testing
- Added `.gitignore` related unit tests
- Tested pattern loading functionality
- Test file filtering accuracy

## v1.2.0 (2025-03-12)

### 🏗 Code structure improvements
- Split `selector.py` module into three modules to improve readability and maintainability
  - `selector_actions.py`: functions related to file selection, search, and expand/collapse actions
  - `selector_ui.py`: user interface related `FileSelector` classes
  - `selector.py`: `interactive_selection` function in the role of external interface

### 💻 Refactoring benefits
- Separation of concerns: clear separation between UI code and behavioural logic
- Ease of testing: each module can be tested independently
- Extensibility: Easier to add new behaviours or UI elements

### 🧪 Testing
- Add unit tests for all separated modules
- Ensure compatibility with existing functionality

### 📖 Documentation
- Update project structure documentation
- Reflect module separation in design overview documentation

## v1.1.0 (12-03-2024)

### 🔍 Added Vim-style search functionality
- Support for search mode via `/` keys (Vim style)
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
- Improved error handling (display error when incorrect regex is entered)

## v1.0.0 (11-03-2024)

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
- Improved code organisation with proper separation of concerns
- Better isolation of functionality into single-responsibility modules
- Enhanced readability through clear module boundaries
- No functional changes to existing behaviour

### 🧪 Testing
- Added unit tests for all new modules
- Test coverage for core functionality

### 📖 Documentation
- Updated project_structure.md to reflect new modular architecture
- Added detailed documentation to each module
- Included Korean comments for core functionality