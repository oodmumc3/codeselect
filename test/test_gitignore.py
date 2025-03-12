#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_gitignore.py - Manual test for .gitignore functionality

This script demonstrates the .gitignore functionality by creating a test directory
with various files and a .gitignore file, then building a file tree and displaying
which files are included/excluded.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from filetree import build_file_tree
from utils import load_gitignore_patterns

def main():
    """Test .gitignore functionality with a manual test."""
    # Create a temporary test directory
    temp_dir = tempfile.mkdtemp()
    print(f"Test directory created at: {temp_dir}")
    
    try:
        # Create .gitignore file
        gitignore_content = """
# This is a test .gitignore file
*.log
ignored_dir/
ignored_file.txt
!important.log
"""
        
        with open(os.path.join(temp_dir, ".gitignore"), "w") as f:
            f.write(gitignore_content)
            
        print("Created .gitignore with content:")
        print(gitignore_content)
        
        # Create test files and directories
        Path(os.path.join(temp_dir, "normal_file.txt")).write_text("Normal file content")
        Path(os.path.join(temp_dir, "error.log")).write_text("Error log content")
        Path(os.path.join(temp_dir, "important.log")).write_text("Important log content")
        Path(os.path.join(temp_dir, "ignored_file.txt")).write_text("Ignored file content")
        
        os.makedirs(os.path.join(temp_dir, "normal_dir"))
        os.makedirs(os.path.join(temp_dir, "ignored_dir"))
        
        Path(os.path.join(temp_dir, "normal_dir", "file_in_normal_dir.txt")).write_text("File in normal dir")
        Path(os.path.join(temp_dir, "ignored_dir", "file_in_ignored_dir.txt")).write_text("File in ignored dir")
        
        # Load gitignore patterns and display them
        patterns = load_gitignore_patterns(temp_dir)
        print("\nLoaded .gitignore patterns:")
        for pattern in patterns:
            print(f"  - {pattern}")
            
        # Build file tree
        print("\nBuilding file tree...")
        root_node = build_file_tree(temp_dir)
        
        # Print the file tree
        print("\nFile tree contents (should exclude ignored files/dirs):")
        def print_tree(node, indent=""):
            print(f"{indent}- {node.name}{'/' if node.is_dir else ''}")
            if node.is_dir and node.children:
                for child_name in sorted(node.children.keys()):
                    print_tree(node.children[child_name], indent + "  ")
                    
        print_tree(root_node)
        
        # Print summary
        print("\nSummary:")
        print("The following should be INCLUDED:")
        print("  - normal_file.txt")
        print("  - important.log (exception to *.log pattern)")
        print("  - normal_dir/")
        print("  - normal_dir/file_in_normal_dir.txt")
        
        print("\nThe following should be EXCLUDED:")
        print("  - error.log (matched by *.log)")
        print("  - ignored_file.txt (directly listed)")
        print("  - ignored_dir/ (directory pattern)")
        print("  - ignored_dir/file_in_ignored_dir.txt (in ignored directory)")
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)
        print(f"\nTest directory removed: {temp_dir}")

if __name__ == "__main__":
    main()
