import streamlit as st
import requests
import base64
# Set page title and header
st.title("Defense Hackathon Quickstart: War Audio Transcription & Translation")



uploaded_files = st.file_uploader("Choose a files", accept_multiple_files=True)

if uploaded_files:
    file_data_list = []
    for uploaded_file in uploaded_files:
        audio_data = uploaded_file.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        file_data_list.append((uploaded_file.name, audio_base64))

if "response_history" not in st.session_state:
    st.session_state.response_history = []

if st.button("Process Audio"):
    if uploaded_file:
        try:
            with st.spinner('Processing audio...'):
                response = requests.post(
                    "http://localhost:8000/api/process_audio",
                    json={"file_data": file_data_list}
                )

                if response.status_code == 200:
                    st.success("Processing audio was successful!")

                    results = response.json()["result"]
                    for idx, uploaded_file in enumerate(uploaded_files):
                        st.session_state.response_history.append({
                            "file_name": uploaded_file.name,
                            "file_type": uploaded_file.type,
                            "transcription": results[idx]['transcription'],
                            "translation": results[idx]['translation']
                    })
                else:
                    st.error(f"Error: {response.status_code}")

        except requests.exceptions.ConnectionError as e:
            st.error(f"Failed to connect to the server. Make sure the FastAPI server is running.")
    else:
        st.warning("Please upload a file before submitting.")

if st.session_state.response_history:
    st.subheader("Audio Processing History")
    for i, item in enumerate(st.session_state.response_history, 1):
        st.markdown(f"**Run {i}:**")
        st.markdown(f"**File Name:** {item['file_name']}")
        st.markdown(f"**File Type:** {item['file_type']}")
        st.markdown(f"**Transcription:** {item['transcription']}")
        st.markdown(f"**Translation:** {item['translation']}")
        st.markdown("---")
        