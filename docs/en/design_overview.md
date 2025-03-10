# Design overview

## 🎯 Key design principles
1. Simplicity: Users should be able to select and easily share files within a project with a single command.
2. **Interactivity**: Provide a Curses-based UI to make file selection intuitive.
3. Extensibility: Design to allow for the addition of different file selection methods and output formats.
4. Minimal Dependencies: Use only standard libraries to run without additional installations.

## 🏛 System Architecture
CodeSelect consists of three main modules: **File Tree Generator**, **Interactive File Selector**, and **Output Generator**.

### 📂 Main Modules
1. file tree generator (`build_file_tree`)
   - Scans the project directory and generates a file tree.
   - Filters out unnecessary files based on `.gitignore` and certain patterns.
   - Internally utilises `os.walk()` to traverse the directory structure.

2. **Interactive file selector (`FileSelector`)**.
   - Uses a `curses`-based terminal UI to display a file tree to the user.
   - The user can expand folders or select files via keyboard input.
   - Save selected files as `collect_selected_content` to utilise in later steps.

3. **Output generator (`write_output_file`)
   - Converts the selected files to the specified format (`txt`, `md`, `llm`) and saves them.
   - Analyses dependencies between files and structures them in a way that is easy for LLM to understand.
   - Automatically copies them to the clipboard if necessary for quick sharing.

## 🔄 Data flow
```
Run user → Scan directory → File selection UI → Collect selected files → Save and output files
```
1. **Execute user**: Execute `codeselect` command
2. **Directory Scan**: Analyses the entire list of files in the project
3. file select UI: user selects files in curses UI
4. collect selected files: Collect required files via `collect_selected_content`.
5. save and output files: convert and save selected files or copy to clipboard

## ⚙️ Design considerations
- Performance optimisation: Optimise `os.walk()` for fast file navigation even in large projects.
- Extensibility: Maintain a modularised structure to support different project structures in the future.
- User experience improvements: intuitive UI and automatic filtering of unnecessary files.

## 🔍 Future improvements.
- Add advanced filtering options: support for including/excluding specific extensions.
- Deepen project dependency analysis: More accurate analysis of `import` and `require` relationships.
- Support for multiple output formats: consider additional support for JSON, YAML, etc.