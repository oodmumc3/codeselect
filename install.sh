#!/bin/bash
# Installation script for CodeSelect - no admin privileges required

set -e

echo "Installing CodeSelect..."

# Determine installation directory
USER_BIN="$HOME/.local/bin"
mkdir -p "$USER_BIN"

# Create CodeSelect directory
CODESELECT_DIR="$HOME/.local/lib/codeselect"
mkdir -p "$CODESELECT_DIR"

# 필요한 모듈 파일 다운로드 또는 복사
echo "Installing CodeSelect modules..."
MODULES=("codeselect.py" "cli.py" "utils.py" "filetree.py" "selector.py" "selector_ui.py" "selector_actions.py" "output.py" "dependency.py")

for MODULE in "${MODULES[@]}"; do
  echo "Installing $MODULE..."
  curl -fsSL "https://raw.githubusercontent.com/maynetee/codeselect/main/$MODULE" -o "$CODESELECT_DIR/$MODULE" 2>/dev/null || {
    # curl이 실패하면 로컬 파일에서 복사
    if [ -f "$MODULE" ]; then
      cp "$MODULE" "$CODESELECT_DIR/$MODULE"
    else
      echo "Error: Cannot download or find $MODULE"
      exit 1
    fi
  }
done

# Create executable wrapper script
CODESELECT_PATH="$USER_BIN/codeselect"
cat > "$CODESELECT_PATH" << 'EOF'
#!/bin/bash
# This wrapper script ensures that the python script is run from its installation
# directory, which allows all of its internal imports to work correctly.

SCRIPT_DIR="$HOME/.local/lib/codeselect"

# Use a subshell to change directory, so it doesn't affect the user's terminal.
# All command-line arguments ("$@") are forwarded to the python script.
(cd "$SCRIPT_DIR" && python3 codeselect.py "$@")
EOF

# Make the script executable
chmod +x "$CODESELECT_PATH"

# Check if the directory is in PATH
if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
    # Determine shell config file
    SHELL_CONFIG=""
    if [[ "$SHELL" == *"zsh"* ]]; then
        SHELL_CONFIG="$HOME/.zshrc"
    elif [[ "$SHELL" == *"bash"* ]]; then
        if [[ "$(uname)" == "Darwin" ]] && [[ ! -f "$HOME/.bashrc" ]]; then
            SHELL_CONFIG="$HOME/.bash_profile"
        else
            SHELL_CONFIG="$HOME/.bashrc"
        fi
    elif [[ "$SHELL" == *"fish"* ]]; then
        FISH_CONFIG_DIR="$HOME/.config/fish"
        mkdir -p "$FISH_CONFIG_DIR"
        SHELL_CONFIG="$FISH_CONFIG_DIR/config.fish"
        # Fish 쉘은 다른 문법을 사용합니다
        echo "set -gx PATH \$HOME/.local/bin \$PATH" >> "$SHELL_CONFIG"
        echo "Added $USER_BIN to your PATH in $SHELL_CONFIG"
        echo "To use immediately, run: source $SHELL_CONFIG"
    else
        SHELL_CONFIG="$HOME/.profile"
    fi

    # Add to PATH (fish 쉘이 아닌 경우)
    if [[ "$SHELL" != *"fish"* ]]; then
        echo '' >> "$SHELL_CONFIG"
        echo '# Add CodeSelect to PATH' >> "$SHELL_CONFIG"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG"
        echo "Added $USER_BIN to your PATH in $SHELL_CONFIG"
        echo "To use immediately, run: source $SHELL_CONFIG"
    fi
fi

echo "
Installation complete!

Usage:
  codeselect                 # Analyze current directory
  codeselect /path/to/project  # Analyze a specific directory
  codeselect --help          # Show help

Features:
  - Automatically respects .gitignore patterns in your project
  - Interactive file selection with tree view
  - Multiple output formats for different AI assistants

CodeSelect is now installed at: $CODESELECT_PATH
All modules installed at: $CODESELECT_DIR
"

# Try to add tab completion for bash
if [[ "$SHELL" == *"bash"* ]]; then
    COMPLETION_DIR="$HOME/.local/share/bash-completion/completions"
    mkdir -p "$COMPLETION_DIR"
    cat > "$COMPLETION_DIR/codeselect" << 'EOF'
_codeselect_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Basic options
    opts="--format --output --skip-selection --no-clipboard --version --help"

    # Handle specific options
    case "${prev}" in
        --format|-f)
            COMPREPLY=( $(compgen -W "txt md llm" -- "${cur}") )
            return 0
            ;;
        --output|-o)
            COMPREPLY=( $(compgen -f -- "${cur}") )
            return 0
            ;;
        *)
            ;;
    esac

    # Complete options or directories
    if [[ ${cur} == -* ]]; then
        COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
    else
        COMPREPLY=( $(compgen -d -- "${cur}") )
    fi
    return 0
}

complete -F _codeselect_completion codeselect
EOF
    echo "Added bash tab completion for CodeSelect"
fi

exit 0