import streamlit as st

def upload_files(supported_files):
    """
    Handles file upload and reading for text analysis.
    Returns:
        texts (list[str]): List of file contents as strings.
        uploaded_files (list): List of uploaded file objects.
    """
    uploaded_files = st.file_uploader(
        "📂 Upload one or more text files",
        type=supported_files,
        accept_multiple_files=True
    )

    if not uploaded_files:
        return None, None

    # Read content safely
    texts = []
    for f in uploaded_files:
        try:
            content = f.read().decode("utf-8", errors="ignore")
            texts.append(content)
        except Exception as e:
            st.warning(f"⚠️ Could not read file '{f.name}': {e}")

    # Show summary
    st.success(f"✅ {len(texts)} file(s) loaded successfully!")
    return texts, uploaded_files
