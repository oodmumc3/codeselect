#!/bin/bash
# Uninstall script for CodeSelect

echo "Uninstalling CodeSelect..."

# Remove the executable
CODESELECT_PATH="$HOME/.local/bin/codeselect"
if [ -f "$CODESELECT_PATH" ]; then
    rm "$CODESELECT_PATH"
    echo "Removed executable from $CODESELECT_PATH"
else
    echo "Executable not found at $CODESELECT_PATH"
fi

# Remove module directory
CODESELECT_DIR="$HOME/.local/lib/codeselect"
if [ -d "$CODESELECT_DIR" ]; then
    rm -rf "$CODESELECT_DIR"
    echo "Removed module directory from $CODESELECT_DIR"
else
    echo "Module directory not found at $CODESELECT_DIR"
fi

# Remove bash completion if it exists
COMPLETION_FILE="$HOME/.local/share/bash-completion/completions/codeselect"
if [ -f "$COMPLETION_FILE" ]; then
    rm "$COMPLETION_FILE"
    echo "Removed bash completion script"
fi

# Identify shell config file
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
    SHELL_CONFIG="$HOME/.config/fish/config.fish"
else
    SHELL_CONFIG="$HOME/.profile"
fi

# Remove the PATH line from shell config
if [ -f "$SHELL_CONFIG" ]; then
    # Create a backup
    cp "$SHELL_CONFIG" "${SHELL_CONFIG}.bak"

    # Remove the PATH line (fish와 다른 쉘에 따라 다른 처리)
    if [[ "$SHELL" == *"fish"* ]]; then
        grep -v 'set -gx PATH $HOME/.local/bin $PATH' "$SHELL_CONFIG" > "${SHELL_CONFIG}.tmp"
    else
        grep -v 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_CONFIG" > "${SHELL_CONFIG}.tmp"
    fi
    
    mv "${SHELL_CONFIG}.tmp" "$SHELL_CONFIG"
    echo "Removed PATH entry from $SHELL_CONFIG"
    echo "Backup created at ${SHELL_CONFIG}.bak"
fi

echo "
Uninstallation complete!

The following files and directories have been removed:
- Executable: $HOME/.local/bin/codeselect
- Module directory: $HOME/.local/lib/codeselect/
- Bash completion: $HOME/.local/share/bash-completion/completions/codeselect
- PATH entry in shell configuration

Note: You may need to restart your terminal or run:
  source $SHELL_CONFIG
"

exit 0
