import streamlit as st
from src.ui.models import PrInfoValidation
from restack_ai import Restack
import time

async def trigger_make_changes(repo_path: str, files_to_create_or_update: list, chat_history: list, user_content: str = None):
    try:
        client = Restack()
        workflow_id = f"{int(time.time() * 1000)}-MakeChangesWorkflow"
        
        run_id = await client.schedule_workflow(
            workflow_name="MakeChangesWorkflow",
            workflow_id=workflow_id,
            input={
                "repo_path": repo_path,
                "files_to_create_or_update": files_to_create_or_update,
                "chat_history": chat_history,
                "user_content": user_content
            }
        )
        
        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=run_id
        )
        return result
    except Exception as e:
        st.error(f"Failed to make changes: {str(e)}")
        return None

def render_pr_info_validation() -> PrInfoValidation | None:
    if "make_changes_result" not in st.session_state:
        st.error("No PR info generated yet")
        return None

    st.header("Step 3: PR Information Validation")
    
    pr_info = st.session_state.make_changes_result.get("pr_info", {})
    
    st.subheader("Generated PR Information")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text_area(
            "Branch Name",
            value=pr_info.get("branch_name", ""),
            disabled=True,
            help="The name of the branch to be created"
        )
        st.text_area(
            "Commit Message",
            value=pr_info.get("commit_message", ""),
            disabled=True,
            help="The commit message following conventional commits format"
        )
        st.text_area(
            "PR Title",
            value=pr_info.get("pr_title", ""),
            disabled=True,
            help="The title of the pull request"
        )
    
    with col2:
        approved = st.checkbox("Approve PR Information")
        feedback = ""
        if not approved:
            feedback = st.text_area(
                "Feedback",
                help="What would you like to change about the PR information?"
            )
    
    if st.button("Proceed" if approved else "Regenerate with Feedback"):
        return PrInfoValidation(approved=approved, feedback=feedback)
    
    return None