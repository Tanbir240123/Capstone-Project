import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Sales Analysis",
    page_icon="📈",
    layout="wide"
)


# =========================================================
# CUSTOM THEME
# =========================================================

st.markdown("""
<style>

/* =====================================================
   GLOBAL
   ===================================================== */

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(225,29,72,0.18),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #f8fafc 0%,
            #f1f5f9 50%,
            #eef2ff 100%
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
            rgba(225,29,72,0.18),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #3b1023 0%,
            #4c1028 55%,
            #240b18 100%
        );
}

[data-testid="stSidebar"] * {
    color: #94a3b8 !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.10) !important;
}


.sidebar-title {
    font-size: 27px;
    font-weight: 850;
    color: #ffffff !important;
    margin-bottom: 4px;
}

.sidebar-subtitle {
    color: #fda4af !important;
    font-size: 13px;
    margin-bottom: 25px;
}


.sidebar-card {

    background:
        rgba(255,255,255,0.045);

    border:
        1px solid rgba(255,255,255,0.08);

    border-radius:
        14px;

    padding:
        15px;

    margin-bottom:
        12px;

    transition:
        transform 0.25s ease,
        background 0.25s ease,
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}


.sidebar-card:hover {

    transform:
        translateX(5px);

    background:
    rgba(225,29,72,0.14);

border-color:
    rgba(244,63,94,0.40);
    
    box-shadow:
        0 8px 20px rgba(0,0,0,0.18);
}


.sidebar-card-title {

    color:
        #60a5fa !important;

    font-size:
        13px;

    font-weight:
        750;
}


.sidebar-card-text {

    color:
        #cbd5e1 !important;

    font-size:
        13px;

    margin-top:
        5px;
}


/* =====================================================
   HEADER
   ===================================================== */

.analysis-title {

    font-size:
        40px;

    font-weight:
        850;

    color:
        #0f172a;

    letter-spacing:
        -0.8px;

    margin-bottom:
        4px;

    animation:
        fadeInUp 0.55s ease;
}


.analysis-subtitle {

    font-size:
        16px;

    color:
        #64748b;

    margin-bottom:
        20px;

    animation:
        fadeInUp 0.7s ease;
}


/* =====================================================
   KPI CARDS
   ===================================================== */

div[data-testid="stMetric"] {

    background:
        rgba(255,255,255,0.90);

    border:
        1px solid rgba(148,163,184,0.20);

    border-radius:
        18px;

    padding:
        20px 18px;

    min-height:
        120px;

    box-shadow:
        0 8px 24px rgba(15,23,42,0.07);

    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease;
}


div[data-testid="stMetric"]:hover {

    transform:
        translateY(-6px);

    box-shadow:
        0 16px 34px rgba(15,23,42,0.13);

    border-color:
        rgba(59,130,246,0.35);
}


div[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 650;
}


div[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-weight: 850;
}


/* =====================================================
   CHARTS
   ===================================================== */

div[data-testid="stPlotlyChart"] {

    background:
        rgba(255,255,255,0.80);

    border-radius:
        20px;

    padding:
        10px;

    box-shadow:
        0 8px 24px rgba(15,23,42,0.06);

    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease;
}


div[data-testid="stPlotlyChart"]:hover {

    transform:
        translateY(-3px);

    box-shadow:
        0 15px 32px rgba(15,23,42,0.10);
}


/* =====================================================
   DATAFRAME
   ===================================================== */

div[data-testid="stDataFrame"] {

    border-radius:
        16px;

    overflow:
        hidden;

    box-shadow:
        0 7px 22px rgba(15,23,42,0.06);
}


/* =====================================================
   INSIGHT BOX
   ===================================================== */

.sales-insight {

    background:
        linear-gradient(
            135deg,
            rgba(59,130,246,0.08),
            rgba(99,102,241,0.08)
        );

    border-left:
        5px solid #3b82f6;

    border-radius:
        14px;

    padding:
        17px 20px;

    margin:
        8px 0;

    color:
        #334155;

    box-shadow:
        0 5px 18px rgba(15,23,42,0.05);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}


.sales-insight:hover {

    transform:
        translateX(4px);

    box-shadow:
        0 10px 24px rgba(59,130,246,0.10);
}


/* =====================================================
   FILTER CARD
   ===================================================== */

.filter-card {

    background:
        rgba(255,255,255,0.75);

    border:
        1px solid rgba(148,163,184,0.20);

    border-radius:
        16px;

    padding:
        16px;

    margin-bottom:
        18px;

    box-shadow:
        0 6px 20px rgba(15,23,42,0.05);
}


/* =====================================================
   DIVIDER
   ===================================================== */

hr {
    border-color:
        rgba(100,116,139,0.15);
}


/* =====================================================
   ANIMATION
   ===================================================== */

@keyframes fadeInUp {

    from {
        opacity: 0;
        transform: translateY(12px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">📊 SalesInsight</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'SME Sales Analytics & Forecasting'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">'
        '📈 CURRENT MODULE'
        '</div>'
        '<div class="sidebar-card-text">'
        'Sales Analysis'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">'
        '💰 SALES OVERVIEW'
        '</div>'
        '<div class="sidebar-card-text">'
        'Revenue, transactions and order performance'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">'
        '📅 SALES TRENDS'
        '</div>'
        '<div class="sidebar-card-text">'
        'Daily and monthly sales patterns'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">'
        '🌍 MARKET ANALYSIS'
        '</div>'
        '<div class="sidebar-card-text">'
        'Country-wise sales contribution'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">'
        '💡 ANALYTICS'
        '</div>'
        '<div class="sidebar-card-text">'
        'Identify sales patterns and business trends.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# LOAD CLEANED DATA FROM HOME PAGE
# =========================================================

if "sales_df" not in st.session_state:

    st.warning(
        "⚠️ Please upload a sales dataset from the Home page first."
    )

    st.stop()

df = st.session_state["sales_df"].copy()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="analysis-title">'
    '📈 Sales Analysis'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="analysis-subtitle">'
    'Analyze revenue trends, transactions and sales performance '
    'across time and markets.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# DATE FILTER
# =========================================================

min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

with st.container():

    st.markdown(
        '<div class="filter-card">',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        start_date = st.date_input(
            "Start Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )

    with col2:

        end_date = st.date_input(
            "End Date",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


filtered_df = df[
    (df["InvoiceDate"].dt.date >= start_date)
    &
    (df["InvoiceDate"].dt.date <= end_date)
].copy()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_df["Sales Amount"].sum()

transactions = filtered_df["InvoiceNo"].nunique()

quantity_sold = filtered_df["Quantity"].sum()

average_transaction = (
    total_sales / transactions
    if transactions > 0
    else 0
)


# =========================================================
# KPI CARDS
# =========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.0f}"
    )

with c2:

    st.metric(
        "🧾 Transactions",
        f"{transactions:,}"
    )

with c3:

    st.metric(
        "📦 Quantity Sold",
        f"{quantity_sold:,.0f}"
    )

with c4:

    st.metric(
        "🛒 Avg Transaction Value",
        f"${average_transaction:,.0f}"
    )


st.divider()


# =========================================================
# MONTHLY SALES
# =========================================================

monthly_sales = (
    filtered_df
    .set_index("InvoiceDate")
    .resample("ME")["Sales Amount"]
    .sum()
)


# =========================================================
# MONTHLY SALES CHART
# =========================================================

st.subheader("📅 Monthly Sales Trend")


fig_monthly = go.Figure()


fig_monthly.add_trace(
    go.Scatter(

        x=monthly_sales.index,

        y=monthly_sales.values,

        mode="lines+markers",

        name="Monthly Sales",

        line=dict(
            color="#3b82f6",
            width=3
        ),

        marker=dict(
            size=7
        ),

        hovertemplate=
            "<b>%{x|%B %Y}</b><br>"
            "Sales: $%{y:,.0f}"
            "<extra></extra>"
    )
)


fig_monthly.update_layout(

    height=480,

    template="plotly_white",

    hovermode="x unified",

    xaxis_title="Month",

    yaxis_title="Sales Amount (AUD)",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(255,255,255,0.35)",

    font={
        "color": "#334155"
    },

    margin={
        "l": 40,
        "r": 30,
        "t": 40,
        "b": 50
    }
)


st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# =========================================================
# DAILY SALES
# =========================================================

st.subheader("📆 Daily Sales Trend")


daily_sales = (
    filtered_df
    .set_index("InvoiceDate")
    .resample("D")["Sales Amount"]
    .sum()
)


fig_daily = go.Figure()


fig_daily.add_trace(
    go.Scatter(

        x=daily_sales.index,

        y=daily_sales.values,

        mode="lines",

        name="Daily Sales",

        line=dict(
            color="#6366f1",
            width=2
        ),

        hovertemplate=
            "<b>%{x|%d %B %Y}</b><br>"
            "Sales: $%{y:,.0f}"
            "<extra></extra>"
    )
)


fig_daily.update_layout(

    height=430,

    template="plotly_white",

    hovermode="x unified",

    xaxis_title="Date",

    yaxis_title="Sales Amount (AUD)",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(255,255,255,0.35)",

    font={
        "color": "#334155"
    }
)


st.plotly_chart(
    fig_daily,
    use_container_width=True
)


# =========================================================
# COUNTRY ANALYSIS
# =========================================================

if "Country" in filtered_df.columns:

    st.subheader("🌍 Sales by Country")

    country_sales = (
        filtered_df
        .groupby("Country")["Sales Amount"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )


    fig_country = go.Figure()


    fig_country.add_trace(
        go.Bar(

            x=country_sales.values,

            y=country_sales.index,

            orientation="h",

            text=[
                f"${x:,.0f}"
                for x in country_sales.values
            ],

            textposition="outside",

            marker=dict(
                color="#3b82f6"
            ),

            hovertemplate=
                "<b>%{y}</b><br>"
                "Sales: $%{x:,.0f}"
                "<extra></extra>"
        )
    )


    fig_country.update_layout(

        height=500,

        template="plotly_white",

        xaxis_title="Sales Amount (AUD)",

        yaxis_title="Country",

        yaxis=dict(
            categoryorder="total ascending"
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(255,255,255,0.35)",

        margin={
            "l": 30,
            "r": 80,
            "t": 30,
            "b": 50
        }
    )


    st.plotly_chart(
        fig_country,
        use_container_width=True
    )


# =========================================================
# MONTHLY SALES TABLE
# =========================================================

st.subheader("📋 Monthly Sales Summary")


monthly_table = monthly_sales.reset_index()

monthly_table.columns = [
    "Month",
    "Sales"
]


monthly_table["Month"] = (
    monthly_table["Month"]
    .dt.strftime("%B %Y")
)


monthly_table["Sales"] = (
    monthly_table["Sales"]
    .map(
        lambda x:
        f"${x:,.0f}"
    )
)


st.dataframe(
    monthly_table,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# SALES INSIGHTS
# =========================================================

st.subheader("💡 Sales Insights")


if len(monthly_sales) >= 2:

    latest_sales = monthly_sales.iloc[-1]

    previous_sales = monthly_sales.iloc[-2]

    if previous_sales != 0:

        monthly_change = (
            (latest_sales - previous_sales)
            / abs(previous_sales)
        ) * 100

    else:

        monthly_change = 0


    if monthly_change > 0:

        st.markdown(
            f"""
            <div class="sales-insight">
            📈 <b>Recent Sales Growth:</b>
            Sales increased by approximately
            <b>{monthly_change:.1f}%</b>
            compared with the previous month.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="sales-insight">
            📉 <b>Recent Sales Change:</b>
            Sales changed by
            <b>{monthly_change:.1f}%</b>
            compared with the previous month.
            </div>
            """,
            unsafe_allow_html=True
        )


if len(monthly_sales) > 0:

    best_month = monthly_sales.idxmax()

    best_month_value = monthly_sales.max()

    st.markdown(
        f"""
        <div class="sales-insight">
        🏆 <b>Highest Sales Month:</b>
        {best_month.strftime("%B %Y")}
        generated approximately
        <b>${best_month_value:,.0f}</b>
        in sales.
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    f"""
    <div class="sales-insight">
    🛒 <b>Average Transaction:</b>
    Each transaction generated approximately
    <b>${average_transaction:,.0f}</b>
    in sales.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div style="text-align:center;'
    'color:#94a3b8;'
    'font-size:12px;'
    'margin-top:25px;">'
    'SalesInsight • Sales Analysis'
    '</div>',
    unsafe_allow_html=True
)