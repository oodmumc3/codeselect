# 📂 **Project Structure (`codeselect`)**

## 🏗️ **Folder & File Overview**
```
codeselect/
  ├── codeselect.py        # Main execution script (CLI entry point)
  ├── cli.py               # CLI command processing & execution flow control
  ├── filetree.py          # File tree exploration & hierarchical structure management
  ├── selector.py          # File selection interface (entry point)
  ├── selector_ui.py       # curses-based UI implementation (`FileSelector` class)
  ├── selector_actions.py  # Functions related to file selection actions
  ├── output.py            # Outputs selected files (supports txt, md, llm formats)
  ├── dependency.py        # Analyzes file dependencies (import/include detection)
  ├── utils.py             # Utility functions (path handling, clipboard copy, etc.)
  ├── install.sh           # Project installation script
  ├── uninstall.sh         # Project uninstallation script
  ├── tests/               # Unit test folder
  │   ├── test_filetree.py         # Tests for file tree generation
  │   ├── test_selector.py         # Tests for file selection interface
  │   ├── test_selector_actions.py # Tests for file selection actions
  │   ├── test_selector_ui.py      # Tests for UI components
  │   └── test_dependency.py       # Tests for dependency analysis
  ├── docs/                # Documentation folder (architecture, usage guide, etc.)
```

---

## 🛠️ **Core Modules Explanation**

### 1️⃣ `codeselect.py` (Program Execution Entry Point)
- Calls `cli.py` to run the program.
- Uses `argparse` to parse CLI options, then:
  - Calls `filetree.py` to explore files.
  - Runs `selector.py` for interactive selection.

### 2️⃣ `cli.py` (CLI Commands & Execution Flow Management)
- Processes CLI arguments (`--format`, `--skip-selection`, etc.).
- Calls `filetree.build_file_tree()` to generate the file list.
- Runs `selector.interactive_selection()` to open the UI for file selection.
- Calls `dependency.analyze_dependencies()` for dependency analysis.
- Saves the results using `output.write_output_file()`.

### 3️⃣ `filetree.py` (File Tree Exploration & Management)
- `build_file_tree(root_path)`: Analyzes directories and files to build a hierarchical tree.
- `flatten_tree(node)`: Converts the tree into a list for easier UI navigation.

### 4️⃣ File Selection Modules (Split into Three Files)
#### a. `selector.py` (External Interface)
- `interactive_selection(root_node)`: Initializes the curses environment and runs `FileSelector`.
- Acts as a simple entry point interface for external modules.

#### b. `selector_ui.py` (UI Components)
- `FileSelector` class: Implements a curses-based interactive UI.
- Handles screen rendering, key inputs, and user interface logic.
- Key functions:
  - `run()`: Runs the selection interface loop.
  - `draw_tree()`: Displays the file tree structure.
  - `process_key()`: Handles user key inputs.

#### c. `selector_actions.py` (Action Functions)
- `toggle_selection(node)`: Toggles file/folder selection.
- `toggle_expand(node)`: Expands/collapses directories.
- `apply_search_filter()`: Applies search filtering.
- `select_all()`: Selects/deselects all files.
- `toggle_current_dir_selection()`: Selects/deselects files only in the current directory.

### 5️⃣ `dependency.py` (Dependency Analysis)
- `analyze_dependencies(root_path, file_contents)`: Analyzes `import`, `require`, and `include` patterns to extract file dependency relationships.
- Supports multiple languages: Python, JavaScript, C/C++, etc.

### 6️⃣ `output.py` (Output File Handling)
- `write_output_file(output_path, format)`: Saves selected files in various formats (`txt`, `md`, `llm`).
- The `llm` format structures the data for AI model compatibility.

### 7️⃣ `utils.py` (Utility Functions)
- `generate_output_filename(root_path, format)`: Automatically generates output file names.
- `try_copy_to_clipboard(content)`: Copies selected file content to the clipboard.
- `load_gitignore_patterns(directory)`: Loads and parses `.gitignore` patterns.
- `should_ignore_path(path, ignore_patterns)`: Checks if a file path matches ignore patterns.

---

## 🚀 **Execution Flow Summary**
1️⃣ `codeselect.py` runs → `cli.py` parses arguments.  
2️⃣ `filetree.py` generates the file tree.  
3️⃣ `selector.py` initializes the curses environment.  
4️⃣ `selector_ui.py` runs `FileSelector` for interactive selection.  
5️⃣ `selector_actions.py` processes user actions.  
6️⃣ `dependency.py` analyzes file dependencies.  
7️⃣ `output.py` saves selected files and copies content to the clipboard.  