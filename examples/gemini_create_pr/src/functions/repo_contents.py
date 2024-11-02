from restack_ai.function import function
from dataclasses import dataclass
import os
import fnmatch

@dataclass
class FunctionInputParams:
    repo_path: str
    output_file: str = "repository_contents.txt"

@dataclass
class FunctionOutputParams:
    repo_contents: str
    output_file: str

def read_scanignore(repo_path):
    """
    Reads .scanignore file and returns list of patterns to ignore.
    Default patterns are included even if file doesn't exist.
    """
    # Default patterns to always ignore
    patterns = [
        '.git/*',
        '.scanignore',
        '*.pyc',
        '__pycache__/*',
        '*.lock',
        'node_modules/*',
    ]
    
    scanignore_path = os.path.join(repo_path, '.scanignore')
    if os.path.exists(scanignore_path):
        with open(scanignore_path, 'r', encoding='utf-8') as f:
            patterns.extend(
                line.strip() for line in f.readlines()
                if line.strip() and not line.startswith('#')
            )
    
    return patterns

def should_ignore(path, ignore_patterns, repo_path):
    """
    Check if a path should be ignored based on ignore patterns.
    """
    rel_path = os.path.relpath(path, repo_path)
    
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
        if pattern.endswith('/*') and fnmatch.fnmatch(rel_path, pattern[:-2]):
            return True
    return False


def read_repostitory_scan(file_path: str):
    """
    Reads the repository scan file and returns its contents as a string.
    
    Args:
        file_path (str): Path to the scan file (default: repository_contents.txt)
    
    Returns:
        str: The contents of the scan file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading scan file: {str(e)}")
        return ""

@function.defn(name="RepoContents")
async def scan_repository(input: FunctionInputParams) -> FunctionOutputParams:
    """
    Scans a repository and writes its structure and file contents to a text file,
    respecting .scanignore patterns.
    
    Args:
        repo_path (str): Path to the repository
        output_file (str): Name of the output file (default: repository_contents.txt)

    Returns:
        str: Absolute path to the output file
    """
    if not os.path.isabs(input.output_file):
        input.output_file = os.path.abspath(input.output_file)

    try:
        ignore_patterns = read_scanignore(input.repo_path)
        
        with open(input.output_file, 'w', encoding='utf-8') as f:
            abs_repo_path = os.path.abspath(input.repo_path)
            f.write(f"=== REPOSITORY ABSOLUTE PATH ===\n{abs_repo_path}\n\n")
            f.write("=== REPOSITORY STRUCTURE ===\n\n")
            for root, dirs, files in os.walk(input.repo_path):
                dirs[:] = [d for d in dirs 
                          if not should_ignore(os.path.join(root, d), ignore_patterns, input.repo_path)]
                level = os.path.relpath(root, input.repo_path)
                if level == ".":
                    f.write(f"📁 {os.path.basename(input.repo_path)}\n")
                else:
                    indent = "  " * (level.count(os.sep) + 1)
                    f.write(f"{indent}📁 {os.path.basename(root)}\n")
                for file in files:
                    file_path = os.path.join(root, file)
                    if not should_ignore(file_path, ignore_patterns, input.repo_path):
                        indent = "  " * (level.count(os.sep) + 1)
                        if level == ".":
                            indent = "  "
                        f.write(f"{indent}📄 {file}\n")
            f.write("\n\n=== FILE CONTENTS ===\n\n")
            for root, dirs, files in os.walk(input.repo_path):
                dirs[:] = [d for d in dirs 
                          if not should_ignore(os.path.join(root, d), ignore_patterns, input.repo_path)]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    if not should_ignore(file_path, ignore_patterns, input.repo_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as file_content:
                                f.write(f"\n--- {os.path.relpath(file_path, input.repo_path)} ---\n")
                                f.write(file_content.read())
                                f.write("\n")
                        except Exception as e:
                            f.write(f"\n--- {os.path.relpath(file_path, input.repo_path)} ---\n")
                            f.write(f"Error reading file: {str(e)}\n")
                        
        print(f"Repository contents have been written to {input.output_file}")

        repo_contents = read_repostitory_scan(input.output_file)
        return FunctionOutputParams(repo_contents=repo_contents, output_file=input.output_file)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
