

import streamlit as st # type: ignore
from PyPDF4 import PdfFileMerger # type: ignore
import os

def merge_pdfs(uploaded_files):
    merger = PdfFileMerger()
    for pdf in uploaded_files:
        merger.append(pdf)
    return merger

def main():
    # Custom CSS to enhance the UI
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%);
            font-family: 'Arial', sans-serif;
        }
        .main {
            background-color: transparent;
        }
        .title {
            text-align: center;
            font-size: 3em;
            color: #333;
            margin-bottom: 20px;
            text-shadow: 2px 2px #ff0000;
        }
        .upload-box {
            text-align: center;
            padding: 20px;
            border: 2px dashed #008cba;
            background-color: #fff9e6;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .upload-box:hover {
            border-color: #005f7f;
            background-color: #ffe4b3;
        }
        .button {
            background-color: #008cba;
            color: white;
            font-size: 1.2em;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.3s;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .button:hover {
            background-color: #005f7f;
            transform: translateY(-2px);
        }
        .download-button {
            text-align: center;
            margin-top: 20px;
        }
        .success-message {
            text-align: center;
            font-size: 1.2em;
            color: #28a745;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="title">PDF Merger</div>', unsafe_allow_html=True)

    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type=['pdf'])
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_files:
        st.write(f"<div class='success-message'>{len(uploaded_files)} file(s) uploaded.</div>", unsafe_allow_html=True)
        if st.button("Merge PDFs", key="merge_button", css_class="button"):
            with st.spinner('Merging PDFs...'):
                # Merging PDFs
                merged_pdf = merge_pdfs(uploaded_files)
                
                # Save the merged PDF to a file
                output_path = "merged_output.pdf"
                with open(output_path, "wb") as f:
                    merged_pdf.write(f)
                
                st.success('PDFs merged successfully!')

                # Provide a download link
                with open(output_path, "rb") as f:
                    st.markdown('<div class="download-button">', unsafe_allow_html=True)
                    st.download_button("Download Merged PDF", f, file_name="merged_output.pdf", key="download_button")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Cleanup
                os.remove(output_path)

if __name__ == "__main__":
    main()
