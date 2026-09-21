import pandas as pd
def create_product_summary(df):
    return (
        df.groupby(["StockCode", "Description"], as_index=False)
        .agg(
            TotalQuantity=("Quantity", "sum"),
            TotalSales=("TotalSales", "sum"),
            Transactions=("InvoiceNo", "nunique"), )
        .sort_values("TotalSales", ascending=False))

def create_customer_summary(df):
    return (
        df.groupby("CustomerID", as_index=False)
        .agg(
            TotalOrders=("InvoiceNo", "nunique"),
            TotalQuantity=("Quantity", "sum"),
            TotalSales=("TotalSales", "sum"),
        )
        .sort_values("TotalSales", ascending=False))
REQUIRED_COLS = [
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country"
]

def load_data(file_input):
    if not file_input:
        raise ValueError("No file provided.")
    if not getattr(file_input, "name", "").lower().endswith(".csv"):
        raise ValueError("Please upload a valid .csv file.")

    try:
        return pd.read_csv(file_input)
    except Exception as e:
        raise ValueError(f"Failed to parse CSV: {e}")

def validate_columns(df):
    if df.empty:
        raise ValueError("Uploaded CSV contains no rows.")
    
    missing = set(REQUIRED_COLS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

def clean_data(df):
    df = df.copy()

    # Handle missing text values
    df["Description"] = df["Description"].fillna("Unknown Product")
    df["Country"] = df["Country"].fillna("Unknown")

    # Remove rows missing essential transaction information
    df = df.dropna(
        subset=["InvoiceNo", "StockCode", "Quantity", "UnitPrice", "InvoiceDate"]
    )

    # Keep missing customer IDs without deleting valid sales
    df["CustomerID"] = df["CustomerID"].fillna("Guest")

    # Remove duplicate records
    df = df.drop_duplicates()

    # Standardise CustomerID and remove trailing .0
    df["CustomerID"] = df["CustomerID"].astype(str).str.removesuffix(".0")

    # Clean up whitespace across text columns
    str_cols = ["InvoiceNo", "StockCode", "Description", "Country"]
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()

    return df

def transform_data(df):
    # Extract date and monthly time periods for easy grouping
    df = df.copy()

    # Convert data types first
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    # Remove invalid records
    df = df.dropna(subset=["Quantity", "UnitPrice", "InvoiceDate"])

    # Calculate sales information
    df["IsReturn"] = (
    df["InvoiceNo"].astype(str).str.startswith("C")
        | (df["Quantity"] < 0)
    )
    df["TotalSales"] = df["Quantity"] * df["UnitPrice"]

    # Create date columns
    df["SaleDate"] = df["InvoiceDate"].dt.date
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    df["Year"] = df["InvoiceDate"].dt.year
    df["Month"] = df["InvoiceDate"].dt.month
    df["MonthName"] = df["InvoiceDate"].dt.month_name()
    df["Day"] = df["InvoiceDate"].dt.day
    df["Hour"] = df["InvoiceDate"].dt.hour

    # Daily and monthly sales
    df["DailySales"] = (
        df.groupby("SaleDate")["TotalSales"].transform("sum")
    )
    df["MonthlySales"] = (
        df.groupby("YearMonth")["TotalSales"].transform("sum")
    )
    return df


def summarize_by_product(df):
    # Group by product details and aggregate key performance metrics
    product_summary = (
        df.groupby(["StockCode", "Description"], as_index=False)
        .agg( TotalQuantity=("Quantity", "sum"),
            TotalSales=("TotalSales", "sum"),
        )
        .sort_values(by="TotalSales", ascending=False) )
    return product_summary

def summarize_by_customer(df):
    # Roll up sales data by customer ID to find top spenders
    customer_summary = (
        df.groupby("CustomerID", as_index=False)
        .agg(
            TotalOrders=("InvoiceNo", "nunique"),
            TotalQuantity=("Quantity", "sum"),
            TotalSales=("TotalSales", "sum"),
        )
        .sort_values(by="TotalSales", ascending=False)
    )
    return customer_summary


def check_data_quality(df):
    # Sanity check to make sure basic constraints are met before exporting
    if df.empty:
        print("Warning: The dataset is empty.")
        return False

    # Check for unexpected missing values in critical columns
    missing_counts = df[["InvoiceNo", "TotalSales"]].isnull().sum()
    if missing_counts.sum() > 0:
        print("Warning: Found unexpected missing values in key fields.")
        return False

    print("Data validation passed successfully.")
    return True
def prepare_forecasting_data(df):
    # Aggregate daily totals needed for time-series modeling
    daily_summary = (
        df.groupby("SaleDate", as_index=False)
        .agg(TotalSales=("TotalSales", "sum"),
            TotalQuantity=("Quantity", "sum"),
            TotalOrders=("InvoiceNo", "nunique"),
            UniqueCustomers=("CustomerID", "nunique"),
            ReturnTransactions=("IsReturn", "sum"), )
        .sort_values(by="SaleDate") )

    # Convert to datetime and extract date features for trend/seasonality analysis
    daily_summary["SaleDate"] = pd.to_datetime(daily_summary["SaleDate"])
    
    daily_summary["Year"] = daily_summary["SaleDate"].dt.year
    daily_summary["Month"] = daily_summary["SaleDate"].dt.month
    daily_summary["DayOfWeek"] = daily_summary["SaleDate"].dt.day_name()

    return daily_summary
def create_forecasting_dataset(df):
    forecasting_df = (
        df.groupby("SaleDate", as_index=False)
        .agg(
            TotalSales=("TotalSales", "sum"),
            TotalQuantity=("Quantity", "sum"),
            TotalOrders=("InvoiceNo", "nunique"),
            UniqueCustomers=("CustomerID", "nunique"),
            ReturnTransactions=("IsReturn", "sum"),
        )
        .sort_values("SaleDate")
    )

    forecasting_df["SaleDate"] = pd.to_datetime(
        forecasting_df["SaleDate"]
    )
    forecasting_df["Year"] = forecasting_df["SaleDate"].dt.year
    forecasting_df["Month"] = forecasting_df["SaleDate"].dt.month
    forecasting_df["DayOfWeek"] = forecasting_df["SaleDate"].dt.day_name()

    return forecasting_df
def validate_cleaned_data(df):
    if df.empty:
        raise ValueError("No valid records remain after cleaning.")
# Final list of columns we want to keep in our output
    required_output_cols = [
        "IsReturn",
        "TotalSales",
        "Year",
        "Month",
        "Day",
        "Hour",
        "SaleDate",
        "YearMonth",
        "DailySales",
        "MonthlySales",
    ]
    essential_cols = [
        "InvoiceNo",
        "StockCode",
        "Quantity",
        "UnitPrice",
        "InvoiceDate",
    ]

    if df[essential_cols].isnull().any().any():
        raise ValueError("Cleaned data still contains missing essential values.")

    if df.duplicated().any():
        raise ValueError("Cleaned data still contains duplicate records.")

    required_output_cols = ["IsReturn", "TotalSales", "Year", "Month", "Day", "Hour"]
    missing_output = set(required_output_cols) - set(df.columns)

    if missing_output:
        raise ValueError(
            f"Missing processed columns: {', '.join(sorted(missing_output))}"
        )
def run_pipeline(uploaded_file):
    raw = load_data(uploaded_file)
    validate_columns(raw)
    missing_before = int(raw.isnull().sum().sum())
    dupes = int(raw.duplicated().sum())
    
    cleaned = clean_data(raw)
    final_df = transform_data(cleaned)
    validate_cleaned_data(final_df)
    missing_after = int(final_df.isnull().sum().sum())
    stats = {
        "original_rows": len(raw),
        "processed_rows": len(final_df),
        "removed_rows": len(raw) - len(final_df),
        "duplicate_rows": dupes,
        "missing_values_handled": missing_before - missing_after,
    }

    return final_df, stats