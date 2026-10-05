from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from dotenv import load_dotenv

from pathlib import Path
from io import BytesIO
import os
import json
import uuid
import re

import httpx
import numpy as np
import pandas as pd


# ============================================================
# ENVIRONMENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_FILE,
    override=True
)

ANTHROPIC_API_KEY = os.getenv(
    "ANTHROPIC_API_KEY",
    ""
).strip()

ANTHROPIC_MODEL = os.getenv(
    "ANTHROPIC_MODEL",
    "claude-sonnet-4-5"
).strip()


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="SalesInsight API",
    version="3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# IN-MEMORY DATA STORE
# ============================================================

DATASETS = {}


# ============================================================
# BASIC HELPERS
# ============================================================

def clean_column_name(value):
    return (
        str(value)
        .strip()
        .replace("\n", " ")
        .replace("\t", " ")
    )


def normalise_columns(df):
    df = df.copy()

    df.columns = [
        clean_column_name(c)
        for c in df.columns
    ]

    return df


def sample_for_llm(df, rows=8):
    sample = df.head(rows).copy()

    return sample.astype(object).where(
        pd.notna(sample),
        None
    ).to_dict(
        orient="records"
    )


def safe_float(value):
    try:
        value = float(value)

        if np.isnan(value) or np.isinf(value):
            return 0.0

        return value

    except Exception:
        return 0.0


def safe_int(value):
    try:
        return int(value)
    except Exception:
        return 0


def money(value):
    return round(safe_float(value), 2)


# ============================================================
# COLUMN DETECTION
# ============================================================

ALIASES = {
    "invoice": [
        "InvoiceNo",
        "Invoice No",
        "Invoice_Number",
        "Transaction_ID",
        "Transaction ID",
        "Order_ID",
        "Order ID",
        "Transaction"
    ],

    "date": [
        "InvoiceDate",
        "Invoice Date",
        "Sale_Date",
        "Sales_Date",
        "Order_Date",
        "Order Date",
        "Date",
        "Timestamp",
        "SaleDate"
    ],

    "quantity": [
        "Quantity",
        "Qty",
        "Units",
        "Units_Sold",
        "Quantity_Sold",
        "quantiy"
    ],

    "unit_price": [
        "UnitPrice",
        "Unit Price",
        "Price",
        "Selling_Price",
        "Selling Price",
        "price_per_unit",
    ],

    "sales": [
        "SalesAmount",
        "Sales Amount",
        "Sales_Amount",
        "Sales",
        "Revenue",
        "Total_Sales",
        "Total Sales",
        "Amount",
        "TotalAmount",
        "Total Amount",
        "total_sale",
    ],

    "customer": [
        "CustomerID",
        "Customer ID",
        "Customer",
        "Customer_Name",
        "Customer Name"
    ],

    "product": [
        "Description",
        "Product",
        "Product_Name",
        "Product Name",
        "Product_ID",
        "Product ID",
        "Item",
        "Item_Name"
    ],

    "product_code": [
        "StockCode",
        "Stock Code",
        "Product_ID",
        "Product ID",
        "Item_ID",
        "Item ID"
    ],

    "category": [
        "Category",
        "Product_Category",
        "Product Category",
        "Department",
        "Product_Type",
        "Product Type"
    ],

    "country": [
        "Country",
        "Region",
        "Location"
    ]
}


def find_column(df, aliases):
    lookup = {
        clean_column_name(c).lower(): c
        for c in df.columns
    }

    for alias in aliases:

        key = clean_column_name(alias).lower()

        if key in lookup:
            return lookup[key]

    # Slightly more flexible matching
    for column in df.columns:

        column_key = (
            clean_column_name(column)
            .lower()
            .replace("_", "")
            .replace(" ", "")
        )

        for alias in aliases:

            alias_key = (
                clean_column_name(alias)
                .lower()
                .replace("_", "")
                .replace(" ", "")
            )

            if column_key == alias_key:
                return column

    return None


def detect_columns(df):

    mapping = {}

    for role, aliases in ALIASES.items():

        mapping[role] = find_column(
            df,
            aliases
        )

    return mapping


# ============================================================
# CATEGORY CREATION
# ============================================================

def infer_category(df, product_column):

    if not product_column:
        return pd.Series(
            ["Unknown"] * len(df),
            index=df.index
        )

    values = (
        df[product_column]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    def classify(value):

        text = value.lower()

        if any(
            word in text
            for word in [
                "laptop",
                "computer",
                "keyboard",
                "mouse",
                "monitor",
                "phone",
                "mobile",
                "tablet"
            ]
        ):
            return "Electronics"

        if any(
            word in text
            for word in [
                "shirt",
                "dress",
                "jeans",
                "shoe",
                "jacket",
                "clothing"
            ]
        ):
            return "Fashion"

        if any(
            word in text
            for word in [
                "coffee",
                "tea",
                "food",
                "snack",
                "drink"
            ]
        ):
            return "Food & Beverage"

        if any(
            word in text
            for word in [
                "chair",
                "table",
                "desk",
                "sofa",
                "furniture"
            ]
        ):
            return "Furniture"

        return "Other"

    return values.apply(classify)


# ============================================================
# DATA PREPARATION
# ============================================================

def prepare_dataset(df):

    df = normalise_columns(df)

    original_rows = len(df)

    mapping = detect_columns(df)

    date_col = mapping["date"]

    if not date_col:
        raise ValueError(
            "A date column could not be detected. "
            "Please provide a column such as Date, Sale_Date, "
            "InvoiceDate or Order_Date."
        )

    # --------------------------------------------------------
    # Date
    # --------------------------------------------------------

    df["__date"] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Quantity
    # --------------------------------------------------------

    quantity_col = mapping["quantity"]

    if quantity_col:

        df["__quantity"] = pd.to_numeric(
            df[quantity_col],
            errors="coerce"
        ).fillna(1)

    else:

        df["__quantity"] = 1

    # --------------------------------------------------------
    # Unit price
    # --------------------------------------------------------

    price_col = mapping["unit_price"]

    if price_col:

        df["__unit_price"] = pd.to_numeric(
            df[price_col],
            errors="coerce"
        ).fillna(0)

    else:

        df["__unit_price"] = 0

    # --------------------------------------------------------
    # Sales
    # --------------------------------------------------------

    sales_col = mapping["sales"]

    if sales_col:

        df["__sales"] = pd.to_numeric(
            df[sales_col],
            errors="coerce"
        )

    else:

        df["__sales"] = (
            df["__quantity"]
            * df["__unit_price"]
        )

    # --------------------------------------------------------
    # Product
    # --------------------------------------------------------

    product_col = mapping["product"]

    if product_col:

        df["__product"] = (
            df[product_col]
            .fillna("Unknown")
            .astype(str)
        )

    else:

        df["__product"] = "Unknown"

    # --------------------------------------------------------
    # Customer
    # --------------------------------------------------------

    customer_col = mapping["customer"]

    if customer_col:

        df["__customer"] = (
            df[customer_col]
            .fillna("Unknown")
            .astype(str)
        )

    else:

        df["__customer"] = "Unknown"

    # --------------------------------------------------------
    # Country
    # --------------------------------------------------------

    country_col = mapping["country"]

    if country_col:

        df["__country"] = (
            df[country_col]
            .fillna("Unknown")
            .astype(str)
        )

    else:

        df["__country"] = "Unknown"

    # --------------------------------------------------------
    # Category
    # --------------------------------------------------------

    category_col = mapping["category"]

    if category_col:

        df["__category"] = (
            df[category_col]
            .fillna("Unknown")
            .astype(str)
        )

    else:

        df["__category"] = infer_category(
            df,
            product_col
        )

    # --------------------------------------------------------
    # Remove unusable rows
    # --------------------------------------------------------

    before_clean = len(df)

    df = df.dropna(
        subset=["__date"]
    )

    df = df[
        df["__sales"].notna()
    ]

    df = df[
        np.isfinite(df["__sales"])
    ]

    duplicate_rows = int(
        df.duplicated().sum()
    )

    df = df.drop_duplicates()

    removed_rows = (
        original_rows
        - len(df)
    )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    df = df.sort_values(
        "__date"
    ).reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # Final mapping
    # --------------------------------------------------------

    public_mapping = {
        "InvoiceDate": mapping["date"],
        "Quantity": mapping["quantity"],
        "UnitPrice": mapping["unit_price"],
        "SalesAmount": mapping["sales"],
        "Description": mapping["product"],
        "Category": mapping["category"],
        "CustomerID": mapping["customer"],
        "Country": mapping["country"],
        "ProductCode": mapping["product_code"]
    }

    quality = {
        "processed_rows": int(len(df)),
        "original_rows": int(original_rows),
        "removed_rows": int(removed_rows),
        "duplicate_rows": int(duplicate_rows),
        "columns": int(len(df.columns))
    }

    return (
        df,
        public_mapping,
        quality
    )


# ============================================================
# ANTHROPIC / CLAUDE
# ============================================================

async def llm_profile(df):

    if not ANTHROPIC_API_KEY:

        return (
            None,
            "Claude is not configured. "
            "Add ANTHROPIC_API_KEY to backend/.env and restart the backend."
        )

    columns = [
        str(c)
        for c in df.columns
        if not str(c).startswith("__")
    ]

    dtypes = {
        str(c): str(df[c].dtype)
        for c in df.columns
        if not str(c).startswith("__")
    }

    missing = {
        str(c): int(df[c].isna().sum())
        for c in df.columns
        if not str(c).startswith("__")
    }

    prompt = {
        "task": (
            "Analyse this retail sales dataset for "
            "SalesInsight."
        ),

        "columns": columns,

        "data_types": dtypes,

        "missing_values": missing,

        "sample_rows": sample_for_llm(df),

        "roles": [
            "date",
            "sales",
            "quantity",
            "unit_price",
            "customer",
            "product",
            "product_code",
            "category",
            "transaction",
            "country"
        ],

        "instructions": [
            "Map roles only to supplied column names.",
            "Do not invent column names.",
            "Do not invent numerical business metrics.",
            "Return 3 to 5 useful observations.",
            "Return valid JSON."
        ]
    }

    request_body = {

        "model": ANTHROPIC_MODEL,

        "max_tokens": 1600,

        "temperature": 0,

        "system": (
            "You are the AI data analysis assistant "
            "for SalesInsight. "
            "Return JSON only."
        ),

        "messages": [
            {
                "role": "user",
                "content": json.dumps(
                    prompt,
                    default=str
                )
            }
        ]
    }

    try:

        async with httpx.AsyncClient(
            timeout=60
        ) as client:

            response = await client.post(

                "https://api.anthropic.com/v1/messages",

                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },

                json=request_body
            )

        if response.status_code != 200:

            try:

                error_data = response.json()

                message = (
                    error_data
                    .get("error", {})
                    .get(
                        "message",
                        response.text
                    )
                )

            except Exception:

                message = response.text

            print(
                "Anthropic error:",
                response.status_code,
                message
            )

            return (
                None,
                f"Claude API error "
                f"{response.status_code}: {message}"
            )

        data = response.json()

        text = ""

        for item in data.get(
            "content",
            []
        ):

            if item.get("type") == "text":

                text += item.get(
                    "text",
                    ""
                )

        text = text.strip()

        text = re.sub(
            r"^```json\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\s*```$",
            "",
            text
        )

        result = json.loads(
            text
        )

        return (
            result,
            f"Claude AI analysis completed using {ANTHROPIC_MODEL}."
        )

    except json.JSONDecodeError:

        return (
            None,
            "Claude responded, but the response was not valid JSON."
        )

    except httpx.TimeoutException:

        return (
            None,
            "Claude request timed out."
        )

    except Exception as exc:

        print(
            "Claude exception:",
            repr(exc)
        )

        return (
            None,
            f"Claude connection error: "
            f"{type(exc).__name__}: {exc}"
        )


# ============================================================
# AI INSIGHTS
# ============================================================

def create_fallback_insights(df):

    insights = []

    total_sales = df["__sales"].sum()

    if len(df) > 0:

        average = (
            total_sales / len(df)
        )

        insights.append(
            f"Average sales value per record is "
            f"${average:,.2f}."
        )

    top_product = (
        df.groupby("__product")["__sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(1)
    )

    if len(top_product):

        product = top_product.index[0]

        value = top_product.iloc[0]

        insights.append(
            f"The highest-sales product is "
            f"{product}, generating "
            f"${value:,.2f}."
        )

    date_min = df["__date"].min()
    date_max = df["__date"].max()

    insights.append(
        f"The dataset covers sales from "
        f"{date_min:%Y-%m-%d} to "
        f"{date_max:%Y-%m-%d}."
    )

    return insights


# ============================================================
# UPLOAD
# ============================================================

@app.post("/api/upload")
async def upload_dataset(
    file: UploadFile = File(...)
):

    filename = (
        file.filename or ""
    ).lower()

    if not filename.endswith(
        (
            ".csv",
            ".xlsx",
            ".xls"
        )
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Only CSV, XLSX and XLS "
                "files are supported."
            )
        )

    try:

        raw = await file.read()

        if filename.endswith(".csv"):

            df = pd.read_csv(
                BytesIO(raw)
            )

        else:

            df = pd.read_excel(
                BytesIO(raw)
            )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=f"Could not read dataset: {exc}"
        )

    try:

        df, mapping, quality = prepare_dataset(
            df
        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    ai_result, llm_status = await llm_profile(
        df
    )

    # --------------------------------------------------------
    # AI insights
    # --------------------------------------------------------

    insights = []

    if ai_result:

        raw_insights = ai_result.get(
            "insights",
            []
        )

        if isinstance(
            raw_insights,
            list
        ):

            insights = [
                str(x)
                for x in raw_insights
            ]

    if not insights:

        insights = create_fallback_insights(
            df
        )

    # --------------------------------------------------------
    # Dataset ID
    # --------------------------------------------------------

    dataset_id = str(
        uuid.uuid4()
    )

    DATASETS[dataset_id] = df

    return {

        "dataset_id": dataset_id,

        "filename": file.filename,

        "rows": len(df),

        "quality": quality,

        "mapping": mapping,

        "insights": insights,

        "llm_status": llm_status,

        "llm_configured": bool(
            ANTHROPIC_API_KEY
        )
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/api/health")
def health():

    return {

        "status": "ok",

        "llm_configured": bool(
            ANTHROPIC_API_KEY
        ),

        "anthropic_model": ANTHROPIC_MODEL
    }


# ============================================================
# DATASET HELPER
# ============================================================

def get_dataset(dataset_id):

    if dataset_id not in DATASETS:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    return DATASETS[dataset_id]


# ============================================================
# DASHBOARD
# ============================================================

@app.get(
    "/api/datasets/{dataset_id}/dashboard"
)
def dashboard(dataset_id: str):

    df = get_dataset(
        dataset_id
    )

    sales = df["__sales"].sum()

    transactions = len(df)

    customers = (
        df["__customer"]
        .replace("Unknown", np.nan)
        .nunique()
    )

    products = (
        df["__product"]
        .nunique()
    )

    units = df[
        "__quantity"
    ].sum()

    aov = (
        sales / transactions
        if transactions
        else 0
    )

    monthly = (
        df.assign(
            month=df["__date"]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby("month")["__sales"]
        .sum()
        .reset_index()
    )

    monthly = [
        {
            "month": row["month"],
            "sales": money(row["__sales"])
        }
        for _, row in monthly.iterrows()
    ]

    top_products = (
        df.groupby("__product")["__sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
        .reset_index()
    )

    top_products = [
        {
            "product": str(row["__product"]),
            "sales": money(row["__sales"])
        }
        for _, row in top_products.iterrows()
    ]

    return {

        "sales": money(sales),

        "transactions": transactions,

        "customers": int(customers),

        "products": int(products),

        "units": money(units),

        "aov": money(aov),

        "monthly": monthly,

        "top_products": top_products
    }


# ============================================================
# SALES
# ============================================================

@app.get(
    "/api/datasets/{dataset_id}/sales"
)
def sales_analysis(dataset_id: str):

    df = get_dataset(
        dataset_id
    )

    monthly = (
        df.assign(
            month=df["__date"]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby("month")["__sales"]
        .sum()
        .reset_index()
    )

    daily = (
        df.assign(
            date=df["__date"]
            .dt.date
            .astype(str)
        )
        .groupby("date")["__sales"]
        .sum()
        .reset_index()
    )

    country = (
        df.groupby("__country")["__sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(15)
        .reset_index()
    )

    returns = int(
        (df["__sales"] < 0).sum()
    )

    return {

        "kpis": {

            "sales": money(
                df["__sales"].sum()
            ),

            "transactions": len(df),

            "units": money(
                df["__quantity"].sum()
            ),

            "returns": returns
        },

        "monthly": [
            {
                "month": row["month"],
                "sales": money(row["__sales"])
            }
            for _, row in monthly.iterrows()
        ],

        "daily": [
            {
                "date": row["date"],
                "sales": money(row["__sales"])
            }
            for _, row in daily.iterrows()
        ],

        "country": [
            {
                "country": str(row["__country"]),
                "sales": money(row["__sales"])
            }
            for _, row in country.iterrows()
        ]
    }


# ============================================================
# PRODUCTS
# ============================================================

@app.get(
    "/api/datasets/{dataset_id}/products"
)
def product_analysis(dataset_id: str):

    df = get_dataset(
        dataset_id
    )

    products = (
        df.groupby(
            [
                "__product",
                "__category"
            ]
        )
        .agg(
            TotalQuantity=(
                "__quantity",
                "sum"
            ),

            TotalSales=(
                "__sales",
                "sum"
            ),

            Transactions=(
                "__sales",
                "count"
            )
        )
        .reset_index()
        .sort_values(
            "TotalSales",
            ascending=False
        )
    )

    categories = (
        df.groupby("__category")[
            "__sales"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    product_rows = []

    for _, row in products.iterrows():

        product_rows.append({

            "StockCode": "",

            "Description": str(
                row["__product"]
            ),

            "Category": str(
                row["__category"]
            ),

            "TotalQuantity": money(
                row["TotalQuantity"]
            ),

            "TotalSales": money(
                row["TotalSales"]
            ),

            "Transactions": int(
                row["Transactions"]
            )
        })

    category_rows = [

        {
            "Category": str(
                row["__category"]
            ),

            "sales": money(
                row["__sales"]
            )
        }

        for _, row in categories.iterrows()
    ]

    return {

        "categories": category_rows,

        "products": product_rows
    }


# ============================================================
# CUSTOMERS
# ============================================================

@app.get(
    "/api/datasets/{dataset_id}/customers"
)
def customer_analysis(dataset_id: str):

    df = get_dataset(
        dataset_id
    )

    customer_df = df[
        df["__customer"] != "Unknown"
    ]

    customers = (
        customer_df
        .groupby("__customer")
        .agg(
            TotalOrders=(
                "__sales",
                "count"
            ),

            TotalQuantity=(
                "__quantity",
                "sum"
            ),

            TotalSales=(
                "__sales",
                "sum"
            )
        )
        .reset_index()
        .sort_values(
            "TotalSales",
            ascending=False
        )
    )

    countries = (
        df.groupby("__country")[
            "__sales"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(15)
        .reset_index()
    )

    customer_rows = [

        {
            "CustomerID": str(
                row["__customer"]
            ),

            "TotalOrders": int(
                row["TotalOrders"]
            ),

            "TotalQuantity": money(
                row["TotalQuantity"]
            ),

            "TotalSales": money(
                row["TotalSales"]
            )
        }

        for _, row in customers.iterrows()
    ]

    country_rows = [

        {
            "country": str(
                row["__country"]
            ),

            "sales": money(
                row["__sales"]
            )
        }

        for _, row in countries.iterrows()
    ]

    return {

        "customers": customer_rows,

        "countries": country_rows
    }


# ============================================================
# FORECAST
# ============================================================

@app.get(
    "/api/datasets/{dataset_id}/forecast"
)
def forecast(dataset_id: str):

    df = get_dataset(
        dataset_id
    )

    monthly = (
        df.set_index("__date")[
            "__sales"
        ]
        .resample("MS")
        .sum()
    )

    monthly = monthly[
        monthly.notna()
    ]

    if len(monthly) < 4:

        raise HTTPException(
            status_code=400,
            detail=(
                "At least four months of "
                "sales history are required "
                "for forecasting."
            )
        )

    forecast_values = None

    # --------------------------------------------------------
    # ARIMA
    # --------------------------------------------------------

    try:

        from statsmodels.tsa.arima.model import ARIMA

        model = ARIMA(
            monthly,
            order=(1, 1, 1)
        )

        fitted = model.fit()

        forecast_values = fitted.forecast(
            steps=3
        )

    except Exception as exc:

        print(
            "ARIMA error:",
            exc
        )

        # Fallback: moving average
        average = monthly.tail(3).mean()

        forecast_values = pd.Series(
            [
                average,
                average,
                average
            ]
        )

    periods = pd.date_range(
        monthly.index[-1]
        + pd.offsets.MonthBegin(1),
        periods=3,
        freq="MS"
    )

    rows = []

    for period, value in zip(
        periods,
        forecast_values
    ):

        value = max(
            0,
            safe_float(value)
        )

        rows.append({

            "period": period.strftime(
                "%Y-%m"
            ),

            "predicted": money(value),

            "lower": money(
                value * 0.85
            ),

            "upper": money(
                value * 1.15
            )
        })

    return {

        "next_month": money(
            rows[0]["predicted"]
        ),

        "three_month_total": money(
            sum(
                x["predicted"]
                for x in rows
            )
        ),

        "forecast": rows
    }


# ============================================================
# BUSINESS PERFORMANCE
# ============================================================

@app.get(
    "/api/datasets/{dataset_id}/performance"
)
def performance(dataset_id: str):

    df = get_dataset(
        dataset_id
    )

    monthly = (
        df.assign(
            month=df["__date"]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby("month")["__sales"]
        .sum()
        .sort_index()
    )

    if len(monthly) >= 2:

        previous = monthly.iloc[-2]

        current = monthly.iloc[-1]

        growth = (
            (
                current - previous
            )
            / abs(previous)
            * 100
            if previous != 0
            else 0
        )

    else:

        growth = 0

    customers = int(
        df["__customer"]
        .replace("Unknown", np.nan)
        .nunique()
    )

    orders = len(df)

    aov = (
        df["__sales"].sum()
        / orders
        if orders
        else 0
    )

    growth_score = min(
        100,
        max(
            0,
            50 + growth
        )
    )

    customer_score = min(
        100,
        customers
    )

    order_value_score = min(
        100,
        aov / 10
    )

    if len(monthly) >= 2:

        consistency = (
            100
            - min(
                100,
                monthly.pct_change()
                .dropna()
                .std()
                * 100
            )
        )

    else:

        consistency = 50

    score = (
        growth_score * 0.30
        + customer_score * 0.20
        + order_value_score * 0.25
        + consistency * 0.25
    )

    return {

        "score": round(
            score,
            1
        ),

        "growth": round(
            growth,
            1
        ),

        "customers": customers,

        "orders": orders,

        "aov": money(aov),

        "growth_score": round(
            growth_score,
            1
        ),

        "customer_score": round(
            customer_score,
            1
        ),

        "order_value_score": round(
            order_value_score,
            1
        ),

        "consistency_score": round(
            consistency,
            1
        )
    }


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )