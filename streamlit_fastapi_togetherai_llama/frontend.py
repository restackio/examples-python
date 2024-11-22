import streamlit as st
import requests

# Set page title and header
st.title("Restack AI with TogetherAi + LlamaIndex")

# Create text area for user input with session state
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

user_prompt = st.text_area("Ask the pirate any question", height=150, key="user_input")

# Initialize response history in session state
if "response_history" not in st.session_state:
    st.session_state.response_history = []

# Create button to send request
if st.button("Generate Response"):
    if user_prompt:
        try:
            # Make POST request to FastAPI backend
            response = requests.post(
                "http://localhost:8000/api/schedule",
                json={"prompt": user_prompt}
            )
            
            if response.status_code == 200:
                st.success("Response received!")
                # Add the new response to history with the original prompt
                st.session_state.response_history.append({
                    "prompt": user_prompt,
                    "response": response.json()["result"]
                })
            else:
                st.error(f"Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the server. Make sure the FastAPI server is running.")
    else:
        st.warning("Please enter a prompt before submitting.")

# Display response history
if st.session_state.response_history:
    st.subheader("Response History")
    for i, item in enumerate(st.session_state.response_history, 1):
        st.markdown(f"**Prompt {i}:** {item['prompt']}")
        st.markdown(f"**Response {i}:** {item['response']}")
        st.markdown("---")
