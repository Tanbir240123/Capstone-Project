import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Product Analysis",
    page_icon="🏆",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM PRODUCT ANALYSIS THEME
# --------------------------------------------------

st.markdown("""
<style>

/* =====================================================
   PRODUCT ANALYSIS SIDEBAR
   ===================================================== */

[data-testid="stSidebar"] {

    background:
        radial-gradient(
            circle at top right,
            rgba(192,132,252,0.18),
            transparent 32%
        ),
        linear-gradient(
            180deg,
            #24112F 0%,
            #3B1D4F 55%,
            #160B20 100%
        );
}


/* SIDEBAR TEXT */

[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}
/* =====================================================
   DATE RANGE - READABLE TEXT
   ===================================================== */

[data-testid="stSidebar"] .stDateInput,
[data-testid="stSidebar"] .stDateInput * {
    color: #334155 !important;
}

/* Date input box */
[data-testid="stSidebar"] .stDateInput [data-baseweb="input"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}

/* Actual date text */
[data-testid="stSidebar"] .stDateInput input {
    color: #334155 !important;
    background-color: #ffffff !important;
    -webkit-text-fill-color: #334155 !important;
}

/* Date text / displayed value */
[data-testid="stSidebar"] .stDateInput [data-baseweb="input"] input {
    color: #334155 !important;
    -webkit-text-fill-color: #334155 !important;
}

/* Calendar icon */
[data-testid="stSidebar"] .stDateInput svg {
    color: #475569 !important;
    fill: #475569 !important;
}


/* SIDEBAR DIVIDER */

[data-testid="stSidebar"] hr {
    border-color:
        rgba(216,180,254,0.18) !important;
}


/* SIDEBAR HEADINGS */

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #E9D5FF !important;
}


/* SIDEBAR INPUT LABELS */

[data-testid="stSidebar"] label {
    color: #DDD6FE !important;
    font-weight: 600;
}


/* SIDEBAR INPUTS */

[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] input {
    border-color:
        rgba(192,132,252,0.30) !important;
}


/* SIDEBAR BUTTON HOVER */

[data-testid="stSidebar"] .stButton > button:hover {

    background:
        rgba(124,58,237,0.25) !important;

    border-color:
        #A855F7 !important;
}


/* =====================================================
   MAIN PAGE BACKGROUND
   ===================================================== */

.stApp {

    background:
        radial-gradient(
            circle at top right,
            rgba(192,132,252,0.08),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #FAF7FF 0%,
            #F5F3FF 50%,
            #F3E8FF 100%
        );
}


/* =====================================================
   METRIC CARDS
   ===================================================== */

div[data-testid="stMetric"] {

    background:
        rgba(255,255,255,0.90);

    border:
        1px solid rgba(192,132,252,0.20);

    border-radius:
        18px;

    padding:
        18px;

    min-height:
        115px;

    box-shadow:
        0 8px 24px rgba(59,29,79,0.08);

    transition:
        transform 0.30s ease,
        box-shadow 0.30s ease,
        border-color 0.30s ease;
}


/* METRIC HOVER */

div[data-testid="stMetric"]:hover {

    transform:
        translateY(-5px);

    box-shadow:
        0 15px 30px rgba(124,58,237,0.14);

    border-color:
        rgba(168,85,247,0.40);
}


/* METRIC LABEL */

div[data-testid="stMetricLabel"] {

    color:
        #6B21A8 !important;

    font-weight:
        650;
}


/* METRIC VALUE */

div[data-testid="stMetricValue"] {

    color:
        #3B1D4F !important;

    font-weight:
        800;
}


/* =====================================================
   CHARTS
   ===================================================== */

div[data-testid="stPlotlyChart"] {

    background:
        rgba(255,255,255,0.78);

    border-radius:
        18px;

    padding:
        8px;

    box-shadow:
        0 7px 22px rgba(59,29,79,0.07);

    transition:
        transform 0.30s ease,
        box-shadow 0.30s ease;
}


/* CHART HOVER */

div[data-testid="stPlotlyChart"]:hover {

    transform:
        translateY(-3px);

    box-shadow:
        0 14px 30px rgba(124,58,237,0.12);
}


/* =====================================================
   DATA TABLE
   ===================================================== */

div[data-testid="stDataFrame"] {

    border-radius:
        16px;

    overflow:
        hidden;

    box-shadow:
        0 7px 22px rgba(59,29,79,0.07);
}


/* =====================================================
   HEADINGS
   ===================================================== */

h1,
h2,
h3 {

    color:
        #3B1D4F;
}


/* =====================================================
   DIVIDERS
   ===================================================== */

hr {

    border-color:
        rgba(107,33,168,0.15);
}


/* =====================================================
   SMOOTH PAGE ENTRY
   ===================================================== */

@keyframes productFadeIn {

    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}


h1,
h2,
h3 {

    animation:
        productFadeIn 0.50s ease-out;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    file_path = "data/SalesInsight.xlsx"

    df = pd.read_excel(
        file_path,
        skiprows=[1, 2]
    )

    df.columns = df.columns.astype(str).str.strip()

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    df["Sales Amount"] = pd.to_numeric(
        df["Sales Amount"],
        errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    df["UnitPrice"] = pd.to_numeric(
        df["UnitPrice"],
        errors="coerce"
    )

    df["InvoiceNo"] = pd.to_numeric(
        df["InvoiceNo"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "InvoiceDate",
            "Sales Amount",
            "InvoiceNo"
        ]
    )

    return df


df = load_data()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🏆 Product Analysis")

st.caption(
    "Analyse product sales, quantity sold and product performance."
)

st.divider()


# --------------------------------------------------
# SIDEBAR FILTER
# --------------------------------------------------

st.sidebar.header("🔎 Product Filters")

min_date = df["InvoiceDate"].min().date()

max_date = df["InvoiceDate"].max().date()


date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


if len(date_range) == 2:

    start_date = pd.Timestamp(
        date_range[0]
    )

    end_date = (
        pd.Timestamp(date_range[1])
        + pd.Timedelta(days=1)
    )

    filtered_df = df[
        (df["InvoiceDate"] >= start_date) &
        (df["InvoiceDate"] < end_date)
    ].copy()

else:

    filtered_df = df.copy()


# --------------------------------------------------
# PRODUCT SUMMARY
# --------------------------------------------------

product_summary = (
    filtered_df
    .groupby(
        ["StockCode", "Description"],
        dropna=False
    )
    .agg(
        Sales=("Sales Amount", "sum"),
        Units=("Quantity", "sum"),
        Transactions=("InvoiceNo", "nunique"),
        Average_Price=("UnitPrice", "mean")
    )
    .reset_index()
)


product_summary["Description"] = (
    product_summary["Description"]
    .fillna("Unknown Product")
    .astype(str)
    .str.strip()
)


# --------------------------------------------------
# KPI VALUES
# --------------------------------------------------

total_products = (
    product_summary["StockCode"].nunique()
)


total_units = (
    filtered_df["Quantity"].sum()
)


best_product = product_summary.loc[
    product_summary["Sales"].idxmax()
]


lowest_product = product_summary.loc[
    product_summary["Sales"].idxmin()
]


average_product_sales = (
    product_summary["Sales"].mean()
    if len(product_summary) > 0
    else 0
)


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Products",
        f"{total_products:,}"
    )


with c2:

    st.metric(
        "Units Sold",
        f"{total_units:,.0f}"
    )


with c3:

    st.metric(
        "Top Product Sales",
        f"${best_product['Sales']:,.0f}"
    )


with c4:

    st.metric(
        "Average Product Sales",
        f"${average_product_sales:,.0f}"
    )


st.divider()


# --------------------------------------------------
# TOP 10 PRODUCTS
# --------------------------------------------------

st.subheader(
    "🥇 Top 10 Products by Sales"
)


top_products = (
    product_summary
    .sort_values(
        "Sales",
        ascending=False
    )
    .head(10)
)


fig_top = px.bar(
    top_products.sort_values("Sales"),
    x="Sales",
    y="Description",
    orientation="h",
    text_auto=".2s",
    title="Highest Revenue-Generating Products"
)


fig_top.update_layout(
    template="plotly_white",
    xaxis_title="Sales Amount (AUD)",
    yaxis_title="Product",
    height=500
)


st.plotly_chart(
    fig_top,
    use_container_width=True
)


# --------------------------------------------------
# TOP PRODUCT TABLE
# --------------------------------------------------

st.subheader(
    "📋 Top Product Details"
)


top_table = top_products.copy()


top_table.insert(
    0,
    "Rank",
    range(
        1,
        len(top_table) + 1
    )
)


top_table = top_table[
    [
        "Rank",
        "StockCode",
        "Description",
        "Sales",
        "Units",
        "Transactions",
        "Average_Price"
    ]
]


top_table.columns = [
    "Rank",
    "Product Code",
    "Product",
    "Sales Amount",
    "Units Sold",
    "Transactions",
    "Avg Unit Price"
]


top_table["Sales Amount"] = (
    top_table["Sales Amount"]
    .apply(
        lambda x:
        f"${x:,.2f}"
    )
)


top_table["Avg Unit Price"] = (
    top_table["Avg Unit Price"]
    .apply(
        lambda x:
        f"${x:,.2f}"
    )
)


st.dataframe(
    top_table,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# LOW PERFORMING PRODUCTS
# --------------------------------------------------

st.subheader(
    "📉 Low-Performing Products"
)


positive_products = product_summary[
    product_summary["Sales"] > 0
]


low_products = (
    positive_products
    .sort_values(
        "Sales",
        ascending=True
    )
    .head(10)
)


fig_low = px.bar(
    low_products.sort_values("Sales"),
    x="Sales",
    y="Description",
    orientation="h",
    text_auto=".2s",
    title="Products with the Lowest Positive Sales"
)


fig_low.update_layout(
    template="plotly_white",
    xaxis_title="Sales Amount (AUD)",
    yaxis_title="Product",
    height=500
)


st.plotly_chart(
    fig_low,
    use_container_width=True
)


# --------------------------------------------------
# PRODUCT QUANTITY ANALYSIS
# --------------------------------------------------

st.subheader(
    "📦 Top Products by Units Sold"
)


top_quantity = (
    product_summary
    .sort_values(
        "Units",
        ascending=False
    )
    .head(10)
)


fig_quantity = px.bar(
    top_quantity.sort_values("Units"),
    x="Units",
    y="Description",
    orientation="h",
    text_auto=".2s",
    title="Products with Highest Quantity Sold"
)


fig_quantity.update_layout(
    template="plotly_white",
    xaxis_title="Units Sold",
    yaxis_title="Product",
    height=500
)


st.plotly_chart(
    fig_quantity,
    use_container_width=True
)


# --------------------------------------------------
# PRODUCT PERFORMANCE TABLE
# --------------------------------------------------

st.subheader(
    "📊 Product Performance Overview"
)


performance_table = product_summary.copy()


performance_table = (
    performance_table
    .sort_values(
        "Sales",
        ascending=False
    )
    .head(20)
)


performance_table = performance_table[
    [
        "StockCode",
        "Description",
        "Sales",
        "Units",
        "Transactions",
        "Average_Price"
    ]
]


performance_table.columns = [
    "Product Code",
    "Product",
    "Sales Amount",
    "Units Sold",
    "Transactions",
    "Avg Unit Price"
]


performance_table["Sales Amount"] = (
    performance_table["Sales Amount"]
    .apply(
        lambda x:
        f"${x:,.2f}"
    )
)


performance_table["Avg Unit Price"] = (
    performance_table["Avg Unit Price"]
    .apply(
        lambda x:
        f"${x:,.2f}"
    )
)


st.dataframe(
    performance_table,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.subheader(
    "💡 Product Insights"
)


st.info(
    f"🏆 **Top Product:** "
    f"{best_product['Description']} generated approximately "
    f"${best_product['Sales']:,.0f} in sales."
)


st.info(
    f"📦 **Highest Quantity Product:** "
    f"{top_quantity.iloc[0]['Description']} had "
    f"{top_quantity.iloc[0]['Units']:,.0f} units sold."
)


st.warning(
    f"📉 **Lowest Positive Sales Product:** "
    f"{low_products.iloc[0]['Description']} generated "
    f"${low_products.iloc[0]['Sales']:,.2f}."
)


# --------------------------------------------------
# NOTE
# --------------------------------------------------

with st.expander(
    "ℹ️ About Product Analysis"
):

    st.write(
        """
        Product performance is evaluated using:

        • Total sales revenue
        • Units sold
        • Number of transactions
        • Average unit price

        Low-performing products shown here are products with
        the lowest positive sales values. Returns or negative
        sales are not used for this particular low-performance
        ranking.
        """
    )