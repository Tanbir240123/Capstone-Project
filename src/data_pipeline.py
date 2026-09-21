import pandas as pd

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
    # Coerce dynamic types
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    # Drop unparseable records
    df = df.dropna(subset=["Quantity", "UnitPrice", "InvoiceDate"])

    # Add calculated columns
    df["IsReturn"] = df["InvoiceNo"].str.startswith("C") | (df["Quantity"] < 0)
    df["TotalSales"] = df["Quantity"] * df["UnitPrice"]

    # Extract date parts
    dates = df["InvoiceDate"].dt
    df["Year"] = dates.year
    df["Month"] = dates.month
    df["MonthName"] = dates.month_name()
    df["Day"] = dates.day
    df["Hour"] = dates.hour

    return df
def validate_cleaned_data(df):
    if df.empty:
        raise ValueError("No valid records remain after cleaning.")

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