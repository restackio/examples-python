import streamlit as st
import asyncio
from restack_ai import Restack
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to trigger a workflow
async def trigger_workflow(workflow_name, workflow_id, input_data):

    try:
        client = Restack()
        run_id = await client.schedule_workflow(
          workflow_name= workflow_name,
          workflow_id= workflow_id,
          input= input_data,
        )

        result = await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id
        )
        print(result)

        return result
    except Exception as e:
        st.error(f"Failed to trigger workflow: {str(e)}")
        return None

# Streamlit UI
st.title("Trigger Restack Workflow")

workflow_name = st.text_input("Workflow Name")
workflow_id = st.text_input("Workflow ID")
input_data = st.text_area("Input Data (JSON format)")

if st.button("Trigger Workflow"):
    if not workflow_name or not workflow_id:
        st.error("Workflow name and ID are required.")
    else:
        input_dict = eval(input_data) if input_data else {}
        run_id = asyncio.run(trigger_workflow(workflow_name, workflow_id, input_dict))
        
        # Log the input data
        logging.info(f"Triggered workflow with input: {input_dict}")
        
        if run_id:
            st.success(f"Workflow triggered successfully with runId: {run_id}")
