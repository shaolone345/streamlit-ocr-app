import streamlit as st
import subprocess
import os
import time

# Streamlit app title
st.title("📄 Searchable PDF Converter (OCR)")
st.write("Upload scanned PDFs, and this app will convert them into searchable PDFs using OCR.")

# Create a temporary directory
TEMP_DIR = "temp_pdfs"
os.makedirs(TEMP_DIR, exist_ok=True)

# File uploader - Allows multiple PDF files
uploaded_files = st.file_uploader("Choose scanned PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    processed_files = []
    
    for uploaded_file in uploaded_files:
        input_path = os.path.join(TEMP_DIR, uploaded_file.name)
        output_path = os.path.join(TEMP_DIR, f"searchable_{uploaded_file.name}")

        # Save the uploaded file temporarily
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Run OCRmyPDF
        with st.spinner(f"Processing {uploaded_file.name}..."):
            try:
                subprocess.run(["ocrmypdf", input_path, output_path, "--redo-ocr", "-l", "eng"], check=True)
                processed_files.append(output_path)

                # Immediately delete the original file after processing
                os.remove(input_path)

            except subprocess.CalledProcessError as e:
                st.error(f"❌ Error processing {uploaded_file.name}: {e}")

    # Show success message
    if processed_files:
        st.success(f"✅ Successfully processed {len(processed_files)} PDFs!")

        # Provide download buttons for each processed file
        for file in processed_files:
            with open(file, "rb") as f:
                st.download_button(f"⬇️ Download {os.path.basename(file)}", f, file_name=os.path.basename(file), mime="application/pdf")

        # Wait before deleting processed files
        time.sleep(2)
        for file in processed_files:
            os.remove(file)
