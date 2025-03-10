# 📌 TODO list

## 🏗 Improve code structure
✅ **Separate and modularise code** (`codeselect.py` single file → multiple modules)
- `codeselect.py` is too big → split into functional modules
- 📂 New module structure
  - `filetree.py`: file tree and navigation
  - `selector.py`: curses-based file selection UI
  - `output.py`: Saving to various formats (txt, md, llm)
  - cli.py`: Handles CLI commands and options
  - `dependency.py`: Analyse dependencies between files in a project

---]

## 🔍 Added filtering and search functions
✅ **Vim-style file search (filtering after entering `/`)**.
- Enter a search term after `/` → show only files containing that keyword
- Regular expression support (`/.*\.py$` → filter only `.py` files)
- Case sensitive option (`/foo` vs `/Foo`)

✅ **More sophisticated `.gitignore` and filtering support**.
- Automatically reflect `.gitignore` to determine which files to ignore
- Added `--include` and `--exclude` CLI options (e.g. `--include ‘*.py’ --exclude ‘tests/’`)

✅ **Support for project-specific configuration files (`.codeselectrc`)
- Save `.codeselectrc` file in project root to auto-load settings
- JSON/YAML support (e.g. `include=[‘*.py’], exclude=[‘node_modules/’]`)

---]

## 🛠 Performance optimisations and UI improvements
✅ **Navigation speed optimisation
- Change `os.walk()` → `scandir()` to speed things up
- Consider introducing multi-threaded or asynchronous processing (to support large projects)

✅ **Instant selection when searching**.
- Select files with `Enter` directly after searching `/`
- Parallel support with the existing `Space` selection method

✅ Highlight selected files during navigation
- Fixed or separate colour highlighting of the currently selected file at the top

History of recently used files/directories
- Save `.codeselect_history` file to keep recently selected files

---]

## 🚀 CLI Options Improvements
✅ **Automatic run mode (`--auto-select`)**
- Automatically select a specific file and run it without UI (`codeselect --auto-select ‘*.py’`)

✅ **Result preview (`--preview`)**
- Adds the ability to preview the contents of selected files

✅ **Extended output format
- Currently support `txt`, `md`, `llm` → add support for `json`, `yaml`

✅ **Automatically copy clipboard option**.
- Added `--no-clipboard` option to turn off auto-copy function

---]

## 📄 Documentation
✅ Created `project_structure.md` (describes project structure)
✅ Create `design_overview.md` (describe the design overview)
✅ Create `usage_guide.md` (usage guide)
✅ Create `file_selection.md` (describes file selection logic)
✅ Create `dependency_analysis.md` (dependency analysis document)
✅ Create `output_formats.md` (describes output data formats)

---]

### 🏁 **Organise your priorities**.
🚀 **Add `1️⃣ Vim-style `/` search function** (top priority)  
📌 **2️⃣ code structure improvement and modularisation** (`codeselect.py` → split into multiple files)  
⚡ **3️⃣ Optimised navigation speed and improved UI** (priority)  
📦 **4️⃣ support for `.codeselectrc` configuration files**.  
📜 **5️⃣ output formats extended (added support for `json`, `yaml`)**  


---]

# Completed tasks
