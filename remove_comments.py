#!/usr/bin/env python3
import os
import sys
import re
import argparse

def remove_tex_comments(content):
    """Remove comments from LaTeX files."""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # Find % not preceded by \
        in_comment = False
        new_line = ""
        i = 0
        
        while i < len(line):
            if i > 0 and line[i-1] == '\\' and line[i] == '%':
                # Escaped %, keep it
                new_line += line[i]
            elif line[i] == '%':
                # Start of comment, stop processing this line
                break
            else:
                new_line += line[i]
            i += 1
        
        result.append(new_line.rstrip())
    
    return '\n'.join(result)

def remove_bib_comments(content):
    """Remove comments from BibTeX files."""
    # Remove % comments (same logic as tex)
    content = remove_tex_comments(content)
    
    # Remove @comment{...} entries
    content = re.sub(r'@comment\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', '', content, flags=re.IGNORECASE | re.MULTILINE)
    
    return content

def process_file(filepath):
    """Process a single file to remove comments."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if filepath.endswith('.tex'):
            cleaned_content = remove_tex_comments(content)
        elif filepath.endswith('.bib'):
            cleaned_content = remove_bib_comments(content)
        else:
            return
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
            
        print(f"Processed: {filepath}")
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Remove comments from .tex and .bib files')
    parser.add_argument('folder', help='Path to folder containing files')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.folder):
        print(f"Error: {args.folder} is not a valid directory")
        sys.exit(1)
    
    # Find all .tex and .bib files
    for root, dirs, files in os.walk(args.folder):
        for file in files:
            if file.endswith(('.tex', '.bib')):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == '__main__':
    main()
