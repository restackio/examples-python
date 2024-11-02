import os

def read_scanignore(repo_path):
    """
    Reads .scanignore file from repository and returns a list of patterns to ignore.

    Args:
        repo_path (str): Path to the repository root directory

    Returns:
        list[str]: List of patterns to ignore
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