
# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO

# # Set up App
# st.set_page_config(page_title="Data Sweeper", layout="wide")
# st.title('Data Sweeper by Amna Sheikh')
# st.write('Transform your files between CSV and Excel formats with built-in data cleaning and visualization.')

# uploaded_files = st.file_uploader('Upload your File (CSV OR Excel):', type=["csv", "xlsx"], accept_multiple_files=True)

# if uploaded_files:
#     for file in uploaded_files:
#         file_ext = os.path.splitext(file.name)[-1].lower()

#         if file_ext == '.csv':
#             df = pd.read_csv(file)  # ✅ Corrected method name
#         elif file_ext == '.xlsx':
#             df = pd.read_excel(file)  # ✅ Indentation fixed
#         else:
#             st.error(f"Unsupported file type: {file_ext}")  # ✅ `f""` string formatting fix
#             continue

#         # Display dataframe
#         st.write(f"**File Name:** {file.name}")
#         st.write(f"File Size:{file.size/1024}")
#         st.write('Previw the first few rows of the dataframe')
#         st.dataframe(df.head())

#         #options for data cleaning
#         st.subheader(' Data cleaning Options')
#         if st.checkbox(f"Clean Data for {file.name}"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button(f"Remove Duplicates from {file.name}"):
#                     df = df.drop_duplicates(inplace=True)
#                     st.write(f"Removed duplicates from {file.name}!")

#                     with col2:
#                         if st.button(f"Fill Missing Values for{file.name}"):
#                             numeric_cols = df.select_dtypes(include=['number']).columns
#                             df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
#                             st.write("Missing Values Has been Filled!")

    
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up App
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title('💽 Data Sweeper by Amna Sheikh')
st.write('Transform your files between CSV and Excel formats with built-in data cleaning and visualization.')

uploaded_files = st.file_uploader('Upload your File (CSV OR Excel):', type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file, engine="openpyxl")
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # Display file details
        st.write(f"📂 **File Name:** {file.name}")
        st.write(f"📏 **File Size:** {round(file.size / 1024, 2)} KB")
        st.write("🔍 Preview the first few rows of the DataFrame:")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df = df.drop_duplicates()
                    st.write(f"✅ Removed duplicates from {file.name}!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values have been filled!")

        # Select Specific Columns
        st.subheader("📌 Select Columns to Keep")
        columns = st.multiselect(f"Select Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            numeric_df = df.select_dtypes(include='number')
            if not numeric_df.empty:
                st.bar_chart(numeric_df.iloc[:, :2])
            else:
                st.write("⚠️ No numerical columns available for visualization!")

        # File Conversion (CSV <-> Excel)
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file.name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file.name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            downloaded =  st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file.name,
                mime=mime_type
            )

 st.success("🎉 File downloaded successfully!")

            

