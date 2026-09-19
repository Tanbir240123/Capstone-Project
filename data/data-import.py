import numpy as np
import pandas as pd
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def predict_future_revenue(df, horizons=30):
    """
    Generate future timeline predictions for business revenue streams.
    """
    # Convert timelines to localized timestamps
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    # Compute financial yield per transaction line
    df["SalesAmount"] = (df["Quantity"] * df["UnitPrice"])

    # Compile aggregations by resetting tracking clocks to midnight
    timeline_indices = df["InvoiceDate"].dt.floor("D")
    grouped_aggregates = df.groupby(timeline_indices)["SalesAmount"]
    
    # Establish chronological structural series
    revenue_series = grouped_aggregates.sum().sort_index().resample("D").asfreq(fill_value=0)

    # Validate volume requirements for mathematical processing
    if len(revenue_series) < 14:raise ValueError("Insufficient tracking history to process pipeline trends.")

    # Configure structural seasonality options
    has_seasonal_history = bool(len(revenue_series) >= 21)
    
    hyperparameters = {"trend": "add","initialization_method": "estimated"}
    
    if has_seasonal_history:
        hyperparameters.update({"seasonal": "add","seasonal_periods": 7})

    # Execute math execution pipeline
    trained_pipeline = ExponentialSmoothing(revenue_series, **hyperparameters).fit(optimized=True)

    # Extract dynamic matrix values
    raw_predictions = trained_pipeline.forecast(horizons).mask(lambda baseline: baseline < 0, 0)

    # Construct outbound analytical dataset
    output_dataframe = pd.DataFrame(data=raw_predictions.values,index=raw_predictions.index,columns=["ForecastSales"]).reset_index().rename(columns={"index": "Date"})

    return revenue_series, output_dataframe

    st.subheader("Revenue Projections")

# Dynamic user slider input configuration
lookahead_window = st.slider("Prediction horizon (days)",min_value=7,max_value=60,value=30)

try:
    
    observed_revenue, predictions_dataset = predict_future_revenue(
        df, 
        lookahead_window)

    # ==========================================
    #  Forecast chart
    # ==========================================
    
    past_records = (observed_revenue.tail(180).reset_index(name="Sales").rename(columns={"index": "Date"}).assign(Type="Historical"))

    future_records = predictions_dataset.rename(columns={"ForecastSales": "Sales"}).assign(Type="Forecast")

    visualization_matrix = pd.concat([past_records, future_records], axis=0, ignore_index=True)[["Date", "Sales", "Type"]]

    timeseries_graph = px.line(data_frame=visualization_matrix,x="Date",y="Sales",color="Type",title="Revenue Analysis: Observed Metrics vs Projections")

    timeseries_graph.update_layout(height=450)

    st.plotly_chart(timeseries_graph, use_container_width=True)

    # ==========================================
    #  Forecast table
    # ==========================================
    
    st.subheader("Predicted Revenue Breakdown")

    st.dataframe(data=predictions_dataset,use_container_width=True,hide_index=True)

    # ==========================================
    #  Forecast total
    # ==========================================
    
    aggregated_prediction = predictions_dataset["ForecastSales"].sum()

    st.metric(label=f"Projected Total Yield — Upcoming {lookahead_window} Days",value=f"${aggregated_prediction:,.2f}")

    # ==========================================
    # Download
    # ==========================================
    
    exported_bytestream = predictions_dataset.to_csv(index=False).encode("utf-8")

    st.download_button(label="Export Projection Ledger",data=exported_bytestream,file_name="revenue_projections_extract.csv",mime="text/csv")

except Exception as processing_anomaly:
    st.error(f"Unable to complete timeline execution pipeline: {processing_anomaly}")

