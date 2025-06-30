#!/usr/bin/env python3
#This code removes comments from all .tex files in a given folder
#should be called as python3 remove_comments.py <FOLDER_PATH>



import os
import sys
import argparse

def remove_tex_comments(content):
    """Remove % comments from LaTeX files."""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # Find first % not escaped by \
        i = 0
        while i < len(line):
            if line[i] == '%' and (i == 0 or line[i-1] != '\\'):
                line = line[:i]
                break
            i += 1
        result.append(line.rstrip())
    
    return '\n'.join(result)


def process_file(filepath):
    """Process a single file."""
    if not filepath.endswith('.tex'):
        return
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cleaned = remove_tex_comments(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)
            
        print(f"Processed: {filepath}")
        
    except Exception as e:
        print(f"Error: {filepath}: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder')
    args = parser.parse_args()
    
    if not os.path.isdir(args.folder):
        print(f"Error: {args.folder} not found")
        sys.exit(1)
    
    for root, dirs, files in os.walk(args.folder):
        for file in files:
            if file.endswith('.tex'):
                process_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
