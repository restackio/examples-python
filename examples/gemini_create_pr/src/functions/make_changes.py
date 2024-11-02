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
    """
    Creates or updates files based on the generated solution.
    
    Args:
        input: FunctionInputParams containing files to create/update and repository path
    
    Returns:
        list[str]: List of paths to files that were created or updated
    """
    modified_files = []

    try:
        for file in input.files_to_create_or_update:
            os.makedirs(os.path.dirname(file.file_path), exist_ok=True)
            with open(file.file_path, 'w', encoding='utf-8') as f:
                f.write(file.content)
            
            modified_files.append(file.file_path)
            print(f"Created/Updated file: {file.file_path}")
        
        print(f"Modified files: {modified_files}")
        return modified_files
        
    except Exception as e:
        print(f"Error making changes: {str(e)}")
        raise e