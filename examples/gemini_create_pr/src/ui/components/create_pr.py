from restack_ai import Restack
import time
import streamlit as st

async def trigger_create_pr(repo_path: str, pr_info: dict):
    try:
        client = Restack()
        workflow_id = f"{int(time.time() * 1000)}-CreatePrWorkflow"
        
        run_id = await client.schedule_workflow(
            workflow_name="CreatePrWorkflow",
            workflow_id=workflow_id,
            input={
                "repo_path": repo_path,
                "pr_info": pr_info
            }
        )
        
        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=run_id
        )
        return result
    except Exception as e:
        st.error(f"Failed to create PR: {str(e)}")
        return None