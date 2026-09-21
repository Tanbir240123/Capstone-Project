import streamlit as st
from src.data_pipeline import run_pipeline

st.set_page_config(
    page_title="SalesInsight",
    page_icon="📊",
    layout="wide",
)

st.title("SalesInsight")
st.caption("Upload a sales CSV dataset to automatically validate, clean, and transform your data.")

uploaded_file = st.file_uploader(
    "Sales Data CSV",
    type=["csv"],
    help="Dataset must contain standard retail columns (InvoiceNo, StockCode, Quantity, UnitPrice, etc.)",
)

if not uploaded_file:
    st.info("Upload a CSV file above to start processing.")
    st.stop()

try:
    with st.spinner("Processing dataset..."):
        df, stats = run_pipeline(uploaded_file)

    st.success("File processed successfully!")

    # Summary Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Original Rows", f"{stats['original_rows']:,}")
    c2.metric("Processed Rows", f"{stats['processed_rows']:,}")
    c3.metric("Rows Removed", f"{stats['removed_rows']:,}")
    c4.metric("Duplicates Dropped", f"{stats['duplicate_rows']:,}")

    st.divider()

    # Data Preview & Export
    st.subheader("Data Preview")
    st.dataframe(df.head(100), use_container_width=True)

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Processed Data (.csv)",
        data=csv_bytes,
        file_name="processed_sales_data.csv",
        mime="text/csv",
        type="primary",
    )

except ValueError as err:
    st.error(str(err))
except Exception as err:
    st.error(f"Unexpected error while processing: {err}")