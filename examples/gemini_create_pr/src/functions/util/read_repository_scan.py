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