import streamlit as st

def render_completion():
    st.header("🎉 Success!")
    
    if "create_pr_result" in st.session_state:
        pr_url = st.session_state.create_pr_result.get("pr_url")
        if pr_url:
            st.success("Pull Request created successfully!")
            st.markdown(f"### [View Pull Request]({pr_url})")
            st.markdown("Your changes have been submitted for review.")
        else:
            st.warning("Pull Request was created but the URL is not available.")
    else:
        st.error("Something went wrong. Pull Request result not found.")
    
    if st.button("Create Another PR"):
        for key in list(st.session_state.keys()):
            if key != "authentication_status":
                del st.session_state[key]
        st.session_state.step = 1
        st.rerun()