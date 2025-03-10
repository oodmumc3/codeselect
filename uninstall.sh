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
else
    SHELL_CONFIG="$HOME/.profile"
fi

# Remove the PATH line from shell config
if [ -f "$SHELL_CONFIG" ]; then
    # Create a backup
    cp "$SHELL_CONFIG" "${SHELL_CONFIG}.bak"

    # Remove the PATH line
    grep -v 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_CONFIG" > "${SHELL_CONFIG}.tmp"
    mv "${SHELL_CONFIG}.tmp" "$SHELL_CONFIG"
    echo "Removed PATH entry from $SHELL_CONFIG"
    echo "Backup created at ${SHELL_CONFIG}.bak"
fi

echo "
Uninstallation complete!

Note: You may need to restart your terminal or run:
  source $SHELL_CONFIG

If you installed CodeSelect as the only tool in ~/.local/bin,
you can also delete this directory:
  rm -rf ~/.local/bin
"

exit 0
