import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Business Performance",
    page_icon="🎯",
    layout="wide"
)


# =========================================================
# CUSTOM THEME
# =========================================================

st.markdown("""
<style>

/* =====================================================
   GLOBAL BACKGROUND
   ===================================================== */

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(16, 185, 129, 0.08),
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
            rgba(16, 185, 129, 0.12),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #111827 0%,
            #172033 50%,
            #0f2f2a 100%
        );
}

[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.10) !important;
}


/* Sidebar title */

.sidebar-title {

    font-size: 27px;

    font-weight: 850;

    color: #ffffff !important;

    margin-bottom: 4px;
}


/* Sidebar subtitle */

.sidebar-subtitle {

    color: #94a3b8 !important;

    font-size: 13px;

    margin-bottom: 25px;
}


/* Sidebar cards */

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
        rgba(16,185,129,0.10);

    border-color:
        rgba(16,185,129,0.28);

    box-shadow:
        0 8px 20px rgba(0,0,0,0.18);
}


.sidebar-card-title {

    color:
        #34d399 !important;

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
   MAIN HEADER
   ===================================================== */

.performance-title {

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


.performance-subtitle {

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
        rgba(255,255,255,0.88);

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
        rgba(16,185,129,0.35);
}


div[data-testid="stMetricLabel"] {

    color:
        #64748b !important;

    font-weight:
        650;
}


div[data-testid="stMetricValue"] {

    color:
        #0f172a !important;

    font-weight:
        850;
}


/* =====================================================
   SECTION HEADINGS
   ===================================================== */

.stSubheader {

    color:
        #0f172a !important;

    font-weight:
        800;
}


/* =====================================================
   CHART CONTAINERS
   ===================================================== */

div[data-testid="stPlotlyChart"] {

    background:
        rgba(255,255,255,0.78);

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
   DATA TABLE
   ===================================================== */

div[data-testid="stDataFrame"] {

    background:
        rgba(255,255,255,0.90);

    border-radius:
        16px;

    overflow:
        hidden;

    box-shadow:
        0 7px 22px rgba(15,23,42,0.06);
}


/* =====================================================
   EXPANDER
   ===================================================== */

[data-testid="stExpander"] {

    background:
        rgba(255,255,255,0.78) !important;

    border:
        1px solid rgba(148,163,184,0.20) !important;

    border-radius:
        15px !important;

    box-shadow:
        0 6px 20px rgba(15,23,42,0.05);
}


/* =====================================================
   DIVIDERS
   ===================================================== */

hr {

    border-color:
        rgba(100,116,139,0.15);
}


/* =====================================================
   INSIGHT BOX
   ===================================================== */

.business-insight {

    background:
        linear-gradient(
            135deg,
            rgba(16,185,129,0.09),
            rgba(59,130,246,0.07)
        );

    border-left:
        5px solid #10b981;

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


.business-insight:hover {

    transform:
        translateX(4px);

    box-shadow:
        0 10px 24px rgba(16,185,129,0.10);
}


/* =====================================================
   SCORE HIGHLIGHT
   ===================================================== */

.score-highlight {

    background:
        linear-gradient(
            135deg,
            #ecfdf5,
            #eff6ff
        );

    border:
        1px solid rgba(16,185,129,0.18);

    border-radius:
        18px;

    padding:
        18px;

    box-shadow:
        0 7px 22px rgba(15,23,42,0.05);
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer-text {

    text-align:
        center;

    color:
        #94a3b8;

    font-size:
        12px;

    margin-top:
        25px;
}


/* =====================================================
   ANIMATION
   ===================================================== */

@keyframes fadeInUp {

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
        '🎯 CURRENT MODULE'
        '</div>'
        '<div class="sidebar-card-text">'
        'Business Performance'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">'
        '⭐ PERFORMANCE'
        '</div>'
        '<div class="sidebar-card-text">'
        'Sales growth, customer activity, order value & consistency'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">'
        '📊 SCORE MODEL'
        '</div>'
        '<div class="sidebar-card-text">'
        'Weighted 0–100 business indicator'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">'
        '📈 COMPONENTS'
        '</div>'
        '<div class="sidebar-card-text">'
        'Growth • Customers • AOV • Consistency'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-card">'
        '<div class="sidebar-card-title">'
        '💡 DECISION SUPPORT'
        '</div>'
        '<div class="sidebar-card-text">'
        'Use the score to understand overall business trends.'
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
    '<div class="performance-title">'
    '🎯 Business Performance Score'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="performance-subtitle">'
    'A transparent score based on sales growth, customer activity, '
    'order value and sales consistency.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# MONTHLY DATA
# =========================================================

monthly = (
    df.set_index("InvoiceDate")
      .resample("ME")
      .agg({
          "Sales Amount": "sum",
          "InvoiceNo": "nunique",
          "CustomerID": "nunique"
      })
)

monthly = monthly.dropna()


# =========================================================
# METRICS
# =========================================================

total_sales = df["Sales Amount"].sum()

total_transactions = df["InvoiceNo"].nunique()

total_customers = df["CustomerID"].nunique()

average_order_value = (
    total_sales / total_transactions
    if total_transactions > 0
    else 0
)


# =========================================================
# SALES GROWTH
# =========================================================

if len(monthly) >= 2:

    previous_sales = monthly["Sales Amount"].iloc[-2]

    latest_sales = monthly["Sales Amount"].iloc[-1]

    if previous_sales != 0:

        sales_growth = (
            (latest_sales - previous_sales)
            / abs(previous_sales)
        ) * 100

    else:

        sales_growth = 0

else:

    sales_growth = 0


# =========================================================
# CUSTOMER GROWTH
# =========================================================

if len(monthly) >= 2:

    previous_customers = monthly["CustomerID"].iloc[-2]

    latest_customers = monthly["CustomerID"].iloc[-1]

    if previous_customers != 0:

        customer_growth = (
            (latest_customers - previous_customers)
            / previous_customers
        ) * 100

    else:

        customer_growth = 0

else:

    customer_growth = 0


# =========================================================
# SALES CONSISTENCY
# =========================================================

monthly_sales = monthly["Sales Amount"]

if monthly_sales.mean() != 0:

    coefficient_variation = (
        monthly_sales.std()
        / monthly_sales.mean()
    )

else:

    coefficient_variation = 0


consistency_score = max(
    0,
    min(
        100,
        100 - (coefficient_variation * 100)
    )
)


# =========================================================
# COMPONENT SCORES
# =========================================================

growth_score = max(
    0,
    min(
        100,
        50 + sales_growth
    )
)


customer_score = max(
    0,
    min(
        100,
        50 + customer_growth
    )
)


order_value_score = max(
    0,
    min(
        100,
        (average_order_value / 500) * 100
    )
)


# =========================================================
# FINAL SCORE
# =========================================================

business_score = (
    growth_score * 0.35
    + customer_score * 0.25
    + order_value_score * 0.20
    + consistency_score * 0.20
)

business_score = max(
    0,
    min(
        100,
        business_score
    )
)


# =========================================================
# PERFORMANCE CATEGORY
# =========================================================

if business_score >= 80:

    performance_label = "Excellent"

elif business_score >= 65:

    performance_label = "Good"

elif business_score >= 50:

    performance_label = "Moderate"

else:

    performance_label = "Needs Attention"


# =========================================================
# TOP KPI CARDS
# =========================================================

col1, col2, col3 = st.columns([1.2, 1, 1])


with col1:

    st.metric(
        "🎯 Business Performance Score",
        f"{business_score:.1f} / 100"
    )


with col2:

    st.metric(
        "⭐ Performance Level",
        performance_label
    )


with col3:

    st.metric(
        "📈 Sales Growth",
        f"{sales_growth:+.1f}%"
    )


st.divider()


# =========================================================
# SCORE GAUGE
# =========================================================

st.subheader("📊 Performance Score")


fig = go.Figure(
    go.Indicator(

        mode="gauge+number",

        value=business_score,

        title={
            "text": performance_label,
            "font": {
                "size": 22,
                "color": "#0f172a"
            }
        },

        number={
            "font": {
                "size": 46,
                "color": "#0f172a"
            }
        },

        gauge={

            "axis": {
                "range": [0, 100],
                "tickcolor": "#64748b"
            },

            "bar": {
                "color": "#10b981"
            },

            "bgcolor": "#e2e8f0",

            "borderwidth": 0,

            "threshold": {

                "line": {
                    "color": "#0f172a",
                    "width": 4
                },

                "thickness": 0.8,

                "value": business_score
            }
        }
    )
)


fig.update_layout(

    height=360,

    paper_bgcolor="rgba(0,0,0,0)",

    font={
        "color": "#0f172a"
    },

    margin={
        "l": 40,
        "r": 40,
        "t": 60,
        "b": 20
    }
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# SCORE COMPONENTS
# =========================================================

st.subheader("🧩 Score Components")


component_data = pd.DataFrame({

    "Metric": [
        "Sales Growth",
        "Customer Activity",
        "Average Order Value",
        "Sales Consistency"
    ],

    "Score": [
        growth_score,
        customer_score,
        order_value_score,
        consistency_score
    ],

    "Weight": [
        "35%",
        "25%",
        "20%",
        "20%"
    ]
})


st.dataframe(
    component_data,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# COMPONENT CHART
# =========================================================

fig2 = go.Figure()


fig2.add_trace(
    go.Bar(

        x=component_data["Metric"],

        y=component_data["Score"],

        text=component_data["Score"].round(1),

        textposition="outside",

        marker=dict(
            color=[
                "#10b981",
                "#3b82f6",
                "#8b5cf6",
                "#f59e0b"
            ],
            line=dict(
                width=0
            )
        ),

        hovertemplate=
            "<b>%{x}</b><br>"
            "Score: %{y:.1f}/100"
            "<extra></extra>"
    )
)


fig2.update_layout(

    title={
        "text": "Performance by Metric",
        "font": {
            "size": 21,
            "color": "#0f172a"
        }
    },

    yaxis_title="Score",

    yaxis_range=[
        0,
        110
    ],

    template="plotly_white",

    height=450,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(255,255,255,0.45)",

    font={
        "color": "#334155"
    },

    margin={
        "l": 40,
        "r": 40,
        "t": 70,
        "b": 50
    }
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# =========================================================
# KEY BUSINESS METRICS
# =========================================================

st.subheader("📌 Key Business Metrics")


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.0f}"
    )


with c2:

    st.metric(
        "🧾 Transactions",
        f"{total_transactions:,}"
    )


with c3:

    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )


with c4:

    st.metric(
        "🛒 Average Order Value",
        f"${average_order_value:,.0f}"
    )


# =========================================================
# BUSINESS INTERPRETATION
# =========================================================

st.subheader("💡 Business Interpretation")


if sales_growth > 0:

    st.markdown(
        f"""
        <div class="business-insight">
        📈 <b>Sales Growth:</b>
        Sales increased by approximately
        <b>{sales_growth:.1f}%</b>
        compared with the previous month.
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""
        <div class="business-insight">
        📉 <b>Sales Growth:</b>
        Sales changed by
        <b>{sales_growth:.1f}%</b>
        compared with the previous month.
        </div>
        """,
        unsafe_allow_html=True
    )


if customer_growth > 0:

    st.markdown(
        f"""
        <div class="business-insight">
        👥 <b>Customer Activity:</b>
        Customer activity increased by approximately
        <b>{customer_growth:.1f}%</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""
        <div class="business-insight">
        👥 <b>Customer Activity:</b>
        Customer activity changed by
        <b>{customer_growth:.1f}%</b>.
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    f"""
    <div class="business-insight">
    🛒 <b>Average Order Value:</b>
    The average order value is
    <b>${average_order_value:,.0f}</b>.
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <div class="business-insight">
    🎯 <b>Overall Score:</b>
    The calculated business performance score is
    <b>{business_score:.1f}/100</b>.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# METHODOLOGY
# =========================================================

with st.expander("ℹ️ How is the score calculated?"):

    st.markdown(
        """
        ### Business Performance Score

        The Business Performance Score is a weighted analytical
        indicator created for this project.

        **Components**

        • 📈 Sales Growth — **35%**

        • 👥 Customer Activity — **25%**

        • 🛒 Average Order Value — **20%**

        • 📊 Sales Consistency — **20%**

        Each component is normalized to a **0–100 scale**
        and then combined using the above weights.

        This score is intended as a dashboard decision-support
        indicator rather than a financial or accounting metric.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer-text">'
    'SalesInsight • Business Performance Analytics'
    '</div>',
    unsafe_allow_html=True
)