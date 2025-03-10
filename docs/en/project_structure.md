# Project structure

## 📂 Root directory

```
codeselect/
│── codeselect.py # Main script to select files
│── install.sh # Installation script
│── uninstall.sh # Uninstall script
│── README.md # Project documentation file
```

## 📄 Main files

- `codeselect.py`: The main script of the project, responsible for analysing and selecting files.
- install.sh`: Shell script to install `CodeSelect`, placing the executable in the user's home directory.
- uninstall.sh`: Shell script to uninstall `CodeSelect` from the system.
- `README.md`: A document describing the project overview and usage.

## 🏗 Directory Structure

The directory structure is dynamically generated based on your project. When you run `codeselect.py`, it scans the target directory and builds an interface for selecting files.

### Sample project structure

```
my_project/
├── src/
│ ├── main.py
│ ├── utils.py
│ ├── helpers/
│ │ ├── data_processor.py
│ │ ├── config_loader.py
│ └── __init__.py
├── tests/
│ ├── test_main.py
│ ├── test_utils.py
├── README.md
└── requirements.txt
```

### How it works with CodeSelect

- The `codeselect` scans your project and displays it in the form of a file tree.
- The user can select the desired files via the UI.
- Unnecessary files such as `.git/`, `__pycache__/`, `.DS_Store` are automatically excluded.
- The selected files will be output in a specific format (`txt`, `md`, `llm`).

## 📑 Future improvements.

- **Customised ignore patterns:** Support for users to set additional file exclusion rules.
- Dependency mapping:** Better detection of internal and external dependencies.
- UI navigation enhancements:** Improved search and filtering capabilities to optimise the file selection process.