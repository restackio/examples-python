from restack_ai.function import function
from dataclasses import dataclass
import os

from src.functions.util import read_scanignore, should_ignore, read_repostitory_scan

@dataclass
class FunctionInputParams:
    repo_path: str
    output_file: str = "repository_contents.txt"

@dataclass
class FunctionOutputParams:
    repo_contents: str
    output_file: str


@function.defn(name="RepoContents")
async def scan_repository(input: FunctionInputParams) -> FunctionOutputParams:
    """
    Scans a repository and generates a structured text file containing its contents.

    The scan includes:
    - Repository absolute path
    - Directory structure with proper indentation
    - Complete file contents for all non-ignored files
    
    Args:
        input.repo_path: Path to the repository to scan
        input.output_file: Where to save the scan results (default: repository_contents.txt)

    Returns:
        FunctionOutputParams with repository contents and output file path
    """

    try:
        output_file = os.path.abspath(input.output_file)
        ignore_patterns = read_scanignore(input.repo_path)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write repository path
            abs_repo_path = os.path.abspath(input.repo_path)
            f.write(f"=== REPOSITORY ABSOLUTE PATH ===\n{abs_repo_path}\n\n")

            # Write repository structure
            f.write("=== REPOSITORY STRUCTURE ===\n\n")
            for root, dirs, files in os.walk(input.repo_path):
                dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_patterns, input.repo_path)]

                # Write directory entry
                level = os.path.relpath(root, input.repo_path)
                indent = "  " * (level.count(os.sep) + 1) if level != "." else ""
                f.write(f"{indent}📁 {os.path.basename(root or input.repo_path)}\n")
                
                # Write file entries
                file_indent = "  " * (level.count(os.sep) + 1) if level != "." else "  "
                for file in files:
                    if not should_ignore(os.path.join(root, file), ignore_patterns, input.repo_path):
                        f.write(f"{file_indent}📄 {file}\n")

            # Write file contents
            f.write("\n\n=== FILE CONTENTS ===\n\n")
            for root, dirs, files in os.walk(input.repo_path):
                dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_patterns, input.repo_path)]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    if not should_ignore(file_path, ignore_patterns, input.repo_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as file_content:
                                f.write(f"\n--- {os.path.relpath(file_path, input.repo_path)} ---\n")
                                f.write(file_content.read() + "\n")
                        except Exception as e:
                            f.write(f"\n--- {os.path.relpath(file_path, input.repo_path)} ---\n")
                            f.write(f"Error reading file: {str(e)}\n")

        return FunctionOutputParams(
            repo_contents=read_repostitory_scan(output_file),
            output_file=output_file)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
