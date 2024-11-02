import streamlit as st
import asyncio
from src.ui.components.initial_input import render_initial_input, trigger_generate_solution
from src.ui.components.solution_validation import render_solution_validation
from src.ui.components.pr_info_validation import render_pr_info_validation, trigger_make_changes
from src.ui.components.create_pr import trigger_create_pr
from src.ui.components.completion import render_completion

def main():
    st.set_page_config(
        page_title="Gemini PR Creator",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("Gemini PR Creator")
    
    if "step" not in st.session_state:
        st.session_state.step = 1
    
    # Step 1: Initial Input and Solution Generation
    if st.session_state.step == 1:
        result = render_initial_input()
        if result:
            st.session_state.initial_input = result
            st.session_state.step = 2
            st.rerun()
    
    # Step 2: Solution Validation
    elif st.session_state.step == 2:
        result = render_solution_validation()
        if result:
            if result.approved:
                st.session_state.step = 3
                # Trigger make changes workflow
                with st.spinner("Making changes and generating PR info..."):
                    make_changes_result = asyncio.run(trigger_make_changes(
                        st.session_state.initial_input.repo_path,
                        st.session_state.workflow_result["files_to_create_or_update"],
                        st.session_state.workflow_history
                ))
                if make_changes_result:
                        st.session_state.make_changes_result = make_changes_result
                        st.rerun()
            else:
                with st.spinner("Regenerating solution with feedback..."):
                    new_result = asyncio.run(trigger_generate_solution(
                        st.session_state.initial_input.repo_path,
                        result.feedback,
                        st.session_state.workflow_history
                    ))
                    if new_result:
                        st.session_state.workflow_result = new_result
                        st.session_state.workflow_history = new_result.get("chat_history", [])
                        st.rerun()
    
    # Step 3: PR Info Validation
    elif st.session_state.step == 3:
        result = render_pr_info_validation()
        if result:
            if result.approved:
                st.session_state.step = 4
                st.success("PR info approved! Ready for the next step.")
                st.rerun()
            else:
                with st.spinner("Regenerating PR info with feedback..."):
                    new_result = asyncio.run(trigger_make_changes(
                        st.session_state.initial_input.repo_path,
                        st.session_state.workflow_result["files_to_create_or_update"],
                        st.session_state.workflow_history,
                        result.feedback
                    ))
                    if new_result:
                        st.session_state.make_changes_result = new_result
                        st.rerun()
    
    # Step 4: Create PR
    elif st.session_state.step == 4:
        with st.spinner("Creating Pull Request..."):
            create_pr_result = asyncio.run(trigger_create_pr(
                st.session_state.initial_input.repo_path,
                st.session_state.make_changes_result.get("pr_info", {})
        ))
        if create_pr_result:
            st.session_state.create_pr_result = create_pr_result
            st.success("Pull Request created successfully!")
            st.session_state.step = 5
            st.rerun()

    # Step 5: Completion
    elif st.session_state.step == 5:
        render_completion()

if __name__ == "__main__":
    main()