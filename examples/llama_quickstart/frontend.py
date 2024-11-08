import streamlit as st
import requests

# Set page title and header
st.title("LLama Hackathon Quickstart")
st.text("FastAPI, Restack, Together AI, LLamaIndex")

# Create text area for user input with session state
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

query = st.text_input("Query HN", key="query", value="ai")
count = st.number_input("Number of results", key="count", value=5)

# Initialize response history in session state
if "response_history" not in st.session_state:
    st.session_state.response_history = []

# Create button to send request
if st.button("Search HN"):
    if query:
        try:
            with st.spinner('Searching...'):
                # Make POST request to FastAPI backend
                response = requests.post(
                    "http://localhost:8000/api/schedule",
                    json={"query": query, "count": count}
                )
                
                if response.status_code == 200:
                    st.success("Response received!")
                    # Add the new response to history with the original prompt
                    st.session_state.response_history.append({
                        "query": query,
                        "count": count,
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
        st.markdown(f"**Query {i}:** {item['query']}")
        st.markdown(f"**Response {i}:** {item['response']}")
        st.markdown("---")
