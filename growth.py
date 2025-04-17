import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("Datasweeper Sterling Integrator By Eisha Saleem")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for Quarter 3.")

# File uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Load data
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"Error loading {file.name}: {e}")
            continue

        # Show data preview
        st.header(f"Preview: {file.name}")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing numeric values filled with column means!")

            # Column selection
            st.subheader("Select Columns to Keep")
            selected_columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[selected_columns]

            # Data Visualization
            st.subheader("Data Visualization")
            if st.checkbox(f"Show visualization for {file.name}"):
                numeric_df = df.select_dtypes(include='number')
                if not numeric_df.empty:
                    st.bar_chart(numeric_df.iloc[:, :2])  # limit to 2 cols for clarity
                else:
                    st.warning("No numeric data available for visualization.")

            # Conversion and Download
            st.subheader("Conversion Options")
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                file_base = os.path.splitext(file.name)[0]

                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = f"{file_base}.csv"
                    mime_type = "text/csv"
                else:  # Excel
                    df.to_excel(buffer, index=False)
                    file_name = f"{file_base}.xlsx"
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)
                st.download_button(
                    label=f"Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

    st.success("All files processed successfully!")
