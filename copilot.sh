#!/bin/bash

# Define the output file
OUTPUT_FILE="copilot.txt"

# Clear the output file if it exists
> "$OUTPUT_FILE"

# Add repository structure information at the beginning
cat << 'EOF' > "$OUTPUT_FILE"
# Repository structure

A Restack backend application should be structured as follows:

- src/
    - client.py
    - functions/
        - __init__.py
        - function.py
    - workflows/
        - __init__.py
        - workflow.py
    - services.py
    - schedule_workflow.py
    - pyproject.toml
    - env.example
    - README.md
    - Dockerfile

All these files are mandatory.

EOF

# Use git ls-files to get tracked files only, excluding .gitignore files
git ls-files "*.py" | grep -v "__init__.py" | grep -v "community/" | while read -r file; do
    echo "Processing: $file"  # Debug line
    echo "### File: $file ###" >> "$OUTPUT_FILE"
    cat "$file" >> "$OUTPUT_FILE"
    echo -e "\n" >> "$OUTPUT_FILE"
done

echo "All Python example code has been compiled into $OUTPUT_FILE"