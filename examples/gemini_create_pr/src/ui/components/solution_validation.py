import streamlit as st
from typing import List
from src.ui.models import FileChange, SolutionValidation

def render_solution_validation() -> SolutionValidation | None:
    if "workflow_result" not in st.session_state:
        st.error("No solution generated yet")
        return None

    st.header("Step 2: Validate Generated Solution")
    
    files = [
        FileChange(
            file_path=file["file_path"],
            content=file["content"]
        ) for file in st.session_state.workflow_result.get("files_to_create_or_update", [])
    ]
    
    approved = True
    feedback = ""
    
    for idx, file in enumerate(files):
        st.subheader(f"File {idx + 1}: {file.file_path}")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_area(
                "Content",
                value=file.content,
                height=300,
                key=f"content_{idx}",
                disabled=True
            )
        
        with col2:
            if not st.checkbox("Approve", key=f"approve_{idx}"):
                approved = False
                feedback = st.text_area(
                    "Feedback",
                    key=f"feedback_{idx}",
                    help="What would you like to change?"
                )
    
    if st.button("Proceed" if approved else "Regenerate with Feedback"):
        return SolutionValidation(approved=approved, feedback=feedback)
    
    return None