# Change Log

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