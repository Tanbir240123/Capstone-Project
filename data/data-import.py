import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from statsmodels.tsa.holtwinters import ExponentialSmoothing


# ============================================================
# SCRUM-86: Prepare historical sales data
# ============================================================
def transform_transactional_records(df):
    clean_df = df.copy()

    # Re-cast data types structurally
    clean_df["InvoiceDate"] = pd.to_datetime(clean_df["InvoiceDate"], errors="coerce")
    clean_df["Quantity"] = pd.to_numeric(clean_df["Quantity"], errors="coerce")
    clean_df["UnitPrice"] = pd.to_numeric(clean_df["UnitPrice"], errors="coerce")

    # Drop missing values and filter for real transactional values
    clean_df = clean_df.dropna(subset=["InvoiceDate", "Quantity", "UnitPrice"])
    clean_df = clean_df[(clean_df["Quantity"] > 0) & (clean_df["UnitPrice"] > 0)]

    # Compute operational earnings metrics
    clean_df["SalesAmount"] = clean_df["Quantity"] * clean_df["UnitPrice"]

    # Build sequential date timeline matrix
    return (
        clean_df.groupby(clean_df["InvoiceDate"].dt.floor("D"))["SalesAmount"]
        .sum()
        .resample("D")
        .asfreq(fill_value=0)
        .sort_index()
    )


# ============================================================
# SCRUM-87: Select forecasting method and variable
# ============================================================
def evaluate_forecasting_logic(timeline_series):
    total_days = len(timeline_series)
    
    if total_days < 14:
        raise ValueError("Insufficient history timeline. Missing baseline 14 elements.")

    model_settings = {
        "trend": "add",
        "initialization_method": "estimated",
    }

    if total_days >= 21:
        model_settings.update({"seasonal": "add", "seasonal_periods": 7})
        algorithm_label = "Exponential Smoothing with additive trend and weekly seasonality"
    else:
        algorithm_label = "Exponential Smoothing with additive trend"

    return model_settings, algorithm_label


# ============================================================
# SCRUM-88: Build and train forecasting model
# ============================================================
def execute_model_fitting(timeline_series, configurations):
    estimator = ExponentialSmoothing(timeline_series, **configurations)
    return estimator.fit(optimized=True)


# ============================================================
# SCRUM-89: Generate future sales predictions
# ============================================================
def compile_prediction_matrices(fitted_pipeline, step_window):
    raw_array = fitted_pipeline.forecast(step_window).mask(lambda val: val < 0, 0)
    
    return pd.DataFrame(
        data=raw_array.values,
        index=raw_array.index,
        columns=["ForecastSales"]
    ).reset_index().rename(columns={"index": "Date"})


# ============================================================
# SCRUM-90: Calculate forecast accuracy and test the model
# ============================================================
def run_model_backtest_metrics(timeline_series, validation_window=14):
    if len(timeline_series) <= (validation_window + 14):
        return None

    # Slice sequences into validation arrays
    training_block = timeline_series.iloc[:-validation_window]
    validation_block = timeline_series.iloc[-validation_window:]

    # Map settings and fit via inner pipeline calls
    inner_settings, _ = evaluate_forecasting_logic(training_block)
    backtested_pipeline = execute_model_fitting(training_block, inner_settings)

    # Process testing arrays
    projected_array = backtested_pipeline.forecast(validation_window).mask(lambda val: val < 0, 0)

    ground_truth = validation_block.to_numpy()
    estimated_truth = projected_array.to_numpy()

    # Calculate absolute baseline error scales
    mean_abs_deviation = np.mean(np.abs(ground_truth - estimated_truth))
    root_mean_sq_deviation = np.sqrt(np.mean((ground_truth - estimated_truth) ** 2))

    valid_indices = ground_truth != 0

    if np.any(valid_indices):
        mean_percentage_error = (
            np.mean(
                np.abs((ground_truth[valid_indices] - estimated_truth[valid_indices]) / ground_truth[valid_indices])
            )
            * 100
        )
        scaled_accuracy = max(0.0, 100.0 - mean_percentage_error)
    else:
        mean_percentage_error = np.nan
        scaled_accuracy = np.nan

    return {
        "MAE": mean_abs_deviation,
        "RMSE": root_mean_sq_deviation,
        "MAPE": mean_percentage_error,
        "Accuracy": scaled_accuracy,
    }


# ============================================================
# Load CSV or Excel file
# ============================================================
def extract_uploaded_bytestream(file_buffer):
    target_extension = file_buffer.name.lower()

    if target_extension.endswith(".csv"):
        return pd.read_csv(file_buffer)
    if target_extension.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_buffer)

    raise ValueError("Unsupported file type. Please upload CSV, XLSX or XLS.")


# ============================================================
# Streamlit interface
# ============================================================
st.title("SalesInsight - Sales Forecasting System")

st.write(
    "Upload historical sales data in CSV or Excel format "
    "to generate future sales predictions."
)

data_stream = st.file_uploader(
    "Upload sales data",
    type=["csv", "xlsx", "xls"],
    help="Supported formats: CSV, XLSX and XLS.",
)

if data_stream is not None:
    try:
        # Load uploaded data
        df = extract_uploaded_bytestream(data_stream)

        st.success(f"File '{data_stream.name}' uploaded successfully.")

        # Check required columns
        structure_targets = ["InvoiceDate", "Quantity", "UnitPrice"]
        absent_fields = [field for field in structure_targets if field not in df.columns]

        if absent_fields:
            st.error(f"Missing required columns: {', '.join(absent_fields)}")
            st.stop()

        st.write(f"Uploaded records: {len(df):,}")

        # ----------------------------------------------------
        # SCRUM-86
        # ----------------------------------------------------
        historical_sales = transform_transactional_records(df)

        st.subheader("Historical Sales Data")

        st.write(f"Historical days available: {len(historical_sales):,}")
        st.write(f"Total historical sales: ${historical_sales.sum():,.2f}")

        # Assemble preview arrays using direct pandas parameters
        st.dataframe(
            data=historical_sales.tail(10).rename("Sales").reset_index().rename(columns={"InvoiceDate": "Date"}),
            use_container_width=True,
            hide_index=True,
        )

        # ----------------------------------------------------
        # SCRUM-87
        # ----------------------------------------------------
        hyperparameters, method_description = evaluate_forecasting_logic(historical_sales)

        st.subheader("Forecasting Method")
        st.info(method_description)

        prediction_days = st.slider(
            label="Prediction horizon (days)",
            min_value=7,
            max_value=60,
            value=30,
        )

        # ----------------------------------------------------
        # SCRUM-88
        # ----------------------------------------------------
        trained_pipeline = execute_model_fitting(historical_sales, hyperparameters)

        st.success("Forecasting model trained successfully.")

    except Exception as application_fault:
        st.error(f"System execution failure: {application_fault}")
                # ----------------------------------------------------
        # SCRUM-89
        # ----------------------------------------------------
        forecast_dataframe = compile_prediction_matrices(
            trained_pipeline,
            prediction_days,
        )

        st.subheader("Future Sales Predictions")

        st.dataframe(
            data=forecast_dataframe,
            use_container_width=True,
            hide_index=True,
        )

        # Forecast chart
        past_records = (
            historical_sales
            .tail(180)
            .rename("Sales")
            .reset_index()
            .rename(columns={"InvoiceDate": "Date"})
            .assign(Type="Historical")
        )

        future_records = forecast_dataframe.rename(
            columns={"ForecastSales": "Sales"}
        ).assign(Type="Forecast")

        visualization_matrix = pd.concat(
            [past_records, future_records],
            axis=0,
            ignore_index=True,
        )[["Date", "Sales", "Type"]]

        timeseries_graph = px.line(
            data_frame=visualization_matrix,
            x="Date",
            y="Sales",
            color="Type",
            title="Historical Sales vs Future Forecast",
        )

        timeseries_graph.update_layout(height=500)

        st.plotly_chart(timeseries_graph, use_container_width=True)

        aggregated_prediction = forecast_dataframe["ForecastSales"].sum()

        st.metric(
            label=f"Projected Sales - Next {prediction_days} Days",
            value=f"${aggregated_prediction:,.2f}",
        )

        # ----------------------------------------------------
        # SCRUM-90
        # ----------------------------------------------------
        accuracy_results = run_model_backtest_metrics(
            historical_sales,
            validation_window=14,
        )

        if accuracy_results is not None:
            st.subheader("Forecast Accuracy Testing")

            layout_col1, layout_col2, layout_col3, layout_col4 = st.columns(4)

            layout_col1.metric(
                label="MAE",
                value=f"${accuracy_results['MAE']:,.2f}",
            )
            layout_col2.metric(
                label="RMSE",
                value=f"${accuracy_results['RMSE']:,.2f}",
            )

            is_mape_invalid = pd.isna(accuracy_results["MAPE"])
            if is_mape_invalid:
                layout_col3.metric(label="MAPE", value="N/A")
            else:
                layout_col3.metric(
                    label="MAPE",
                    value=f"{accuracy_results['MAPE']:.2f}%",
                )

            is_acc_invalid = pd.isna(accuracy_results["Accuracy"])
            if is_acc_invalid:
                layout_col4.metric(label="Accuracy", value="N/A")
            else:
                layout_col4.metric(
                    label="Accuracy",
                    value=f"{accuracy_results['Accuracy']:.2f}%",
                )
        else:
            st.warning(
                "Not enough historical data to calculate forecast accuracy."
            )

        # Download forecast
        exported_bytestream = forecast_dataframe.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Sales Forecast",
            data=exported_bytestream,
            file_name="sales_forecast.csv",
            mime="text/csv",
        )

    except Exception as application_fault:
        st.error(
            f"Unable to complete sales forecasting: {application_fault}"
        )
