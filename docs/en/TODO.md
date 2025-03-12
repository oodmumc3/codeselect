# 📌 TODO list

~~✅ **Support for more sophisticated `.gitignore` and filtering**~~ (Done)
- Automatically reflect `.gitignore` to determine which files to ignore~~ (DONE)
- Added `--include` and `--exclude` CLI options (e.g. `--include ‘*.py’ --exclude ‘tests/’`)

✅ **Support for project-specific configuration files (`.codeselectrc`)
- Save `.codeselectrc` file in project root to auto-load settings
- JSON/YAML support (e.g. `include=[‘*.py’], exclude=[‘node_modules/’]`)

---

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

✅ **Optimise file tree navigation
- Improved performance by utilising `os.scandir()` instead of `os.walk()`.
- Improved speed of `.gitignore` and filtering

File tree asynchronous processing
- Considered introducing `asyncio`-based asynchronous directory traversal
- Quickly build file trees, even for large projects

✅ **Flexible filtering support
- Improved `.gitignore‘ to allow additional filtering settings in `.codeselectrc’ in addition to `.gitignore'

---
## 🚀 Improved CLI options
✅ **Automatic execution mode (`--auto-select`)
- Automatically select specific files and run them without UI (`codeselect --auto-select ‘*.py’`)

✅ **Preview results (`--preview`)**
- Adds the ability to preview the contents of selected files

✅ **Extended output format
- Currently support `txt`, `md`, `llm` → add support for `json`, `yaml`

✅ **Automatically copy clipboard option**.
- Added `--no-clipboard` option to turn off auto-copy function

---

## 📄 Documentation
✅ Created `project_structure.md` (describes project structure)
✅ Create `design_overview.md` (describe the design overview)
✅ Create `usage_guide.md` (usage guide)
✅ Create `file_selection.md` (describes file selection logic)
✅ Create `dependency_analysis.md` (dependency analysis document)
✅ Create `output_formats.md` (describes output data formats)

---]
### 🏁 **Prioritise**
~~🚀 **Add `1️⃣ Vim-style `/` search function** (top priority)~~ (done)
~~📌 **Improve and modularise code structure of 2️⃣ (`codeselect.py` → split into multiple files)~~ (Done)
~~🔍 **Added **3️⃣ `.gitignore` support** (improved file filtering)~~ (Done)
⚡ **4️⃣ navigation speed optimisation and UI improvements** (Done)
📦 **5️⃣ `.codeselectrc` configuration file support** (improved filtering)
📜 **6️⃣ output format extended (added `json`, `yaml` support)**


---

# Completed tasks

~~## 🏗 Improved code structure~~.
✅ **Separate and modularise code** (`codeselect.py` single file → multiple modules)
- `codeselect.py` is too bloated → split into functional modules
- 📂 **New module structure** ✅ **New module structure
  - `filetree.py`: file tree and navigation
  - `selector.py`: curses-based file selection UI
  - `output.py`: Saving to various formats (txt, md, llm)
  - cli.py`: Handles CLI commands and options
  - `dependency.py`: Analyses dependencies between files in a project

~~## 🔧 Support for `.gitignore`-based file filtering~~
✅ **Automatically parse and filter `.gitignore` files**.
- Automatic detection of `.gitignore` files in the project root
- Support for different pattern types:
  - Wildcard pattern (`*.log`)
  - Directory-specific pattern (`ignored_dir/`)
  - Exclusion pattern (`!important.log`)
- Added pattern loading and parsing functionality to `utils.py`
- Improved file path matching algorithm
- Added tests (pattern loading, file filtering)

~~## 🔍 Added Vim-style file searching~~
✅ **Implemented Vim-style search (search after `/` input)**.
- Enter search mode with `/` key, type search term and hit enter to execute search
- Support for regular expressions (e.g. `/.*\.py$` → search only .py files)
- Case-sensitive toggle function (using the `^` key)
- Preserves tree structure in search results

Implemented **Vim-style navigation**.
- Move up/down with `j/k` keys
- Close/open folders with `h/l` keys
- Restore full list with ESC key in search mode

---