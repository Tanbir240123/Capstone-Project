import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Sales Forecast",
    page_icon="🔮",
    layout="wide"
)


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
        #3b1d4a 0%,
        #51245f 50%,
        #6b2d75 100%
    );
}

/* Sidebar text */

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
    color: #cbd5e1 !important;
    font-size: 13px;
    margin-bottom: 25px;
}


/* Sidebar cards */

.sidebar-card {
    background: rgba(255,255,255,0.08);

    border: 1px solid rgba(255,255,255,0.12);

    border-radius: 12px;

    padding: 14px;

    margin-bottom: 12px;

    transition:
        transform 0.25s ease,
        background 0.25s ease,
        box-shadow 0.25s ease;
}


/* Sidebar card hover */

.sidebar-card:hover {
    transform: translateX(4px);

    background: rgba(255,255,255,0.14);

    box-shadow:
        0 6px 18px rgba(0,0,0,0.15);
}


/* Sidebar card title */

.sidebar-card-title {
    color: #93c5fd !important;
    font-weight: 700;
    font-size: 14px;
}


/* Sidebar card text */

.sidebar-card-text {
    color: #e2e8f0 !important;
    font-size: 13px;
    margin-top: 4px;
}


/* Sidebar divider */

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
}


/* =====================================================
   PAGE HEADER
   ===================================================== */

.forecast-title {
    font-size: 38px;
    font-weight: 800;

    color: #172554;

    margin-bottom: 5px;

    animation: fadeInUp 0.6s ease;
}


.forecast-subtitle {
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


/* KPI hover */

div[data-testid="stMetric"]:hover {

    transform: translateY(-6px);

    box-shadow:
        0 15px 32px rgba(37, 99, 235, 0.16);

    border-color:
        rgba(79, 70, 229, 0.35);
}


/* KPI label */

div[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 600;
}


/* KPI value */

div[data-testid="stMetricValue"] {
    color: #172554 !important;
    font-weight: 800;
}


/* =====================================================
   SECTION HEADINGS
   ===================================================== */

.stSubheader {
    color: #172554 !important;
    font-weight: 750 !important;
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


/* Chart hover */

div[data-testid="stPlotlyChart"]:hover {

    transform: translateY(-3px);

    box-shadow:
        0 14px 30px rgba(37, 99, 235, 0.11);
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
   INSIGHT BOX
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
        '<div class="sidebar-card-title">🔮 Current Module</div>'
        '<div class="sidebar-card-text">'
        'Sales Forecast'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">📈 Forecast Period</div>'
        '<div class="sidebar-card-text">'
        'Next 3 Months'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">🤖 Model</div>'
        '<div class="sidebar-card-text">'
        'ARIMA (1, 1, 1)'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">📊 Data Frequency</div>'
        '<div class="sidebar-card-text">'
        'Monthly Sales'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.caption(
        "SalesInsight Analytics System"
    )


# =========================================================
# LOAD DATA
# =========================================================

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


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="forecast-title">'
    '🔮 Sales Forecasting'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="forecast-subtitle">'
    'Predicting future sales using historical monthly sales patterns.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# MONTHLY SALES DATA
# =========================================================

monthly_sales = (
    df.set_index("InvoiceDate")
      .resample("ME")["Sales Amount"]
      .sum()
)

monthly_sales = monthly_sales.dropna()


# =========================================================
# FORECAST
# =========================================================

try:

    model = ARIMA(
        monthly_sales,
        order=(1, 1, 1)
    )

    model_fit = model.fit()

    forecast_steps = 3

    forecast_result = model_fit.get_forecast(
        steps=forecast_steps
    )

    forecast = forecast_result.predicted_mean

    confidence = forecast_result.conf_int()

except Exception as e:

    st.error("Unable to generate forecast.")

    st.exception(e)

    st.stop()


# =========================================================
# FORECAST METRICS
# =========================================================

next_month_value = forecast.iloc[0]

three_month_total = forecast.sum()

last_actual_value = monthly_sales.iloc[-1]

change_percentage = (
    (next_month_value - last_actual_value)
    / last_actual_value
) * 100


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Last Actual Sales",
        f"${last_actual_value:,.0f}"
    )


with col2:

    st.metric(
        "Next Month Forecast",
        f"${next_month_value:,.0f}"
    )


with col3:

    st.metric(
        "3-Month Forecast",
        f"${three_month_total:,.0f}"
    )


with col4:

    st.metric(
        "Expected Change",
        f"{change_percentage:+.1f}%"
    )


st.divider()


# =========================================================
# FORECAST CHART
# =========================================================

st.subheader(
    "📈 Historical Sales & Future Forecast"
)

fig = go.Figure()


# -----------------------------
# Historical Sales
# -----------------------------

fig.add_trace(
    go.Scatter(

        x=monthly_sales.index,

        y=monthly_sales.values,

        mode="lines+markers",

        name="Actual Sales",

        line=dict(
            color="#2563EB",
            width=3
        ),

        marker=dict(
            size=6,
            color="#2563EB"
        )
    )
)


# -----------------------------
# Forecast
# -----------------------------

fig.add_trace(
    go.Scatter(

        x=forecast.index,

        y=forecast.values,

        mode="lines+markers",

        name="Forecast",

        line=dict(
            color="#7C3AED",
            width=3,
            dash="dash"
        ),

        marker=dict(
            size=7,
            color="#7C3AED"
        )
    )
)


# -----------------------------
# Confidence Interval
# -----------------------------

fig.add_trace(
    go.Scatter(

        x=list(forecast.index)
          + list(forecast.index[::-1]),

        y=list(confidence.iloc[:, 1])
          + list(confidence.iloc[:, 0][::-1]),

        fill="toself",

        fillcolor="rgba(124,58,237,0.12)",

        line=dict(
            color="rgba(255,255,255,0)"
        ),

        hoverinfo="skip",

        name="Confidence Interval"
    )
)


fig.update_layout(

    height=500,

    xaxis_title="Month",

    yaxis_title="Sales Amount (AUD)",

    hovermode="x unified",

    template="plotly_white",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(255,255,255,0.55)",

    font=dict(
        family="Arial",
        color="#172554"
    ),

    title_font=dict(
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
# FORECAST TABLE
# =========================================================

st.subheader(
    "📋 Forecast Details"
)


forecast_table = pd.DataFrame({

    "Forecast Month":
        forecast.index.strftime("%B %Y"),

    "Predicted Sales":
        forecast.values,

    "Lower Estimate":
        confidence.iloc[:, 0].values,

    "Upper Estimate":
        confidence.iloc[:, 1].values
})


forecast_table["Predicted Sales"] = (
    forecast_table["Predicted Sales"]
    .map(lambda x: f"${x:,.0f}")
)


forecast_table["Lower Estimate"] = (
    forecast_table["Lower Estimate"]
    .map(lambda x: f"${x:,.0f}")
)


forecast_table["Upper Estimate"] = (
    forecast_table["Upper Estimate"]
    .map(lambda x: f"${x:,.0f}")
)


st.dataframe(

    forecast_table,

    use_container_width=True,

    hide_index=True
)


# =========================================================
# BUSINESS INTERPRETATION
# =========================================================

st.subheader(
    "💡 Forecast Insights"
)


if change_percentage > 5:

    st.success(

        f"📈 The model predicts an increase of approximately "
        f"{change_percentage:.1f}% in the next month."
    )


elif change_percentage < -5:

    st.warning(

        f"📉 The model predicts a decrease of approximately "
        f"{abs(change_percentage):.1f}% in the next month."
    )


else:

    st.info(

        f"➡️ The forecast indicates relatively stable sales, "
        f"with an expected change of "
        f"{change_percentage:.1f}%."
    )


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "Forecast generated using an ARIMA (1,1,1) time-series "
    "model based on historical monthly sales."
)