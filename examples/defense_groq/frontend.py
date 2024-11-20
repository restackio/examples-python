import streamlit as st
import requests
import base64
# Set page title and header
st.title("Defense Hackathon Groq Example")
st.text("Streamlit, FastAPI, Restack, Groq")



uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    audio_data = uploaded_file.read()
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    file_data = (uploaded_file.name, audio_base64)


if "response_history" not in st.session_state:
    st.session_state.response_history = []

if st.button("Transcribe"):
    if uploaded_file:
        try:
            with st.spinner('Transcribing...'):
                response = requests.post(
                    "http://localhost:8000/api/transcribe",
                    json={"file_data": file_data}
                )

                if response.status_code == 200:
                    st.success("Transcription received!")
                    st.session_state.response_history.append({
                        "file_name": uploaded_file.name,
                        "file_type": uploaded_file.type,
                        "transcription": response.json()["result"]
                    })
                else:
                    st.error(f"Error: {response.status_code}")

        except requests.exceptions.ConnectionError as e:
            st.error(f"Failed to connect to the server. Make sure the FastAPI server is running.")
    else:
        st.warning("Please upload a file before submitting.")

if st.session_state.response_history:
    st.subheader("Transcription History")
    for i, item in enumerate(st.session_state.response_history, 1):
        st.markdown(f"**File Name {i}:** {item['file_name']}")
        st.markdown(f"**File Type {i}:** {item['file_type']}")
        st.markdown(f"**Transcription {i}:** {item['transcription']}")
        st.markdown("---")
        