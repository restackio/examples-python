import os
import sys
import streamlit.web.cli as stcli

# Add the project root to PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "src/ui/app.py"]
    sys.exit(stcli.main())