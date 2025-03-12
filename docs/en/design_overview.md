# Design overview

## 🎯 Key design principles
1. Simplicity: Users should be able to select and easily share files within a project with a single command.
2. **Interactivity**: Provide a Curses-based UI to make file selection intuitive.
3. Extensibility: Design to allow for the addition of different file selection methods and output formats.
4. Minimal Dependencies: Uses only standard libraries to run without additional installations.
5. Familiar UX: Borrow controls from popular tools like Vim to minimise the learning curve.
6. **Separation of Concerns**: Improve maintainability and scalability with a clear separation of responsibilities between modules.

## 🏛 System Architecture
CodeSelect consists of three main modules: **File Tree Generator**, **Interactive File Selector**, and **Output Generator**.

### 📂 Main Modules
1. file tree generator (`build_file_tree`)
   - Scans the project directory and generates a file tree.
   - Filters out unnecessary files based on `.gitignore` and certain patterns.
   - Internally utilises `os.walk()` to traverse the directory structure.

2. Interactive file selectors
   - File Selection Interface (`selector.py`)
     - Initialise and run the selection interface via the `interactive_selection` function.
   - UI component (`selector_ui.py`)
     - Implement a curses-based UI with the `FileSelector` class
     - Includes screen drawing, keystroke handling, and user interface logic
   - Manage actions (`selector_actions.py`)
     - Provides action-related functions for file selection, searching, expanding/contracting, etc.
     - Implements core functions such as `toggle_selection`, `apply_search_filter`, etc.

3. output generator (`write_output_file`)
   - Converts selected files to a specified format (`txt`, `md`, `llm`) and saves them.
   - Analyses dependencies between files and structures them in a way that is easy for LLM to understand.
   - Automatically copies them to the clipboard if necessary for quick sharing.

## 🔄 Data flow
```
User launch → Scan directory → File selection UI → Collect selected files → Save and output files
```
1. **Run user**: Execute `codeselect` command
2. **Directory Scan**: Analyses the entire list of files in the project
3. file selection UI: user selects files in curses UI (browse, search, filter)
4. collect selected files: Collect the required files via `collect_selected_content`.
5. save and output files: convert and save selected files or copy to clipboard

## 🔍 Search and filtering design
The search function is designed with the following flow

1. **Enter search mode**: Activate search mode via `/` key
2. support for regular expressions: process user input into regular expressions to support powerful filtering
3. preserves tree structure: shows directory hierarchy even in search results
   - All parent directories of matched files are displayed
4. unfiltering: restore to full list via ESC key

## 🔄 Interaction between modules
Interaction between the file selection modules is done as follows:

1. **External interface (`selector.py`)**.
   - UI initialisation and execution via `interactive_selection` function
   - Setting up the terminal environment using `curses.wrapper`.

2. the UI module (`selector_ui.py`)
   - The `FileSelector` class is in charge of interacting with the user
   - It takes keystrokes and calls the appropriate action function

3. actions module (`selector_actions.py`)
   - Performs the actions requested by the UI module (select, search, expand/collapse)
   - Returns the result of the action to the UI module and reflects it on the screen

## ⚙️ Design considerations
- Performance optimisation: Optimise `os.walk()` for fast file navigation even in large projects.
- Extensibility: Maintain a modularised structure to support different project structures in the future.
- Improved user experience: intuitive UI and automatic filtering of unnecessary files.
- Vim-friendly: borrowing keybindings from the popular Vim to lower the learning curve.
- Separation of concerns: Improved code readability and maintainability by separating UI and behavioural logic.

## 🔍 Future improvements
- Add advanced filtering options: support for including/excluding certain extensions
- Deepen project dependency analysis**: More accurate analysis of `import` and `require` relationships, etc.
- Support for multiple output formats: consider additional support for JSON, YAML, etc.
- Search history management: support for storing and easily accessing previous searches
- Plugin system: consider introducing a plugin architecture to add custom behaviour