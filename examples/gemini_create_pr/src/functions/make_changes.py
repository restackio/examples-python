from restack_ai.function import function
from dataclasses import dataclass
import os

@dataclass
class FilesToCreateOrUpdate:
    file_path: str
    content: str

@dataclass
class FunctionInputParams:
    files_to_create_or_update: list[FilesToCreateOrUpdate]

@function.defn(name="MakeChanges")
async def make_changes(input: FunctionInputParams):
    """Creates or updates files in the repository with provided content.

    This function:
    1. Creates any necessary directories in the file path
    2. Writes or overwrites files with the provided content
    3. Uses UTF-8 encoding for file operations

    Args:
        input (FunctionInputParams): Contains list of files to create/update, 
            where each file has a file_path and content

    Returns:
        list[str]: List of paths to all modified files
    """
    modified_files = []

    try:
        for file in input.files_to_create_or_update:
            os.makedirs(os.path.dirname(file.file_path), exist_ok=True)
            with open(file.file_path, 'w', encoding='utf-8') as f:
                f.write(file.content)
            
            modified_files.append(file.file_path)
        return modified_files
        
    except Exception as e:
        print(f"Error making changes: {str(e)}")
        raise e