#!/usr/bin/env python3
import os
import sys
import argparse

def get_tex_content(folder):
    """Get all .tex file content."""
    content = ""
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.tex'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content += f.read() + "\n"
                except:
                    pass
    return content

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', help='Project folder')
    parser.add_argument('figures', help='Figures subfolder')
    args = parser.parse_args()
    
    if not os.path.isdir(args.folder):
        print(f"Error: {args.folder} not found")
        sys.exit(1)
    
    figures_path = os.path.join(args.folder, args.figures)
    if not os.path.isdir(figures_path):
        print(f"Error: {figures_path} not found")
        sys.exit(1)
    
    # Get all tex content
    tex_content = get_tex_content(args.folder)
    
    # Check each figure file recursively
    deleted = []
    for root, dirs, files in os.walk(figures_path):
        for file in files:
            filepath = os.path.join(root, file)
            filename = os.path.splitext(file)[0]  # Without extension
            if filename not in tex_content and file not in tex_content:
                try:
                    os.remove(filepath)
                    deleted.append(os.path.relpath(filepath, figures_path))
                except:
                    pass
    
    # Print deleted files
    if deleted:
        print("Deleted files:")
        for file in deleted:
            print(f"  {file}")
    else:
        print("No unused figures found")

if __name__ == '__main__':
    main()
