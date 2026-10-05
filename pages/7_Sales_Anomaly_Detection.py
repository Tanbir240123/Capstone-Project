import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Sales Anomaly Detection",
    page_icon="🚨",
    layout="wide"
)

# ============================================================
# SUBSCRIPTION ACCESS CONTROL
# ============================================================

is_authorized = bool(st.session_state.get("subscription_active", False))

if not is_authorized:

    st.title("🔒 Sales Anomaly Detection")

    st.warning("Subscription Required")

    st.write(
        "Please choose a SalesInsight subscription plan "
        "to access Sales Anomaly Detection."
    )

    if st.button(
        label="💳 Browse Subscription Tiers",
        use_container_width=True
    ):
        st.switch_page(
            "pages/9_💳_Subscription.py"
        )

    st.stop()

# =========================================================
# SALESINSIGHT MODERN THEME
# =========================================================

st.markdown("""
<style>

/* =====================================================
   MAIN BACKGROUND
   ===================================================== */

.stApp {
    background: linear-gradient(
        135deg,
        #eef4ff 0%,
        #f5f3ff 50%,
        #eef7ff 100%
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
    background: linear-gradient(
        180deg,
        #134e4a 0%,
        #115e59 50%,
        #0f766e 100%
    );
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
}


/* Sidebar title */

.sidebar-title {
    font-size: 25px;
    font-weight: 800;
    color: white !important;
    margin-bottom: 5px;
}


/* Sidebar subtitle */

.sidebar-subtitle {
    color: #c7d2fe !important;
    font-size: 13px;
    margin-bottom: 25px;
}


/* Sidebar cards */

.sidebar-card {
    background: rgba(255,255,255,0.09);

    border: 1px solid rgba(255,255,255,0.14);

    border-radius: 12px;

    padding: 14px;

    margin-bottom: 12px;

    transition:
        transform 0.25s ease,
        background 0.25s ease,
        box-shadow 0.25s ease;
}

.sidebar-card:hover {
    transform: translateX(4px);

    background: rgba(255,255,255,0.15);

    box-shadow:
        0 6px 18px rgba(0,0,0,0.15);
}


.sidebar-card-title {
    color: #c4b5fd !important;
    font-weight: 700;
    font-size: 14px;
}


.sidebar-card-text {
    color: #eef2ff !important;
    font-size: 13px;
    margin-top: 4px;
}


/* Sidebar sliders */

[data-testid="stSidebar"] .stSlider {
    padding-top: 5px;
    padding-bottom: 10px;
}


/* Sidebar divider */

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.16) !important;
}


/* =====================================================
   PAGE HEADER
   ===================================================== */

.anomaly-title {
    font-size: 38px;
    font-weight: 800;

    color: #172554;

    margin-bottom: 5px;

    animation: fadeInUp 0.6s ease;
}


.anomaly-subtitle {
    color: #64748b;

    font-size: 16px;

    margin-bottom: 20px;

    animation: fadeInUp 0.7s ease;
}


/* =====================================================
   KPI CARDS
   ===================================================== */

div[data-testid="stMetric"] {

    background: rgba(255, 255, 255, 0.92);

    border: 1px solid rgba(148, 163, 184, 0.25);

    border-radius: 18px;

    padding: 20px 18px;

    min-height: 125px;

    box-shadow:
        0 7px 22px rgba(15, 23, 42, 0.08);

    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease;
}


div[data-testid="stMetric"]:hover {

    transform: translateY(-6px);

    box-shadow:
        0 15px 32px rgba(79, 70, 229, 0.16);

    border-color:
        rgba(79, 70, 229, 0.35);
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
   CHART CONTAINER
   ===================================================== */

div[data-testid="stPlotlyChart"] {

    background: rgba(255, 255, 255, 0.78);

    border-radius: 18px;

    padding: 10px;

    box-shadow:
        0 7px 22px rgba(15, 23, 42, 0.06);

    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease;
}


div[data-testid="stPlotlyChart"]:hover {

    transform: translateY(-3px);

    box-shadow:
        0 14px 30px rgba(79, 70, 229, 0.11);
}


/* =====================================================
   DATA TABLE
   ===================================================== */

div[data-testid="stDataFrame"] {

    background: rgba(255,255,255,0.9);

    border-radius: 16px;

    overflow: hidden;

    box-shadow:
        0 6px 20px rgba(15, 23, 42, 0.06);
}


/* =====================================================
   ALERT / INSIGHT BOXES
   ===================================================== */

div[data-testid="stAlert"] {

    border-radius: 14px !important;

    animation:
        fadeInUp 0.5s ease;
}


/* =====================================================
   DIVIDERS
   ===================================================== */

hr {
    border-color:
        rgba(100, 116, 139, 0.16);
}


/* =====================================================
   CAPTION
   ===================================================== */

.stCaption {
    color: #64748b !important;
}


/* =====================================================
   ANIMATION
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

</style>
""", unsafe_allow_html=True)


# =========================================================
# SALESINSIGHT SIDEBAR
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
        '<div class="sidebar-card-title">🚨 Current Module</div>'
        '<div class="sidebar-card-text">'
        'Sales Anomaly Detection'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">📊 Analysis Type</div>'
        '<div class="sidebar-card-text">'
        'Daily Sales Monitoring'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">📐 Detection Method</div>'
        '<div class="sidebar-card-text">'
        'Rolling Mean + Standard Deviation'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # -----------------------------
    # ORIGINAL CONTROLS
    # -----------------------------

    st.markdown(
        '<div class="sidebar-card-title">'
        '⚙️ Detection Settings'
        '</div>',
        unsafe_allow_html=True
    )

    window = st.slider(
        "Rolling Window (Days)",
        min_value=7,
        max_value=30,
        value=14
    )

    threshold = st.slider(
        "Anomaly Threshold (Standard Deviations)",
        min_value=1.0,
        max_value=3.0,
        value=2.0,
        step=0.5
    )

    st.divider()

    st.caption(
        "SalesInsight Analytics System"
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
    '<div class="anomaly-title">'
    '🚨 Sales Anomaly Detection'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="anomaly-subtitle">'
    'Identifying unusual increases or decreases in daily sales.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# DAILY SALES
# =========================================================

daily_sales = (
    df.set_index("InvoiceDate")
      .resample("D")["Sales Amount"]
      .sum()
)

daily_sales = daily_sales.asfreq("D").fillna(0)


# =========================================================
# ANOMALY CALCULATION
# =========================================================

rolling_mean = daily_sales.rolling(
    window=window
).mean()

rolling_std = daily_sales.rolling(
    window=window
).std()

upper_limit = rolling_mean + (
    threshold * rolling_std
)

lower_limit = rolling_mean - (
    threshold * rolling_std
)

anomalies = (
    (daily_sales > upper_limit) |
    (daily_sales < lower_limit)
)


anomaly_data = pd.DataFrame({

    "Date": daily_sales.index,

    "Sales": daily_sales.values,

    "Rolling Average":
        rolling_mean.values,

    "Upper Limit":
        upper_limit.values,

    "Lower Limit":
        lower_limit.values,

    "Anomaly":
        anomalies.values
})


anomaly_data = anomaly_data.dropna(
    subset=[
        "Rolling Average",
        "Upper Limit",
        "Lower Limit"
    ]
)


# =========================================================
# KPI CARDS
# =========================================================

total_anomalies = int(
    anomaly_data["Anomaly"].sum()
)

highest_sales_day = daily_sales.idxmax()

highest_sales_value = daily_sales.max()

lowest_sales_day = daily_sales.idxmin()

lowest_sales_value = daily_sales.min()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Anomalous Days",
        total_anomalies
    )


with col2:

    st.metric(
        "Highest Sales Day",
        highest_sales_day.strftime(
            "%d %b %Y"
        )
    )


with col3:

    st.metric(
        "Highest Daily Sales",
        f"${highest_sales_value:,.0f}"
    )


with col4:

    st.metric(
        "Lowest Daily Sales",
        f"${lowest_sales_value:,.0f}"
    )


st.divider()


# =========================================================
# ANOMALY CHART
# =========================================================

st.subheader(
    "📈 Daily Sales with Anomaly Limits"
)


fig = go.Figure()


# -----------------------------
# Daily Sales
# -----------------------------

fig.add_trace(
    go.Scatter(

        x=anomaly_data["Date"],

        y=anomaly_data["Sales"],

        mode="lines",

        name="Daily Sales",

        line=dict(
            color="#2563EB",
            width=2.5
        )
    )
)


# -----------------------------
# Rolling Average
# -----------------------------

fig.add_trace(
    go.Scatter(

        x=anomaly_data["Date"],

        y=anomaly_data["Rolling Average"],

        mode="lines",

        name="Rolling Average",

        line=dict(
            color="#7C3AED",
            width=2.5
        )
    )
)


# -----------------------------
# Upper Limit
# -----------------------------

fig.add_trace(
    go.Scatter(

        x=anomaly_data["Date"],

        y=anomaly_data["Upper Limit"],

        mode="lines",

        name="Upper Limit",

        line=dict(
            color="#F97316",
            width=2,
            dash="dash"
        )
    )
)


# -----------------------------
# Lower Limit
# -----------------------------

fig.add_trace(
    go.Scatter(

        x=anomaly_data["Date"],

        y=anomaly_data["Lower Limit"],

        mode="lines",

        name="Lower Limit",

        line=dict(
            color="#F97316",
            width=2,
            dash="dash"
        )
    )
)


# -----------------------------
# Anomaly Points
# -----------------------------

anomaly_points = anomaly_data[
    anomaly_data["Anomaly"] == True
]


fig.add_trace(
    go.Scatter(

        x=anomaly_points["Date"],

        y=anomaly_points["Sales"],

        mode="markers",

        name="Anomalies",

        marker=dict(

            size=11,

            symbol="x",

            color="#DC2626",

            line=dict(
                width=2,
                color="#991B1B"
            )
        )
    )
)


# -----------------------------
# Chart Layout
# -----------------------------

fig.update_layout(

    height=550,

    template="plotly_white",

    hovermode="x unified",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(255,255,255,0.55)",

    xaxis_title="Date",

    yaxis_title="Sales Amount (AUD)",

    font=dict(
        family="Arial",
        color="#172554"
    ),

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),

    margin=dict(
        l=30,
        r=30,
        t=60,
        b=30
    )
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# ANOMALY TABLE
# =========================================================

st.subheader(
    "📋 Detected Anomalies"
)


display_anomalies = anomaly_data[
    anomaly_data["Anomaly"] == True
].copy()


display_anomalies["Date"] = (
    display_anomalies["Date"]
    .dt.strftime("%d %B %Y")
)


display_anomalies["Sales"] = (
    display_anomalies["Sales"]
    .map(lambda x: f"${x:,.0f}")
)


display_anomalies["Rolling Average"] = (
    display_anomalies["Rolling Average"]
    .map(lambda x: f"${x:,.0f}")
)


display_anomalies["Upper Limit"] = (
    display_anomalies["Upper Limit"]
    .map(lambda x: f"${x:,.0f}")
)


display_anomalies["Lower Limit"] = (
    display_anomalies["Lower Limit"]
    .map(lambda x: f"${x:,.0f}")
)


st.dataframe(

    display_anomalies,

    use_container_width=True,

    hide_index=True
)


# =========================================================
# INSIGHTS
# =========================================================

st.subheader(
    "💡 Anomaly Insights"
)


if total_anomalies == 0:

    st.info(
        "No unusual sales days were detected "
        "using the selected settings."
    )

else:

    st.warning(

        f"{total_anomalies} unusual sales day(s) "
        "were detected. These dates may require "
        "business investigation."
    )


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "Method: Rolling mean and standard deviation. "
    "A day is marked anomalous when its sales exceed "
    "the selected limits."
)