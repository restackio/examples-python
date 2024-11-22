import streamlit as st
import requests
import tempfile
from pathlib import Path

st.title("Defense Hackathon Quickstart: War Audio Noise Removal")

tmp_dir = Path(tempfile.gettempdir()) / 'streamlit_uploads'
tmp_dir.mkdir(exist_ok=True)

def get_file_path(uploaded_file):
    temp_path = tmp_dir / uploaded_file.name
    temp_path.write_bytes(uploaded_file.getvalue())
    return str(temp_path.absolute())

uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

if uploaded_files:
    file_data_list = []
    file_paths = []

    for uploaded_file in uploaded_files:
        file_path = get_file_path(uploaded_file)
        file_paths.append(file_path)
        file_data_list.append((file_path, uploaded_file.name))

if "response_history" not in st.session_state:
    st.session_state.response_history = []

if st.button("Process Audio"):
    if uploaded_files:
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
                        with open(file_paths[idx], "rb") as f:
                            file_bytes = f.read()
                        st.session_state.response_history.append({
                            "file_name": uploaded_file.name,
                            "file_type": uploaded_file.type,
                            "original_audio": uploaded_file,
                            "cleaned_audio": results[idx]['cleaned_audio']
                        })
                else:
                    st.error(f"Error: {response.status_code}")

        except requests.exceptions.ConnectionError as e:
            st.error("Failed to connect to the server. Make sure the FastAPI server is running.")
    else:
        st.warning("Please upload a file before submitting.")

if st.session_state.response_history:
    st.subheader("Audio Processing History")
    for i, item in enumerate(st.session_state.response_history, 1):
        st.markdown(f"**Run {i}:**")
        st.markdown(f"**File Name:** {item['file_name']}")
        st.markdown(f"**File Type:** {item['file_type']}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Original Audio:**")
            try:
                st.audio(item['original_audio'], format=item['file_type'])
            except Exception as e:
                st.error(f"Error playing original audio: {str(e)}")

        with col2:
            st.markdown("**Cleaned Audio:**")
            try:
                st.audio(item['cleaned_audio'], format='audio/mp3')
            except Exception as e:
                st.error(f"Error playing audio: {e}")

        st.markdown("---")
        