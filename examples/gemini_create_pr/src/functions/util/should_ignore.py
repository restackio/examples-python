import os
import fnmatch

def should_ignore(path, ignore_patterns, repo_path):
    """
    Determines if a file or directory should be ignored based on provided patterns.

    Args:
        path: Absolute path to the file or directory to check
        ignore_patterns: List of glob patterns to match against (e.g., ['*.pyc', 'node_modules/*'])
        repo_path: Root path of the repository for relative path calculation

    Returns:
        bool: True if the path should be ignored, False otherwise
    """
    rel_path = os.path.relpath(path, repo_path)
    
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
        if pattern.endswith('/*') and fnmatch.fnmatch(rel_path, pattern[:-2]):
            return True
    return False