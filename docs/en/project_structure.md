# 📂 Project structure (`codeselect`)

## 🏗️ **Overview of folders and files**.
```
codeselect/
  ├── codeselect.py # Main executable script (CLI entry point)
  ├── cli.py # CLI command processing and execution flow control
  ├── filetree.py # File tree navigation and hierarchy management
  ├── selector.py # curses-based file selection UI
  ├── output.py # Output of selected files (txt, md, llm supported)
  ├── dependency.py # Analyse dependencies between files (import/include detection)
  utils.py # Common utility functions (path handling, clipboard copy, etc.)
  install.sh # Project installation script
  uninstall.sh # project uninstall script
  tests/ # Unit test folder
  docs/ # documentation folder (design overview, usage, etc.)
  └── .codeselectrc # customisation files (filtering, output settings)
```

## 🛠️ **Core module descriptions

### 1️⃣ `codeselect.py` (entry point to run the programme)
- Call `cli.py` to run the programme
- Parse CLI options with `argparse`, browse files with `filetree.py` and run selector UI with `selector.py`.

### 2️⃣ `cli.py` (manages CLI commands and execution flow)
- Handle command arguments (`--format`, `--skip-selection`, etc.)
- Create a list of files by calling `filetree.build_file_tree()`.
- Run `selector.interactive_selection()` to select files in the UI
- Perform dependency analysis by calling `dependency.analyse_dependencies()`.
- Finally, save the results with `output.write_output_file()`.

### 3️⃣ `filetree.py` (File tree navigation and management)
- build_file_tree(root_path)`: Hierarchically analyse files and folders inside a directory to create a tree structure.
- flatten_tree(node)`: Converts a tree into a list for easy navigation in the UI.

### 4️⃣ `selector.py` (file selector UI)
- Class `FileSelector`: provides an interactive UI based on curses
- run()`: Run the file selection interface
- toggle_selection(node)`: Toggle file selection/deselection with space key

### 5️⃣ `dependency.py` (dependency analysis)
- analyse_dependencies(root_path, file_contents)`: Analyse `import`, `require`, `include` patterns to extract reference relationships between files
- Supports languages such as Python, JavaScript, C/C++, etc.

### 6️⃣ `output.py` (save output file)
- write_output_file(output_path, format)`: converts the selected file to various formats (txt, md, llm) and saves it.
- The `llm` format is processed into a structure that is easier for AI models to understand.

### 7️⃣ `utils.py` (utility functions)
- generate_output_filename(root_path, format)`: generate output filename automatically
- `try_copy_to_clipboard(content)`: copy selected file contents to clipboard

### 8️⃣ `tests/` (test code)
- `filetree_test.py`: Test file tree generation
- `selector_test.py`: Test file selector UI
- `dependency_test.py`: dependency analysis test

---
## 🚀 **Summary of the execution flow**.
Run 1️⃣ `codeselect.py` → parse arguments in `cli.py`
Create a file tree at 2️⃣ `filetree.py`
Run curses UI in 3️⃣ `selector.py` (select a file)
4️⃣ Analyse dependencies between files in `dependency.py`
5️⃣ `output.py` to save and clipboard copy selected files