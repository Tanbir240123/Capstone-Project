import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Analysis",
    page_icon="👥",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CUSTOMER ANALYSIS THEME
# --------------------------------------------------

st.markdown("""
<style>

/* =====================================================
   MAIN PAGE
   ===================================================== */

.stApp {

    background:
        radial-gradient(
            circle at top right,
            rgba(16,185,129,0.08),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #f8fffc 0%,
            #f0fdf9 50%,
            #ecfdf5 100%
        );
}


.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

[data-testid="stSidebar"] {

    background:
        radial-gradient(
            circle at top right,
            rgba(52,211,153,0.16),
            transparent 32%
        ),
        linear-gradient(
            180deg,
            #102a25 0%,
            #123c34 50%,
            #071c18 100%
        );
}


/* Sidebar general text */

[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}


/* Sidebar headings */

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {

    color: #d1fae5 !important;
}


/* Sidebar divider */

[data-testid="stSidebar"] hr {

    border-color:
        rgba(167,243,208,0.18) !important;
}


/* Sidebar labels */

[data-testid="stSidebar"] label {

    color: #a7f3d0 !important;

    font-weight:
        650;
}


/* =====================================================
   DATE INPUT FIX
   ===================================================== */

[data-testid="stSidebar"] .stDateInput,
[data-testid="stSidebar"] .stDateInput * {

    color:
        #334155 !important;
}


[data-testid="stSidebar"] .stDateInput
[data-baseweb="input"] {

    background-color:
        #ffffff !important;

    border-radius:
        10px !important;
}


[data-testid="stSidebar"] .stDateInput input {

    color:
        #334155 !important;

    background-color:
        #ffffff !important;

    -webkit-text-fill-color:
        #334155 !important;
}


[data-testid="stSidebar"] .stDateInput
[data-baseweb="input"] input {

    color:
        #334155 !important;

    -webkit-text-fill-color:
        #334155 !important;
}


/* Calendar icon */

[data-testid="stSidebar"] .stDateInput svg {

    color:
        #047857 !important;

    fill:
        #047857 !important;
}


/* =====================================================
   MAIN HEADINGS
   ===================================================== */

h1,
h2,
h3 {

    color:
        #064e3b;
}


/* =====================================================
   METRIC CARDS
   ===================================================== */

div[data-testid="stMetric"] {

    background:
        rgba(255,255,255,0.92);

    border:
        1px solid rgba(16,185,129,0.20);

    border-radius:
        18px;

    padding:
        20px 18px;

    min-height:
        120px;

    box-shadow:
        0 8px 24px rgba(6,78,59,0.07);

    transition:
        transform 0.30s ease,
        box-shadow 0.30s ease,
        border-color 0.30s ease;
}


/* Metric hover */

div[data-testid="stMetric"]:hover {

    transform:
        translateY(-6px);

    box-shadow:
        0 16px 32px rgba(5,150,105,0.15);

    border-color:
        rgba(16,185,129,0.45);
}


/* Metric label */

div[data-testid="stMetricLabel"] {

    color:
        #047857 !important;

    font-weight:
        650;
}


/* Metric value */

div[data-testid="stMetricValue"] {

    color:
        #064e3b !important;

    font-weight:
        850;
}


/* =====================================================
   PLOTLY CHART CONTAINERS
   ===================================================== */

div[data-testid="stPlotlyChart"] {

    background:
        rgba(255,255,255,0.80);

    border-radius:
        20px;

    padding:
        10px;

    box-shadow:
        0 8px 24px rgba(6,78,59,0.06);

    transition:
        transform 0.30s ease,
        box-shadow 0.30s ease;
}


/* Chart hover */

div[data-testid="stPlotlyChart"]:hover {

    transform:
        translateY(-3px);

    box-shadow:
        0 15px 32px rgba(5,150,105,0.12);
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
        0 7px 22px rgba(6,78,59,0.07);
}


/* =====================================================
   INFO / WARNING BOXES
   ===================================================== */

div[data-testid="stAlert"] {

    border-radius:
        14px;
}


/* =====================================================
   DIVIDERS
   ===================================================== */

hr {

    border-color:
        rgba(5,150,105,0.15);
}


/* =====================================================
   SMOOTH ANIMATION
   ===================================================== */

@keyframes customerFadeIn {

    from {

        opacity:
            0;

        transform:
            translateY(12px);
    }

    to {

        opacity:
            1;

        transform:
            translateY(0);
    }
}


h1,
h2,
h3 {

    animation:
        customerFadeIn 0.55s ease-out;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD CLEANED DATA FROM HOME PAGE
# =========================================================

if "sales_df" not in st.session_state:
    st.warning(
        "⚠️ Please upload a sales dataset from the Home page first."
    )
    st.stop()

df = st.session_state["sales_df"].copy()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("👥 Customer Analysis")

st.caption(
    "Understand customer value, purchasing frequency and "
    "customer purchasing patterns."
)

st.divider()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("🔎 Customer Filters")

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
# CUSTOMER DATA
# --------------------------------------------------

customer_df = filtered_df.dropna(
    subset=["CustomerID"]
).copy()


customer_summary = (
    customer_df
    .groupby("CustomerID")
    .agg(
        Total_Sales=("Sales Amount", "sum"),
        Transactions=("InvoiceNo", "nunique"),
        Units=("Quantity", "sum"),
        First_Purchase=("InvoiceDate", "min"),
        Last_Purchase=("InvoiceDate", "max")
    )
    .reset_index()
)


customer_summary["Average_Order_Value"] = (
    customer_summary["Total_Sales"]
    /
    customer_summary["Transactions"].replace(0, 1)
)


# --------------------------------------------------
# KPI VALUES
# --------------------------------------------------

total_customers = len(
    customer_summary
)


total_customer_sales = (
    customer_summary["Total_Sales"].sum()
)


average_customer_value = (

    customer_summary["Total_Sales"].mean()

    if total_customers > 0

    else 0
)


repeat_customers = (
    customer_summary["Transactions"] > 1
).sum()


repeat_percentage = (

    repeat_customers
    / total_customers
    * 100

    if total_customers > 0

    else 0
)


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Customers",
        f"{total_customers:,}"
    )


with c2:

    st.metric(
        "Customer Sales",
        f"${total_customer_sales:,.0f}"
    )


with c3:

    st.metric(
        "Avg Customer Value",
        f"${average_customer_value:,.0f}"
    )


with c4:

    st.metric(
        "Repeat Customers",
        f"{repeat_percentage:.1f}%"
    )


st.divider()


# --------------------------------------------------
# TOP CUSTOMERS
# --------------------------------------------------

st.subheader(
    "🏆 Highest-Value Customers"
)


top_customers = (
    customer_summary
    .sort_values(
        "Total_Sales",
        ascending=False
    )
    .head(10)
)


display_top = top_customers.copy()


display_top.insert(
    0,
    "Rank",
    range(
        1,
        len(display_top) + 1
    )
)


display_top["Customer"] = (
    "Customer "
    +
    display_top["CustomerID"]
    .astype(int)
    .astype(str)
)


fig_top = px.bar(
    display_top.sort_values(
        "Total_Sales"
    ),
    x="Total_Sales",
    y="Customer",
    orientation="h",
    text_auto=".2s",
    title="Top 10 Customers by Sales"
)


fig_top.update_layout(
    template="plotly_white",
    xaxis_title="Total Sales ($)",
    yaxis_title="Customer",
    height=500
)


st.plotly_chart(
    fig_top,
    use_container_width=True
)


# --------------------------------------------------
# TOP CUSTOMER TABLE
# --------------------------------------------------

st.subheader(
    "📋 Customer Value Table"
)


top_table = display_top[
    [
        "Rank",
        "Customer",
        "Total_Sales",
        "Transactions",
        "Units",
        "Average_Order_Value",
        "Last_Purchase"
    ]
].copy()


top_table.columns = [
    "Rank",
    "Customer",
    "Total Sales",
    "Transactions",
    "Units",
    "Avg Order Value",
    "Last Purchase"
]


top_table["Total Sales"] = (
    top_table["Total Sales"]
    .apply(
        lambda x:
        f"${x:,.2f}"
    )
)


top_table["Avg Order Value"] = (
    top_table["Avg Order Value"]
    .apply(
        lambda x:
        f"${x:,.2f}"
    )
)


top_table["Last Purchase"] = (
    pd.to_datetime(
        top_table["Last Purchase"]
    )
    .dt.strftime(
        "%d %b %Y"
    )
)


st.dataframe(
    top_table,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# MOST FREQUENT CUSTOMERS
# --------------------------------------------------

st.subheader(
    "🔁 Most Frequent Customers"
)


frequent_customers = (
    customer_summary
    .sort_values(
        "Transactions",
        ascending=False
    )
    .head(10)
    .copy()
)


frequent_customers["Customer"] = (
    "Customer "
    +
    frequent_customers["CustomerID"]
    .astype(int)
    .astype(str)
)


fig_frequency = px.bar(
    frequent_customers.sort_values(
        "Transactions"
    ),
    x="Transactions",
    y="Customer",
    orientation="h",
    text_auto=True,
    title="Top 10 Customers by Number of Transactions"
)


fig_frequency.update_layout(
    template="plotly_white",
    xaxis_title="Number of Transactions",
    yaxis_title="Customer",
    height=500
)


st.plotly_chart(
    fig_frequency,
    use_container_width=True
)


# --------------------------------------------------
# CUSTOMER PURCHASE FREQUENCY
# --------------------------------------------------

st.subheader(
    "📊 Customer Purchase Frequency"
)


frequency_distribution = (
    customer_summary["Transactions"]
    .value_counts()
    .sort_index()
    .head(15)
    .reset_index()
)


frequency_distribution.columns = [
    "Transactions",
    "Number of Customers"
]


fig_frequency_dist = px.bar(
    frequency_distribution,
    x="Transactions",
    y="Number of Customers",
    text_auto=True,
    title="Number of Customers by Purchase Frequency"
)


fig_frequency_dist.update_layout(
    template="plotly_white",
    xaxis_title="Number of Transactions",
    yaxis_title="Number of Customers",
    height=450
)


st.plotly_chart(
    fig_frequency_dist,
    use_container_width=True
)


# --------------------------------------------------
# CUSTOMER VALUE DISTRIBUTION
# --------------------------------------------------

st.subheader(
    "💰 Customer Value Distribution"
)


fig_value = px.histogram(
    customer_summary,
    x="Total_Sales",
    nbins=30,
    title="Distribution of Customer Sales Value"
)


fig_value.update_layout(
    template="plotly_white",
    xaxis_title="Customer Sales ($)",
    yaxis_title="Number of Customers",
    height=450
)


st.plotly_chart(
    fig_value,
    use_container_width=True
)


# --------------------------------------------------
# CUSTOMER SEGMENTS
# --------------------------------------------------

st.subheader(
    "🎯 Customer Segments"
)


def segment_customer(row):

    sales = row["Total_Sales"]

    transactions = row["Transactions"]


    if sales >= customer_summary[
        "Total_Sales"
    ].quantile(0.75):

        return "High Value"


    elif transactions >= customer_summary[
        "Transactions"
    ].quantile(0.75):

        return "Frequent"


    elif sales <= customer_summary[
        "Total_Sales"
    ].quantile(0.25):

        return "Low Value"


    else:

        return "Regular"


customer_summary["Segment"] = (
    customer_summary
    .apply(
        segment_customer,
        axis=1
    )
)


segment_counts = (
    customer_summary["Segment"]
    .value_counts()
    .reset_index()
)


segment_counts.columns = [
    "Segment",
    "Customers"
]


fig_segments = px.pie(
    segment_counts,
    names="Segment",
    values="Customers",
    hole=0.45,
    title="Customer Segmentation"
)


fig_segments.update_layout(
    template="plotly_white",
    height=450
)


st.plotly_chart(
    fig_segments,
    use_container_width=True
)


# --------------------------------------------------
# CUSTOMER SUMMARY
# --------------------------------------------------

st.subheader(
    "📋 Customer Analytics Summary"
)


summary_table = pd.DataFrame({

    "Metric": [

        "Total Customers",

        "Repeat Customers",

        "Repeat Customer %",

        "Total Customer Sales",

        "Average Customer Value"
    ],

    "Value": [

        f"{total_customers:,}",

        f"{repeat_customers:,}",

        f"{repeat_percentage:.1f}%",

        f"${total_customer_sales:,.2f}",

        f"${average_customer_value:,.2f}"
    ]
})


st.dataframe(
    summary_table,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.subheader(
    "💡 Customer Insights"
)


if len(top_customers) > 0:

    top_customer = top_customers.iloc[0]

    st.info(
        f"🏆 Customer "
        f"{int(top_customer['CustomerID'])} "
        f"generated the highest sales of approximately "
        f"${top_customer['Total_Sales']:,.0f}."
    )


st.info(
    f"🔁 Approximately "
    f"{repeat_percentage:.1f}% "
    f"of customers made more than one transaction."
)


if len(frequent_customers) > 0:

    frequent_customer = (
        frequent_customers.iloc[0]
    )

    st.info(
        f"🔄 Customer "
        f"{int(frequent_customer['CustomerID'])} "
        f"had the highest number of transactions: "
        f"{int(frequent_customer['Transactions'])}."
    )


# --------------------------------------------------
# METHODOLOGY
# --------------------------------------------------

with st.expander(
    "ℹ️ About Customer Analysis"
):

    st.write(
        """
        Customer analysis uses:

        • Total sales per customer
        • Number of transactions
        • Units purchased
        • Average order value
        • First and last purchase dates
        • Purchase frequency

        Customer segments are created using sales value and
        transaction frequency. They are analytical segments
        created specifically for this dashboard.
        """
    )