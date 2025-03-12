# 📂 **Project Structure (`codeselect`)**

## 🏗️ **Folder and File Overview**
```
codeselect/
  ├── codeselect.py        # Main execution script (CLI entry point)
  ├── cli.py               # Handles CLI commands and execution flow
  ├── filetree.py          # Manages file tree exploration and hierarchy
  ├── selector.py          # Entry point for the file selection interface
  ├── selector_ui.py       # Curses-based UI implementation (FileSelector class)
  ├── selector_actions.py  # Collection of functions for file selection actions
  ├── output.py            # Handles output of selected files (txt, md, llm formats)
  ├── dependency.py        # Analyzes file dependencies (import/include search)
  ├── utils.py             # Common utility functions (path handling, clipboard copy, etc.)
  ├── install.sh           # Project installation script
  ├── uninstall.sh         # Project uninstallation script
  ├── tests/               # Unit test directory
  │   ├── test_filetree.py         # Tests for file tree generation
  │   ├── test_selector.py         # Tests for file selection interface
  │   ├── test_selector_actions.py # Tests for file selection actions
  │   ├── test_selector_ui.py      # Tests for UI components
  │   └── test_dependency.py       # Tests for dependency analysis
  ├── docs/                # Documentation folder (design overview, usage guide, etc.)
```

## 🛠️ **Core Modules Overview**

### 1️⃣ `codeselect.py` (Program Entry Point)
- Calls `cli.py` to execute the program.
- Parses CLI options using `argparse`, then:
  - Uses `filetree.py` to explore files.
  - Calls `selector.py` to launch the selection UI.

### 2️⃣ `cli.py` (CLI Command and Execution Flow Management)
- Processes command-line arguments (e.g., `--format`, `--skip-selection`).
- Calls `filetree.build_file_tree()` to generate a file list.
- Executes `selector.interactive_selection()` to start the interactive selection UI.
- Calls `dependency.analyze_dependencies()` to analyze dependencies.
- Saves the final selection using `output.write_output_file()`.

### 3️⃣ `filetree.py` (File Tree Exploration and Management)
- `build_file_tree(root_path)`: Analyzes directory structure and builds a hierarchical file tree.
- `flatten_tree(node)`: Converts the tree into a list for easier navigation in the UI.

### 4️⃣ File Selection Modules (Split into Three Files)
#### a. `selector.py` (External Interface)
- `interactive_selection(root_node)`: Initializes the curses environment and runs `FileSelector`.
- Serves as an entry point for external modules.

#### b. `selector_ui.py` (UI Components)
- `FileSelector` class: Implements a curses-based interactive UI.
- Handles rendering, key input, and UI logic.
- Key functions:
  - `run()`: Executes the interactive selection loop.
  - `draw_tree()`: Visualizes the file tree.
  - `process_key()`: Handles key inputs.

#### c. `selector_actions.py` (Action Functions)
- `toggle_selection(node)`: Toggles selection state of a file/folder.
- `toggle_expand(node)`: Expands/collapses directories.
- `apply_search_filter()`: Applies a search filter.
- `select_all()`: Selects/deselects all files.
- `toggle_current_dir_selection()`: Selects/deselects files only in the current directory.

### 5️⃣ `dependency.py` (Dependency Analysis)
- `analyze_dependencies(root_path, file_contents)`: Extracts file references by analyzing `import`, `require`, and `include` patterns.
- Supports multiple languages, including Python, JavaScript, and C/C++.

### 6️⃣ `output.py` (Saving Selected Files)
- `write_output_file(output_path, format)`: Saves selected files in different formats (`txt`, `md`, `llm`).
- The `llm` format is structured for better AI model processing.

### 7️⃣ `utils.py` (Utility Functions)
- `generate_output_filename(root_path, format)`: Automatically generates output file names.
- `try_copy_to_clipboard(content)`: Copies selected content to the clipboard.

---
## 🚀 **Execution Flow Summary**
1️⃣ Run `codeselect.py` → Parse arguments in `cli.py`.  
2️⃣ Generate the file tree using `filetree.py`.  
3️⃣ Initialize the curses environment via `selector.py`.  
4️⃣ `FileSelector` in `selector_ui.py` provides the selection interface.  
5️⃣ Handle user actions via `selector_actions.py`.  
6️⃣ Analyze file dependencies with `dependency.py`.  
7️⃣ Save the selected files and copy content to the clipboard using `output.py`.  