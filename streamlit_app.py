import streamlit as st
import pandas as pd
from datetime import datetime, date

# define global variables
today = datetime.now()
start_of_year = date(today.year, 1, 1)
end_of_year = date(today.year, 12, 31)

# Function to create the layout for Batch Doc generation page
def batch_doc_generation_page(title):
    st.title(title)
    st.subheader("Date Range")

    # Single calendar picker for the date range
    date_range = st.date_input(
        "Select SSIM Date Range",
        [today.date(), (today + pd.DateOffset(days=7)).date()],
        min_value=start_of_year,
        max_value=end_of_year,
        format="DD/MM/YYYY"
    )

    # date_range will be a list of 0, 1, or 2 date objects
    if len(date_range) == 2:
        start_date, end_date = date_range
    elif len(date_range) == 1:
        start_date = end_date = date_range[0]
    else:  # This case will occur if no dates are selected
        start_date = end_date = today.date()  # or any default value you choose

    st.subheader("Upload a SSIM file")
    uploaded_file = st.file_uploader("", type="ssim")
    if uploaded_file is not None:
        # You can add code here to handle the uploaded file
        st.write("File Uploaded Successfully")

# Setting up the sidebar
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Type of Doc Generation", ["Batch Doc Generation", "Comparative Doc Generation"])

if app_mode == "Batch Doc Generation":
    batch_doc_generation_page("Batch Doc Generation")

elif app_mode == "Comparative Doc Generation":
    st.title("Comparative Doc Generation")

    # Date Range Picker with a unique key
    st.subheader("Date Range")
    date_range = st.date_input(
        "Select SSIM Date Range",
        [today.date(), (today + pd.DateOffset(days=7)).date()],
        min_value=start_of_year,
        max_value=end_of_year,
        format="DD/MM/YYYY",
        key="comparative_date_range"  # unique key for this date input
    )

    # Layout for side by side file uploaders
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Insert base SSIM File")
        base_ssim_file = st.file_uploader("Drag and drop file here or click to browse", type="txt", key="base_ssim")

    with col2:
        st.subheader("Insert new SSIM File")
        new_ssim_file = st.file_uploader("Drag and drop file here or click to browse", type="txt", key="new_ssim")

