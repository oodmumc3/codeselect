# Project structure

## 📂 Root directory

```
codeselect/
│── codeselect.py # Main script to select files
│── utils.py      # Utility functions
│── filetree.py   # File tree structure management
│── selector.py   # Interactive file selection UI
│── output.py     # Output format management
│── dependency.py # Dependency analysis (WIP)
│── cli.py        # Command line interface (WIP)
│── install.sh    # Installation script
│── uninstall.sh  # Uninstall script
│── README.md     # Project documentation file
```

## 📄 Main files

- `codeselect.py`: The main script of the project, responsible for orchestrating all components.
- `utils.py`: Common utility functions like language mapping, clipboard operations, and filename generation.
- `filetree.py`: Manages file tree structure, providing node representation and content collection.
- `selector.py`: Provides a curses-based interactive file selection UI.
- `output.py`: Manages output formats (txt, md, llm).
- `dependency.py`: Analyzes dependencies between project files.
- `cli.py`: Handles command line arguments processing.
- `install.sh`: Shell script to install `CodeSelect`, placing the executable in the user's home directory.
- `uninstall.sh`: Shell script to uninstall `CodeSelect` from the system.
- `README.md`: A document describing the project overview and usage.

## 🏗 Current Modularization Progress

### Completed Modules

1. **utils.py**
   - Provides utility functions including `get_language_name()`, `try_copy_to_clipboard()`, `generate_output_filename()`, and `should_ignore_path()`.
   - Handles common operations used across the application.

2. **filetree.py**
   - Implements the `Node` class for file/directory representation.
   - Provides functions to build and traverse file trees.
   - Handles file content collection via `collect_selected_content()` and `collect_all_content()`.

3. **selector.py**
   - Implements the `FileSelector` class for the interactive curses-based UI.
   - Provides functions for selecting, navigating, and manipulating the file tree.
   - Handles user keyboard input and screen display.

4. **output.py**
   - Handles different output formats (txt, md, llm).
   - Includes functions for writing file tree structure and content.
   - Provides specialized formatting for different output purposes.
   - Contains `write_file_tree_to_string()`, `write_output_file()`, `write_markdown_output()`, and `write_llm_optimized_output()` functions.

### Completed Modules (Continued)

5. **dependency.py**
   - Analyzes relationships between project files.
   - Detects imports and references across multiple programming languages.
   - Provides insights about internal and external dependencies.
   - Contains `analyze_dependencies()` function to map references between project files.

6. **cli.py** (Upcoming)
   - Will handle command line argument parsing.
   - Will provide interface to various program options.
   - Will organize the main execution flow.

7. **codeselect.py** (To be refactored)
   - Will be streamlined to import and coordinate between modules.
   - Will serve as the entry point for the application.

## 📑 Future improvements.

- **Customised ignore patterns:** Support for users to set additional file exclusion rules.
- **Dependency mapping:** Better detection of internal and external dependencies.
- **UI navigation enhancements:** Improved search and filtering capabilities to optimise the file selection process.
- **Vim-style search functionality:** Allow searching for files using keyboard shortcuts.
- **Support for project configuration files:** Add `.codeselectrc` for project-specific settings.
- **Additional output formats:** Add support for JSON, YAML, and other formats.