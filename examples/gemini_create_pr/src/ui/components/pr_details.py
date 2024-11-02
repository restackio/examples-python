import streamlit as st
from src.ui.models import PrDetails

def render_pr_details() -> PrDetails | None:
    st.header("Step 3: Pull Request Details")
    
    branch_name = st.text_input(
        "Branch Name",
        value="feature/readme-update",
        help="Name of the branch to create"
    )
    
    title = st.text_input(
        "PR Title",
        value="Update README with detailed project description",
        help="Title of the pull request"
    )
    
    description = st.text_area(
        "PR Description",
        value="This PR updates the README to provide a more comprehensive project description.",
        help="Description of the pull request"
    )
    
    approved = st.checkbox("Approve PR Details")
    
    if st.button("Create Pull Request" if approved else "Regenerate Details"):
        return PrDetails(
            branch_name=branch_name,
            title=title,
            description=description,
            approved=approved
        )
    
    return None