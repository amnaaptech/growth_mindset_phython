
import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("💽 Data Sweeper by Amna Sheikh")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

uploaded_files = st.file_uploader("Upload your File (CSV OR Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # ✅ Try reading the file
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                file_bytes = BytesIO(file.getvalue())  # ✅ Convert to file-like object
                df = pd.read_excel(file_bytes, engine="openpyxl")
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"❌ Error reading {file_ext} file: {e}")
            continue 

        # ✅ Ensure DataFrame is valid
        if df is None or df.empty:
            st.error(f"⚠️ The uploaded file {file.name} is empty or invalid.")
            continue

        # ✅ Display file details
        st.write(f"📂 **File Name:** {file.name}")
        st.write(f"📏 **File Size:** {round(file.size / 1024, 2)} KB")
        st.write("🔍 Preview the first few rows of the DataFrame:")
        st.dataframe(df.head())

        # ✅ Data Cleaning Options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write(f"✅ Removed duplicates from {file.name}!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values have been filled!")
 
  # Select Specific Columns
        if not df.empty:
            st.subheader("📌 Select Columns to Keep")
            columns = st.multiselect(f"Select Columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]


              # Data Visualization
        if not df.empty:
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"Show Visualization for {file.name}"):
                numeric_df = df.select_dtypes(include='number')
                if not numeric_df.empty:
                    st.bar_chart(numeric_df.iloc[:, :2])
                else:
                    st.write("⚠️ No numerical columns available for visualization!")


              
        # ✅ File Conversion (CSV <-> Excel)
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            try:
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file.name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False, engine="openpyxl")
                    file.name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)
                file_downloaded = st.download_button(
                    label=f"📥 Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file.name,
                    mime=mime_type
                )

                # ✅ Show balloons only after download
                if file_downloaded:
                    st.success("🎉 File downloaded successfully!")
                    st.balloons()

            except Exception as e:
                st.error(f"❌ Error during file conversion: {e}")

    st.success("🎉 All files processed successfully!")
