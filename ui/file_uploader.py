import streamlit as st
import zipfile
import rarfile
import tempfile
import os
from utils.logger import get_logger

logger = get_logger("file_uploader")


def upload_files(supported_types):
    """
    Handles uploading of text files or compressed archives (ZIP/RAR).
    Returns:
        texts (list[str]): List of decoded text contents.
        uploaded_files (list[UploadedFile]): Original uploaded files.
    """
    st.header("📤 Upload Files")

    uploaded_files = st.file_uploader(
        "Upload text files or compressed archives (ZIP/RAR)",
        type=supported_types + ["zip", "rar"],
        accept_multiple_files=True
    )

    logger.info(f"[UPLOAD] Uploaded files list: {uploaded_files}")
    texts = []

    if uploaded_files:
        for file in uploaded_files:
            try:
                filename = file.name.lower()
                logger.info(f"[UPLOAD] Processing file: {filename} | size={file.size}")

                # Return the cursor to the beginning of the file
                file.seek(0)

                # Create a temporary folder to work on
                with tempfile.TemporaryDirectory() as tmpdir:
                    path = os.path.join(tmpdir, filename)

                    # Save the file in the temporary folder
                    with open(path, "wb") as temp_file:
                        temp_file.write(file.read())

                    extracted_files = []

                    # If the file is a ZIP file
                    if filename.endswith(".zip"):
                        with zipfile.ZipFile(path, "r") as zip_ref:
                            zip_ref.extractall(tmpdir)
                            extracted_files = [
                                os.path.join(tmpdir, name)
                                for name in zip_ref.namelist()
                                if name.endswith(".txt")
                            ]

                    # If the file is RAR
                    elif filename.endswith(".rar"):
                        with rarfile.RarFile(path, "r") as rar_ref:
                            rar_ref.extractall(tmpdir)
                            extracted_files = [
                                os.path.join(tmpdir, name)
                                for name in rar_ref.namelist()
                                if name.endswith(".txt")
                            ]

                    # If it is a plain text file
                    elif filename.endswith(".txt"):
                        extracted_files = [path]

                    # Reading extracted text files
                    for txt_path in extracted_files:
                        if os.path.isfile(txt_path):
                            try:
                                with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
                                    content = f.read().strip()
                                    texts.append(content)
                                    logger.info(f"[UPLOAD] Read text file: {txt_path} | length={len(content)}")
                            except Exception as e:
                                logger.error(f"Failed to read extracted file {txt_path}: {e}")

            except Exception as e:
                logger.error(f"[UPLOAD] Failed to process file {file.name}: {e}")

        if texts:
            st.success(f"✅ Loaded {len(texts)} text file(s) successfully!")
        else:
            st.warning("⚠ No valid text content found in the uploaded files.")

    else:
        st.info("📎 Please upload text files (.txt) or a ZIP/RAR archive.")

    # Display statistics in the log
    logger.info(f"[UPLOAD] Final result: files_count={len(uploaded_files) if uploaded_files else 0}, texts_count={len(texts)}")
    for i, t in enumerate(texts):
        logger.info(f"[UPLOAD] Text {i+1}: length={len(t)} preview='{t[:50]}'")

    return texts, uploaded_files
