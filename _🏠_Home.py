import streamlit as st
import pandas as pd
import plotly.express as px

def extract_uploaded_bytestream(file_buffer):
    
    file_name = file_buffer.name.lower()

    # CSV file
    if file_name.endswith(".csv"):
        return pd.read_csv(file_buffer)

    # Excel file
    elif file_name.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_buffer)

    # Unsupported file
    else:
        raise ValueError("Unsupported file type. Please upload CSV, XLSX or XLS.")

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(page_title="SalesInsight",page_icon="📊",layout="wide")

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* =====================================================
   SALESINSIGHT MODERN THEME
   ===================================================== */

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #eef4ff 0%,
        #f5f3ff 50%,
        #eef7ff 100%
    );
}

/* Main content */
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2.5rem;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

/* =====================================================
   SIDEBAR
   ===================================================== */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #172554 55%,
        #1e1b4b 100%
    );

    color: #f8fafc !important;
}

/* Sidebar general text */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
}

/* Sidebar section labels */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stDateInput label {
    color: #cbd5e1 !important;
    font-weight: 600;
}


/* =====================================================
   DATE RANGE INPUT
   ===================================================== */

[data-testid="stSidebar"] .stDateInput input {
    background-color: #ffffff !important;
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;

    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;

    font-weight: 600 !important;
}


/* =====================================================
   PRODUCT & CATEGORY SELECTBOX
   ===================================================== */

[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}

/* Selectbox text */
[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #172554 !important;
}

/* Selected value */
[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #172554 !important;
    font-weight: 600 !important;
}

/* Selectbox arrow */
[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #172554 !important;
}


/* =====================================================
   DROPDOWN MENU
   ===================================================== */

[data-baseweb="popover"] {
    background-color: #ffffff !important;
}

[data-baseweb="popover"] * {
    color: #172554 !important;
}


/* =====================================================
   SIDEBAR DIVIDER
   ===================================================== */

[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.15) !important;
}


/* =====================================================
   SIDEBAR SCROLLBAR
   ===================================================== */

[data-testid="stSidebar"]::-webkit-scrollbar {
    width: 6px;
}

[data-testid="stSidebar"]::-webkit-scrollbar-track {
    background: #0f172a;
}

[data-testid="stSidebar"]::-webkit-scrollbar-thumb {
    background: #475569;
    border-radius: 10px;
}


/* =====================================================
   SIDEBAR INPUT HOVER
   ===================================================== */

/* =====================================================
   SIDEBAR
   ===================================================== */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #172554 55%,
        #1e1b4b 100%
    );

    color: #f8fafc !important;
}

/* Sidebar general text */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
}

/* Sidebar section labels */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stDateInput label {
    color: #cbd5e1 !important;
    font-weight: 600;
}


/* =====================================================
   DATE RANGE INPUT
   ===================================================== */

[data-testid="stSidebar"] .stDateInput input {
    background-color: #ffffff !important;
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;

    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;

    font-weight: 600 !important;
}


/* =====================================================
   PRODUCT & CATEGORY SELECTBOX
   ===================================================== */

[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}

/* Selectbox text */
[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #172554 !important;
}

/* Selected value */
[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #172554 !important;
    font-weight: 600 !important;
}

/* Selectbox arrow */
[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #172554 !important;
}


/* =====================================================
   DROPDOWN MENU
   ===================================================== */

[data-baseweb="popover"] {
    background-color: #ffffff !important;
}

[data-baseweb="popover"] * {
    color: #172554 !important;
}


/* =====================================================
   SIDEBAR DIVIDER
   ===================================================== */

[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.15) !important;
}


/* =====================================================
   SIDEBAR SCROLLBAR
   ===================================================== */

[data-testid="stSidebar"]::-webkit-scrollbar {
    width: 6px;
}

[data-testid="stSidebar"]::-webkit-scrollbar-track {
    background: #0f172a;
}

[data-testid="stSidebar"]::-webkit-scrollbar-thumb {
    background: #475569;
    border-radius: 10px;
}


/* =====================================================
   SIDEBAR INPUT HOVER
   ===================================================== */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #172554 55%,
        #1e1b4b 100%
    );

    color: #f8fafc !important;
}

/* Sidebar general text */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
}

/* Sidebar section labels */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stDateInput label {
    color: #cbd5e1 !important;
    font-weight: 600;
}


/* =====================================================
   DATE RANGE INPUT
   ===================================================== */

[data-testid="stSidebar"] .stDateInput input {
    background-color: #ffffff !important;
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;

    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;

    font-weight: 600 !important;
}


/* =====================================================
   PRODUCT & CATEGORY SELECTBOX
   ===================================================== */

[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}

/* Selectbox text */
[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #172554 !important;
}

/* Selected value */
[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #172554 !important;
    font-weight: 600 !important;
}

/* Selectbox arrow */
[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #172554 !important;
}


/* =====================================================
   DROPDOWN MENU
   ===================================================== */

[data-baseweb="popover"] {
    background-color: #ffffff !important;
}

[data-baseweb="popover"] * {
    color: #172554 !important;
}


/* =====================================================
   SIDEBAR DIVIDER
   ===================================================== */

[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.15) !important;
}


/* =====================================================
   SIDEBAR SCROLLBAR
   ===================================================== */

[data-testid="stSidebar"]::-webkit-scrollbar {
    width: 6px;
}

[data-testid="stSidebar"]::-webkit-scrollbar-track {
    background: #0f172a;
}

[data-testid="stSidebar"]::-webkit-scrollbar-thumb {
    background: #475569;
    border-radius: 10px;
}


/* =====================================================
   SIDEBAR INPUT HOVER
   ===================================================== */

[data-testid="stSidebar"] .stDateInput input:hover {
    border-color: #60a5fa !important;
    box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.15);
    transition: all 0.25s ease;
}

[data-testid="stSidebar"] div[data-baseweb="select"]:hover {
    box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.15);
    transition: all 0.25s ease;
}

/* =====================================================
   DASHBOARD HEADER
   ===================================================== */

.dashboard-title {
    font-size: 36px;
    font-weight: 800;
    color: #172554;
    margin-bottom: 2px;
    letter-spacing: -0.5px;
}

.dashboard-subtitle {
    color: #64748b;
    font-size: 16px;
    margin-top: 4px;
}


/* =====================================================
   SECTION HEADINGS
   ===================================================== */

.section-title {
    font-size: 24px;
    font-weight: 750;
    color: #172554;
    margin-top: 14px;
    margin-bottom: 12px;
}


/* =====================================================
   KPI CARDS
   ===================================================== */

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.90);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 16px;
    padding: 18px 16px;
    min-height: 115px;

    box-shadow:
        0 6px 20px rgba(15, 23, 42, 0.07);

    transition:
        transform 0.30s ease,
        box-shadow 0.30s ease,
        border-color 0.30s ease;
}

/* KPI hover animation */
div[data-testid="stMetric"]:hover {
    transform: translateY(-6px);

    box-shadow:
        0 14px 30px rgba(37, 99, 235, 0.16);

    border-color: rgba(37, 99, 235, 0.35);
}

div[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #172554 !important;
    font-weight: 800;
}


/* =====================================================
   CHART CONTAINERS
   ===================================================== */

div[data-testid="stPlotlyChart"] {
    background: rgba(255, 255, 255, 0.72);
    border-radius: 16px;
    padding: 8px;

    box-shadow:
        0 5px 18px rgba(15, 23, 42, 0.05);

    transition:
        transform 0.30s ease,
        box-shadow 0.30s ease;
}

div[data-testid="stPlotlyChart"]:hover {
    transform: translateY(-3px);

    box-shadow:
        0 12px 26px rgba(37, 99, 235, 0.10);
}


/* =====================================================
   INSIGHT BOX
   ===================================================== */

.insight-box {
    padding: 18px;
    border-radius: 14px;

    background: linear-gradient(
        135deg,
        #eff6ff,
        #eef2ff
    );

    border-left: 5px solid #4f46e5;

    margin-bottom: 12px;

    box-shadow:
        0 5px 16px rgba(79, 70, 229, 0.08);
}


/* =====================================================
   BUTTONS
   ===================================================== */

.stButton > button {
    border-radius: 10px;
    border: none;

    background: linear-gradient(
        135deg,
        #2563eb,
        #4f46e5
    );

    color: white;
    font-weight: 650;

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 8px 20px rgba(37, 99, 235, 0.25);
}


/* =====================================================
   SELECTBOX / INPUTS
   ===================================================== */

div[data-baseweb="select"] > div {
    border-radius: 10px;
}


/* =====================================================
   DATA TABLE
   ===================================================== */

div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;

    box-shadow:
        0 5px 18px rgba(15, 23, 42, 0.06);
}


/* =====================================================
   DIVIDERS
   ===================================================== */

hr {
    border-color: rgba(100, 116, 139, 0.15);
}


/* =====================================================
   SMOOTH PAGE ENTRY
   ===================================================== */

@keyframes fadeInUp {

    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}

.dashboard-title,
.dashboard-subtitle,
.section-title {
    animation: fadeInUp 0.55s ease-out;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA IMPORT
# =========================================================

st.sidebar.subheader("📥 Import Sales Data")

data_stream = st.sidebar.file_uploader("Upload your sales data",type=["csv", "xlsx", "xls"],help="Upload a CSV or Excel sales file.")

if data_stream is None:

    st.markdown("""
<div style="
    background: linear-gradient(135deg, #eef5ff, #f8f9ff);
    border: 1px solid #d8e5f5;
    border-radius: 24px;
    padding: 50px 45px;
    margin-top: 25px;
    text-align: center;
">

<div style="
    font-size: 52px;
    margin-bottom: 10px;
">
📊
</div>

<div style="
    font-size: 38px;
    font-weight: 800;
    color: #17365d;
    margin-bottom: 10px;
">
Welcome to SalesInsight
</div>

<div style="
    font-size: 20px;
    color: #52657a;
    margin-bottom: 18px;
">
SME Sales Analytics & Forecasting System
</div>

<div style="
    font-size: 16px;
    color: #66788a;
    max-width: 750px;
    margin: 0 auto 30px auto;
">
Turn your sales data into clear business insights.
Upload your CSV or Excel sales file using the sidebar
to explore your business performance.
</div>

<div style="
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 14px;
    margin-bottom: 30px;
">

<div style="
    background: white;
    border: 1px solid #dbe7f5;
    border-radius: 15px;
    padding: 18px 22px;
    min-width: 180px;
">
<div style="font-size: 25px;">📈</div>
<div style="font-weight: 700; color: #17365d; margin-top: 6px;">
Sales Analytics
</div>
<div style="font-size: 13px; color: #66788a; margin-top: 5px;">
Track sales trends and performance
</div>
</div>

<div style="
    background: white;
    border: 1px solid #dbe7f5;
    border-radius: 15px;
    padding: 18px 22px;
    min-width: 180px;
">
<div style="font-size: 25px;">📦</div>
<div style="font-weight: 700; color: #17365d; margin-top: 6px;">
Product Analysis
</div>
<div style="font-size: 13px; color: #66788a; margin-top: 5px;">
Find top and low-performing products
</div>
</div>

<div style="
    background: white;
    border: 1px solid #dbe7f5;
    border-radius: 15px;
    padding: 18px 22px;
    min-width: 180px;
">
<div style="font-size: 25px;">👥</div>
<div style="font-weight: 700; color: #17365d; margin-top: 6px;">
Customer Insights
</div>
<div style="font-size: 13px; color: #66788a; margin-top: 5px;">
Understand customer purchasing patterns
</div>
</div>

<div style="
    background: white;
    border: 1px solid #dbe7f5;
    border-radius: 15px;
    padding: 18px 22px;
    min-width: 180px;
">
<div style="font-size: 25px;">💡</div>
<div style="font-weight: 700; color: #17365d; margin-top: 6px;">
Business Insights
</div>
<div style="font-size: 13px; color: #66788a; margin-top: 5px;">
Discover important business trends
</div>
</div>

</div>

<div style="
    background: #dcecff;
    border-radius: 14px;
    padding: 15px 20px;
    color: #1f4e79;
    font-weight: 600;
    font-size: 15px;
">
📥 Upload your CSV or Excel file using the sidebar to get started.
</div>

</div>
""", unsafe_allow_html=True)

    # =========================================================
    # SUBSCRIPTION STATUS / CTA
    # =========================================================

    is_active_account = bool(st.session_state.get("subscription_active", False))

    if is_active_account:

        current_tier_label = str(st.session_state.get("selected_plan", "Active"))

        st.markdown(f"""
        <div style="
            background-image: linear-gradient(to bottom right, #edfef6, #f2fef6);
            border: 1px solid #c2f9d5;
            border-radius: 1.125rem;
            padding: 1.5rem 1.75rem;
            margin-block-start: 1.25rem;
            text-align: center;
        ">

        <div style="
            font-size: 1.85rem;
            margin-block-end: 0.5rem;
        ">
        ✅
        </div>

        <div style="
            font-size: 1.5rem;
            font-weight: calc(400 + 400);
            color: #11532b;
            line-height: 1.3;
            margin-block-end: 0.5rem;
        ">
        Subscription Active
        </div>

        <div style="
            font-size: 0.95rem;
            color: #4b5563;
            margin-block-end: 0.5rem;
        ">
        Your SalesInsight premium features are unlocked.
        </div>

        <div style="
            font-size: 0.875rem;
            color: #11532b;
            font-weight: 600;
        ">
        Plan: {current_tier_label}
        </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div style="
            background-image: linear-gradient(to bottom right, #f2f7fe, #fcfdff);
            border: 1px solid #dee7f2;
            border-radius: 1.125rem;
            padding: 1.5rem 1.75rem;
            margin-block-start: 1.25rem;
            text-align: center;
        ">

        <div style="
            font-size: 1.85rem;
            margin-block-end: 0.5rem;
        ">
        🔒
        </div>

        <div style="
            font-size: 1.5rem;
            font-weight: calc(400 + 400);
            color: #122c4d;
            line-height: 1.3;
            margin-block-end: 0.5rem;
        ">
        Access Complete SalesInsight Analytics Features
        </div>

        <div style="
            font-size: 0.95rem;
            color: #4f5e6e;
            margin-block-end: 0.75rem;
        ">
        Activate your membership to unlock Customer Analytics, Product Analysis,
        Sales Anomaly Detection, Sales Forecasting, and overall Business Performance.
        </div>

        <div style="
            font-size: 0.875rem;
            color: #617182;
        ">
        Available premium tiers include our 7-Day Trial, Monthly, or Yearly subscriptions.
        </div>

        </div>
        """, unsafe_allow_html=True)

        if st.button(
            label="💳 Browse Subscription Tiers",
            use_container_width=True
        ):
            st.switch_page(
                "pages/9_💳_Subscription.py"
            )

        st.stop()

# =========================================================
# SAFETY CHECK - NO FILE UPLOADED
# =========================================================

is_stream_absent = bool(data_stream is None)

if is_stream_absent:

    st.info(
        body="📥 Please upload your CSV or Excel file from the sidebar to begin."
    )

    st.stop()

# Process data extraction through our ingestion gateway
df = extract_uploaded_bytestream(data_stream)

st.success(f"File '{data_stream.name}' uploaded successfully.")

# Clean column names
df.columns = df.columns.astype(str).str.strip()

# =========================================================
# DATA IMPORT FUNCTION
# =========================================================



# =========================================================
# DATA NORMALISATION & CLEANING
# =========================================================

import re


# ---------------------------------------------------------
# Helper: make column names easier to compare
# ---------------------------------------------------------
def normalise_column_name(name):
    return re.sub(
        r"[^a-z0-9]",
        "",
        str(name).strip().lower()
    )


# ---------------------------------------------------------
# Find a column using possible alternative names
# ---------------------------------------------------------
def find_column(columns, possible_names):

    lookup = {normalise_column_name(column): column
        for column in columns
    }

    for name in possible_names:

        key = normalise_column_name(name)

        if key in lookup:
            return lookup[key]

    return None


# ---------------------------------------------------------
# Possible column names used by sales datasets
# ---------------------------------------------------------

invoice_col = find_column(
    df.columns,
    ["InvoiceNo","Invoice No","Invoice_No","Invoice","Transaction_ID","TransactionID","Transaction","Order_ID","OrderID","Order_No","OrderNumber"]
)

date_col = find_column(
    df.columns,
    ["InvoiceDate","Invoice Date","Invoice_Date","Sale_Date","Sales_Date","SalesDate","Order_Date","OrderDate","Date","Timestamp"]
)

quantity_col = find_column(
    df.columns,
    ["Quantity","Quantity_Sold","Quantity Sold","Qty","Units","Units_Sold","Units Sold"]
)

price_col = find_column(
    df.columns,
    ["UnitPrice","Unit Price","Unit_Price","Price","Selling_Price","Selling Price","Sale_Price","Sale Price"]
)

sales_col = find_column(
    df.columns,
    ["Sales Amount","Sales_Amount","SalesAmount","Sales","Revenue","Total_Sales","Total Sales","Total_Sales_Amount","Total Sales Amount","Amount","Revenue_Amount"]
)

customer_col = find_column(
    df.columns,
    ["CustomerID","Customer ID","Customer_ID","Customer","Customer_Name","Customer Name"]
)

product_col = find_column(
    df.columns,
    ["Description","Product","Product_Name","Product Name","Product_ID","Product ID","Product_ID","Item","Item_Name","Item Name","StockCode","Stock Code"]
)

stock_col = find_column(
    df.columns,
    ["StockCode","Stock Code","Product_ID","Product ID","Product","Item","Item_ID","Item ID"]
)

category_col = find_column(
    df.columns,
    ["Category","Product_Category","Product Category","ProductCategory","Department","Product_Type","Product Type"]
)


# ---------------------------------------------------------
# DATE
# ---------------------------------------------------------

if date_col is None:

    st.error(
        "❌ I could not find a date column in this sales dataset.")

    st.info(
        "Please make sure your dataset contains a date column "
        "such as Date, Sale_Date, Sales_Date, Order_Date or InvoiceDate.")

    st.stop()

else:

    df["InvoiceDate"] = pd.to_datetime(
        df[date_col],
        errors="coerce")


# ---------------------------------------------------------
# SALES AMOUNT
# ---------------------------------------------------------

if sales_col is not None:

    df["Sales Amount"] = pd.to_numeric(
        df[sales_col],
        errors="coerce")

elif quantity_col is not None and price_col is not None:

    quantity_values = pd.to_numeric(
        df[quantity_col],
        errors="coerce")

    price_values = pd.to_numeric(
        df[price_col],
        errors="coerce")

    df["Sales Amount"] = quantity_values * price_values

else:

    st.error("❌ I could not determine the sales amount from this dataset.")

    st.info(
        "Your dataset needs a Sales/Revenue/Amount column "
        "or both Quantity and Unit Price columns.")

    st.stop()


# ---------------------------------------------------------
# QUANTITY
# ---------------------------------------------------------

if quantity_col is not None:

    df["Quantity"] = pd.to_numeric(
        df[quantity_col],
        errors="coerce")

else:

    # If quantity is not provided, treat each sales record as 1 unit.
    df["Quantity"] = 1

    st.warning(
        "⚠️ No quantity column was found. "
        "Each sales record has been treated as 1 unit.")


# ---------------------------------------------------------
# UNIT PRICE
# ---------------------------------------------------------

if price_col is not None:

    df["UnitPrice"] = pd.to_numeric(
        df[price_col],
        errors="coerce")

else:

    # Calculate unit price when possible
    df["UnitPrice"] = (
        df["Sales Amount"] /
        df["Quantity"].replace(0, pd.NA))


# ---------------------------------------------------------
# TRANSACTION / INVOICE NUMBER
# ---------------------------------------------------------

if invoice_col is not None:

    df["InvoiceNo"] = df[invoice_col].astype(str)

else:

    # No transaction ID available.
    # Use one ID per row as a fallback.
    df["InvoiceNo"] = range(1, len(df) + 1)

    st.warning(
        "⚠️ No transaction/order ID was found. "
        "Each sales row has been treated as one transaction.")


# ---------------------------------------------------------
# CUSTOMER ID
# ---------------------------------------------------------

if customer_col is not None:

    df["CustomerID"] = df[customer_col].astype(str)

else:

    # Keep missing customer information as unknown.
    df["CustomerID"] = pd.NA


# ---------------------------------------------------------
# PRODUCT / DESCRIPTION
# ---------------------------------------------------------

if product_col is not None:

    df["Description"] = df[product_col].astype(str)

else:

    # If no product name exists, use the row number.
    df["Description"] = [f"Product {i}"for i in range(1, len(df) + 1)]


# ---------------------------------------------------------
# STOCK CODE / PRODUCT ID
# ---------------------------------------------------------

if stock_col is not None:

    df["StockCode"] = df[stock_col].astype(str)

else:

    df["StockCode"] = df["Description"]


# ---------------------------------------------------------
# CATEGORY
# ---------------------------------------------------------

if category_col is not None:

    df["Category"] = df[category_col].astype(str)

else:

    # Category will be created by the category section
    # later in the application.
    df["Category"] = "Other"

# ---------------------------------------------------------
# COUNTRY / REGION
# ---------------------------------------------------------

country_col = find_column(
    df.columns,
    ["Country","Country_Name","Country Name","Region","State","Location","Market"])

if country_col is not None:

    df["Country"] = df[country_col].astype(str)

else:

    df["Country"] = "Unknown"


# ---------------------------------------------------------
# CLEAN NUMERIC VALUES
# ---------------------------------------------------------

df["Sales Amount"] = pd.to_numeric(
    df["Sales Amount"],
    errors="coerce")

df["Quantity"] = pd.to_numeric(
    df["Quantity"],
    errors="coerce")

df["UnitPrice"] = pd.to_numeric(
    df["UnitPrice"],
    errors="coerce")


# ---------------------------------------------------------
# REMOVE INVALID SALES RECORDS
# ---------------------------------------------------------

df = df[
    df["InvoiceDate"].notna()
    & df["Sales Amount"].notna()
].copy()


# ---------------------------------------------------------
# REMOVE NEGATIVE / ZERO SALES
# ---------------------------------------------------------

df = df[
    df["Sales Amount"] > 0
].copy()


# ---------------------------------------------------------
# SHOW DETECTED DATA
# ---------------------------------------------------------

st.success(
    f"✅ Dataset processed successfully: {len(df):,} sales records")


with st.expander("🔍 View detected dataset columns"):

    detected_columns = pd.DataFrame(
        {"SalesInsight Field": ["Transaction ID","Date","Sales Amount","Quantity","Unit Price","Customer","Product","Category"],
        
        "Detected Column": [invoice_col if invoice_col else "Generated automatically",
        date_col,
        sales_col if sales_col else "Calculated from Quantity × Unit Price",
        quantity_col if quantity_col else "Generated as 1",
        price_col if price_col else "Calculated",
        customer_col if customer_col else "Not available",
        product_col if product_col else "Generated",
        category_col if category_col else "Created as Other"]
        })

    st.dataframe(
        detected_columns,
        use_container_width=True,
        hide_index=True)


# ---------------------------------------------------------
# MAKE CLEANED DATA AVAILABLE TO OTHER PAGES
# ---------------------------------------------------------

st.session_state["sales_df"] = df

# =========================================================
# CATEGORY CREATION
# =========================================================

def create_category(description):

    if pd.isna(description):
        return "Other"

    text = str(description).upper()

    if any(word in text for word in [
        "LIGHT", "LAMP", "CANDLE", "HEART",
        "HOLDER", "DECOR", "FRAME", "MIRROR",
        "CLOCK", "SIGN", "ORNAMENT"
    ]):
        return "Home & Decor"

    elif any(word in text for word in [
        "BAG", "PURSE", "HANDBAG", "WALLET",
        "SCARF", "HAT", "SHOES"
    ]):
        return "Fashion & Accessories"

    elif any(word in text for word in [
        "TOY", "DOLL", "GAME", "PUZZLE",
        "CHILDREN", "KIDS"
    ]):
        return "Toys & Games"

    elif any(word in text for word in [
        "NOTEBOOK", "PAPER", "PEN", "PENCIL",
        "CARD", "BOOK", "STATIONERY"
    ]):
        return "Stationery"

    elif any(word in text for word in [
        "CAKE", "CHOCOLATE", "SWEET", "TEA",
        "COFFEE", "FOOD", "JAM", "BISCUIT"
    ]):
        return "Food & Drink"

    elif any(word in text for word in [
        "SOAP", "CREAM", "BATH", "BEAUTY",
        "PERFUME", "COSMETIC"
    ]):
        return "Beauty & Personal Care"

    else:
        return "Other"


df["Category"] = df["Description"].apply(
    create_category)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📊 SalesInsight")

st.sidebar.caption(
    "SME Sales Analytics & Forecasting System")

st.sidebar.divider()

st.sidebar.subheader("🎛️ Dashboard Filters")

# Date range
min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

selected_dates = st.sidebar.date_input(
    "📅 Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date)

# Product filter
product_options = sorted(
    df["Description"]
    .dropna()
    .unique()
    .tolist()
)

selected_product = st.sidebar.selectbox(
    "📦 Product",
    ["All Products"] + product_options)

# Category filter
category_options = sorted(
    df["Category"].unique().tolist())

selected_category = st.sidebar.selectbox(
    "🏷️ Category",
    ["All Categories"] + category_options)

# =========================================================
# APPLY PRODUCT & CATEGORY FILTERS
# =========================================================

filtered_df = df.copy()

if selected_product != "All Products":

    filtered_df = filtered_df[
        filtered_df["Description"] == selected_product
    ]

if selected_category != "All Categories":

    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

# =========================================================
# APPLY DATE FILTER
# =========================================================

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])

    end_date = (
        pd.Timestamp(selected_dates[1])
        + pd.Timedelta(days=1))

    filtered_df = filtered_df[
        (filtered_df["InvoiceDate"] >= start_date)
        & (filtered_df["InvoiceDate"] < end_date)
    ]

else:

    start_date = pd.Timestamp(min_date)

    end_date = (
        pd.Timestamp(max_date)
        + pd.Timedelta(days=1)
    )

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div style="background: linear-gradient(135deg, #eaf3ff, #f8fbff); border-radius: 20px; padding: 35px; margin-bottom: 25px; border: 1px solid #dbe7f5;">

<div style="display: inline-block; background: #dcecff; color: #1f4e79; padding: 7px 15px; border-radius: 20px; font-size: 14px; font-weight: 600; margin-bottom: 15px;">
🏠 HOME
</div>

<div style="font-size: 38px; font-weight: 800; color: #17365d; margin-bottom: 8px;">
📊 SalesInsight
</div>

<div style="font-size: 19px; color: #52657a; margin-bottom: 15px;">
SME Sales Analytics & Forecasting Dashboard
</div>

<div style="font-size: 16px; color: #52657a; margin-bottom: 20px;">
Analyse sales performance, products, customers and market trends from your uploaded sales data.
</div>

<div style="display: flex; flex-wrap: wrap; gap: 10px;">

<span style="background: white; border: 1px solid #dbe7f5; padding: 8px 14px; border-radius: 12px; color: #36516d;">
📈 Sales Trends
</span>

<span style="background: white; border: 1px solid #dbe7f5; padding: 8px 14px; border-radius: 12px; color: #36516d;">
📦 Product Performance
</span>

<span style="background: white; border: 1px solid #dbe7f5; padding: 8px 14px; border-radius: 12px; color: #36516d;">
👥 Customer Analytics
</span>

<span style="background: white; border: 1px solid #dbe7f5; padding: 8px 14px; border-radius: 12px; color: #36516d;">
🌍 Market Analysis
</span>

<span style="background: white; border: 1px solid #dbe7f5; padding: 8px 14px; border-radius: 12px; color: #36516d;">
💡 Business Insights
</span>

</div>

</div>
""", unsafe_allow_html=True)

st.divider()

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_df["Sales Amount"].sum()

transactions = filtered_df["InvoiceNo"].nunique()

customers = filtered_df["CustomerID"].nunique()

products = filtered_df["StockCode"].nunique()

units_sold = filtered_df["Quantity"].sum()

if transactions > 0:
    average_order_value = total_sales / transactions
else:
    average_order_value = 0

# =========================================================
# KPI CARDS
# =========================================================

st.markdown(
    '<div class="section-title">📌 Business Overview</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.0f}")

with k2:
    st.metric(
        "🧾 Transactions",
        f"{transactions:,}")

with k3:
    st.metric(
        "👥 Customers",
        f"{customers:,}")

with k4:
    st.metric(
        "📦 Products",
        f"{products:,}")

with k5:
    st.metric(
        "🛒 Units Sold",
        f"{units_sold:,.0f}")

with k6:
    st.metric(
        "💳 Avg Order Value",
        f"${average_order_value:,.0f}")

# =========================================================
# SALES TREND
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">📈 Sales Performance</div>',
    unsafe_allow_html=True)

monthly_sales = (
    filtered_df
    .groupby(
        filtered_df["InvoiceDate"].dt.to_period("M")
    )["Sales Amount"]
    .sum()
    .reset_index()
)

monthly_sales["InvoiceDate"] = (
    monthly_sales["InvoiceDate"].dt.to_timestamp()
)

fig_trend = px.line(
    monthly_sales,
    x="InvoiceDate",
    y="Sales Amount",
    markers=True)

fig_trend.update_layout(
    height=430,
    xaxis_title="Month",
    yaxis_title="Sales Amount (ADU)",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=20, b=20))

st.plotly_chart(
    fig_trend,
    use_container_width=True)

# =========================================================
# PRODUCT PERFORMANCE
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">🏆 Product Performance</div>',
    unsafe_allow_html=True)

product_sales = (
    filtered_df
    .groupby("Description")["Sales Amount"]
    .sum()
    .sort_values(ascending=False))

product_sales = product_sales.dropna()

p1, p2 = st.columns(2)

# TOP PRODUCTS
with p1:

    st.subheader("🏆 Top 10 Products")

    top_products = (
        product_sales
        .head(10)
        .sort_values(ascending=True)
        .reset_index())

    fig_top = px.bar(
        top_products,
        x="Sales Amount",
        y="Description",
        orientation="h",
        text="Sales Amount")

    fig_top.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside")

    fig_top.update_layout(
        height=500,
        xaxis_title="Sales Amount (AUD)",
        yaxis_title="",
        margin=dict(l=10, r=100, t=20, b=20))

    st.plotly_chart(
        fig_top,
        use_container_width=True)

# LOW PRODUCTS
with p2:

    st.subheader("📉 Low Performing Products")

    low_products = (
        product_sales
        .tail(10)
        .sort_values(ascending=True)
        .reset_index())

    fig_low = px.bar(
        low_products,
        x="Sales Amount",
        y="Description",
        orientation="h",
        text="Sales Amount")

    fig_low.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside")

    fig_low.update_layout(
        height=500,
        xaxis_title="Sales Amount (AUD)",
        yaxis_title="",
        margin=dict(l=10, r=100, t=20, b=20))

    st.plotly_chart(
        fig_low,
        use_container_width=True)

# =========================================================
# CATEGORY & COUNTRY ANALYTICS
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">🌍 Market Analysis</div>',
    unsafe_allow_html=True)

m1, m2 = st.columns(2)

# CATEGORY
with m1:

    st.subheader("🏷️ Sales by Category")

    category_sales = (
        filtered_df
        .groupby("Category")["Sales Amount"]
        .sum()
        .sort_values(ascending=True)
        .reset_index())

    fig_category = px.bar(
        category_sales,
        x="Sales Amount",
        y="Category",
        orientation="h",
        text="Sales Amount")

    fig_category.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside")

    fig_category.update_layout(
        height=450,
        xaxis_title="Sales Amount (AUD)",
        yaxis_title="")

    st.plotly_chart(
        fig_category,
        use_container_width=True)

# COUNTRY
with m2:

    st.subheader("🌍 Top Countries by Sales")

    country_sales = (
        filtered_df
        .groupby("Country")["Sales Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values(ascending=True)
        .reset_index())

    fig_country = px.bar(
        country_sales,
        x="Sales Amount",
        y="Country",
        orientation="h",
        text="Sales Amount")

    fig_country.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside")

    fig_country.update_layout(
        height=450,
        xaxis_title="Sales Amount (AUD)",
        yaxis_title="")

    st.plotly_chart(
        fig_country,
        use_container_width=True)

# =========================================================
# CUSTOMER ANALYTICS
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">👥 Customer Analytics</div>',
    unsafe_allow_html=True)

customer_df = filtered_df.dropna(
    subset=["CustomerID"]).copy()

customer_df["CustomerID"] = (
    customer_df["CustomerID"]
    .astype(str)
    .str.replace(r"\.0$", "", regex=True))

customer_sales = (
    customer_df
    .groupby("CustomerID")["Sales Amount"]
    .sum()
    .sort_values(ascending=False))

customer_transactions = (
    customer_df
    .groupby("CustomerID")["InvoiceNo"]
    .nunique()
    .sort_values(ascending=False))

c1, c2 = st.columns(2)

with c1:

    st.subheader("💰 Highest Value Customers")

    top_customers = (
        customer_sales
        .head(10)
        .sort_values(ascending=True)
        .reset_index())

    top_customers["Customer"] = (
        "Customer "
        + top_customers["CustomerID"])

    fig_customers = px.bar(
        top_customers,
        x="Sales Amount",
        y="Customer",
        orientation="h",
        text="Sales Amount")

    fig_customers.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside")

    fig_customers.update_layout(
        height=450,
        xaxis_title="Sales Amount (AUD)",
        yaxis_title="",
        margin=dict(l=10, r=100, t=20, b=20))

    st.plotly_chart(
        fig_customers,
        use_container_width=True)

with c2:

    st.subheader("🛒 Most Frequent Customers")

    frequent_customers = (
        customer_transactions
        .head(10)
        .sort_values(ascending=True)
        .reset_index())

    frequent_customers["Customer"] = (
        "Customer "
        + frequent_customers["CustomerID"])

    fig_frequency = px.bar(
        frequent_customers,
        x="InvoiceNo",
        y="Customer",
        orientation="h",
        text="InvoiceNo")

    fig_frequency.update_traces(
        texttemplate="%{text} orders",
        textposition="outside")

    fig_frequency.update_layout(
        height=450,
        xaxis_title="Number of Transactions",
        yaxis_title="",
        margin=dict(l=10, r=100, t=20, b=20))

    st.plotly_chart(
        fig_frequency,
        use_container_width=True)

# =========================================================
# AUTOMATIC BUSINESS INSIGHTS
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">💡 Business Insights</div>',
    unsafe_allow_html=True)

insight_col1, insight_col2 = st.columns(2)

# Top product
if len(product_sales) > 0:

    best_product = product_sales.idxmax()
    best_product_sales = product_sales.max()

    top_product_text = (
        f"🏆 **Top Product:** {best_product} "
        f"generated ${best_product_sales:,.0f} in sales.")

else:

    top_product_text = "No product data available."

# Top country
country_sales_all = (
    filtered_df
    .groupby("Country")["Sales Amount"]
    .sum())

if len(country_sales_all) > 0:

    best_country = country_sales_all.idxmax()
    best_country_sales = country_sales_all.max()

    country_text = (
        f"🌍 **Top Market:** {best_country} "
        f"generated ${best_country_sales:,.0f} in sales.")

else:

    country_text = "No country data available."

# Best month
if len(monthly_sales) > 0:

    best_month_row = monthly_sales.loc[
        monthly_sales["Sales Amount"].idxmax()]

    best_month = best_month_row["InvoiceDate"].strftime(
        "%B %Y")

    best_month_sales = best_month_row["Sales Amount"]

    month_text = (
        f"📅 **Best Sales Month:** {best_month} "
        f"with ${best_month_sales:,.0f} in sales.")

else:

    month_text = "No monthly sales data available."

# Customer insight
if len(customer_sales) > 0:

    highest_customer = customer_sales.idxmax()
    highest_customer_sales = customer_sales.max()

    customer_text = (
        f"👤 **Highest Value Customer:** Customer "
        f"{highest_customer} generated "
        f"${highest_customer_sales:,.0f} in sales.")

else:

    customer_text = "No customer data available."

with insight_col1:

    st.markdown(
        f"""
        <div class="insight-box">
        {top_product_text}<br><br>
        {month_text}
        </div>
        """,
        unsafe_allow_html=True)

with insight_col2:

    st.markdown(
        f"""
        <div class="insight-box">
        {country_text}<br><br>
        {customer_text}
        </div>
        """,
        unsafe_allow_html=True)

# =========================================================
# DATA INFORMATION
# =========================================================

st.divider()

with st.expander("📋 Dataset Information"):

    info1, info2, info3, info4 = st.columns(4)

    with info1:
        st.write("**Records**")
        st.write(f"{len(filtered_df):,}")

    with info2:
        st.write("**Countries**")
        st.write(f"{filtered_df['Country'].nunique():,}")

    with info3:
        st.write("**Date Start**")
        st.write(
            filtered_df["InvoiceDate"]
            .min()
            .strftime("%d %b %Y"))

    with info4:
        st.write("**Date End**")
        st.write(
            filtered_df["InvoiceDate"]
            .max()
            .strftime("%d %b %Y"))