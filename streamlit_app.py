import streamlit as st
import pandas as pd
from datetime import datetime, date
import io
import zipfile
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

# Add the project root to sys.path
sys.path.append(str(project_root))

# Now you can import your modules
from src.main import test_batch_streamlit
from src.models.ssim_file import SSIM_File

# Define global variables
today = datetime.now()
start_of_year = date(today.year, 1, 1)
end_of_year = date(today.year + 1, 12, 31)

# Set page to wide mode
st.set_page_config(layout="wide")

# Function to handle Batch Document Generation
def batch_doc_generation_page(title):
    st.title(title)
    st.subheader("Date Range")

    # Single calendar picker for the date range
    date_range = st.date_input(
        "Select SSIM Date Range",
        [today.date(), (today + pd.DateOffset(days=7)).date()],
        min_value=start_of_year,
        max_value=end_of_year,
        format="DD-MM-YYYY"
    )

    # Handling date_range
    start_date, end_date = date_range if len(date_range) == 2 else (date_range[0], date_range[0])

    st.subheader("Upload a SSIM file")
    uploaded_file = st.file_uploader("", type="ssim")

    if uploaded_file is not None:
        ssim_object = SSIM_File(uploaded_file)
        st.write("File Uploaded Successfully")
        generate_button = st.button("Generate Permits")
        if generate_button:
            # Assuming test_batch processes the uploaded file and returns a zip buffer
            zip_buffer = test_batch_streamlit(ssim_object)
            st.download_button(
                label="Download Output ZIP",
                data=zip_buffer,
                file_name="output.zip",
                mime="application/zip"
            )

# Function to handle Comparative Document Generation
def comparative_doc_generation_page(title):
    st.title(title)
    st.subheader("Date Range")

    date_range = st.date_input(
        "Select SSIM Date Range",
        [today.date(), (today + pd.DateOffset(days=7)).date()],
        min_value=start_of_year,
        max_value=end_of_year,
        format="DD-MM-YYYY",
        key="comparative_date_range"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Insert base SSIM File")
        base_ssim_file = st.file_uploader("Drag and drop file here or click to browse", type="ssim", key="base_ssim")

    with col2:
        st.subheader("Insert new SSIM File")
        new_ssim_file = st.file_uploader("Drag and drop file here or click to browse", type="ssim", key="new_ssim")

# Main App
def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Type of Doc Generation", ["Batch Doc Generation", "Comparative Doc Generation"])

    if app_mode == "Batch Doc Generation":
        batch_doc_generation_page("Batch Doc Generation")
    elif app_mode == "Comparative Doc Generation":
        comparative_doc_generation_page("Comparative Doc Generation")

if __name__ == "__main__":
    main()
