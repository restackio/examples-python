import streamlit as st
from src.ui.models import InitialInput
import asyncio
from restack_ai import Restack
import time

async def trigger_generate_solution(repo_path: str, user_content: str, chat_history: list = None):
    try:
        client = Restack()
        workflow_id = f"{int(time.time() * 1000)}-GenerateSolutionWorkflow"
        
        run_id = await client.schedule_workflow(
            workflow_name="GenerateSolutionWorkflow",
            workflow_id=workflow_id,
            input={
                "repo_path": repo_path,
                "user_content": user_content,
                "chat_history": chat_history or []
            }
        )
        
        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=run_id
        )
        return result
    except Exception as e:
        st.error(f"Failed to generate solution: {str(e)}")
        return None

def render_initial_input() -> InitialInput | None:
    st.header("Step 1: Initial Input")
    
    repo_path = st.text_input(
        "Repository Path",
        value="/Users/leawn/Code/github.com/leawn/sudoku",
        help="The absolute path to your repository"
    )
    
    task = st.text_area(
        "Task Description",
        value="Change the README.md to be maximum 100 words long",
        help="Describe what changes you want to make"
    )
    
    if st.button("Generate Solution"):
        with st.spinner("Generating solution..."):
            result = asyncio.run(trigger_generate_solution(repo_path, task))
            if result:
                st.session_state.workflow_result = result
                st.session_state.workflow_history = result.get("chat_history", [])
                return InitialInput(repo_path=repo_path, task=task)
            else:
                st.error("Failed to generate solution")
    
    return None