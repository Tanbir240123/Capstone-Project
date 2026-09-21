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
    # Drop exact duplicates and missing critical info
    df = df.drop_duplicates()
    df = df.dropna(subset=["InvoiceNo", "StockCode", "Description"])

    # Clean CustomerID: replace missing values and strip trailing floats (e.g. 12345.0 -> 12345)
    customer_ids = df["CustomerID"].fillna("Unknown").astype(str)
    df["CustomerID"] = customer_ids.str.removesuffix(".0")

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

def run_pipeline(uploaded_file):
    raw = load_data(uploaded_file)
    validate_columns(raw)
    
    dupes = int(raw.duplicated().sum())
    
    cleaned = clean_data(raw)
    final_df = transform_data(cleaned)

    stats = {
        "original_rows": len(raw),
        "processed_rows": len(final_df),
        "removed_rows": len(raw) - len(final_df),
        "duplicate_rows": dupes,
    }

    return final_df, stats