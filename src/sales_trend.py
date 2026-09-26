import streamlit as st
import pandas as pd
import plotly.express as px


def show_sales_trend(df):
    """
    Display an interactive sales trend chart for SalesInsight.
    """

    st.subheader("Interactive Sales Trend")

    # Make a copy so the original dataset is not changed
    data = df.copy()

    # Convert InvoiceDate to date format
    data["InvoiceDate"] = pd.to_datetime(
        data["InvoiceDate"],
        errors="coerce"
    )

    # Remove rows with invalid dates
    data = data.dropna(subset=["InvoiceDate"])

    # Calculate sales if Sales column does not already exist
    if "Sales" not in data.columns:
        data["Sales"] = (
            pd.to_numeric(data["Quantity"], errors="coerce").fillna(0)
            * pd.to_numeric(data["UnitPrice"], errors="coerce").fillna(0)
        )

    # Date filter
    min_date = data["InvoiceDate"].min().date()
    max_date = data["InvoiceDate"].max().date()

    date_range = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Filter selected dates
    if len(date_range) == 2:
        start_date, end_date = date_range

        filtered_data = data[
            (data["InvoiceDate"].dt.date >= start_date)
            & (data["InvoiceDate"].dt.date <= end_date)
        ]
    else:
        filtered_data = data

    # Group sales by day
    daily_sales = (
        filtered_data
        .groupby(filtered_data["InvoiceDate"].dt.date)["Sales"]
        .sum()
        .reset_index()
    )

    daily_sales.columns = ["Date", "Sales"]

    # Interactive Plotly line chart
    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        markers=True,
        title="Sales Trend Over Time"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Summary
    total_sales = filtered_data["Sales"].sum()

    st.metric(
        "Sales in Selected Period",
        f"${total_sales:,.2f}"
    )
