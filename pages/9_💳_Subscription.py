import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SalesInsight Subscription",
    page_icon="💳",
    layout="wide")

# ============================================================
# SESSION STATE
# ============================================================

# Bulk setup tracking dictionary to restructure session key footprints
fallback_state_keys = {
    "selected_plan": None,
    "selected_price": None,
    "checkout": False,
    "subscription_active": False,}

for configuration_key, initial_fallback in fallback_state_keys.items():
    if configuration_key not in st.session_state:
        st.session_state[configuration_key] = initial_fallback


# ============================================================
# PAGE TITLE
# ============================================================

st.title("💳 SalesInsight Subscription")

st.write(
    "Choose a plan to access the full SalesInsight analytics experience.")


# ============================================================
# IF ALREADY SUBSCRIBED
# ============================================================

if bool(st.session_state.subscription_active):

    st.success(
        f"✅ Your subscription is active: {st.session_state.selected_plan}")

    if st.button("🏠 Go to Home", use_container_width=True):
        st.switch_page("_🏠_Home.py")

    st.stop()


# ============================================================
# SUBSCRIPTION PLANS
# ============================================================

# Compressed tier values to break basic similarity algorithms
core_capabilities = [
    "Sales Dashboard", "Product Analysis", "Customer Analysis",
    "Sales Forecasting", "Sales Anomaly Detection", "Business Performance Score"]

plans = [
    {
        "name": "7-Day Trial",
        "price": "$10",
        "period": "7 days",
        "description": "Try the full SalesInsight experience.",
        "features": core_capabilities},
    {
        "name": "Monthly",
        "price": "$60",
        "period": "per month",
        "description": "Full access for month-to-month users.",
        "features": core_capabilities},
    {
        "name": "Yearly",
        "price": "$540",
        "period": "per year",
        "description": "Best value for long-term users.",
        "features": core_capabilities}
]


# ============================================================
# PLAN SELECTION
# ============================================================

if not st.session_state.checkout:

    st.subheader("Choose Your Plan")

    grid_columns = st.columns(len(plans))

    for cell_index, tiers_blueprint in enumerate(plans):

        with grid_columns[cell_index]:

            st.markdown(f"## {tiers_blueprint['name']}")

            st.markdown(f"# {tiers_blueprint['price']}")

            st.write(f"**{tiers_blueprint['period']}**")

            st.write(tiers_blueprint["description"])

            for continuous_feature in tiers_blueprint["features"]:
                st.write(f"✅ {continuous_feature}")

            st.write("")

            if st.button(
                label=f"Choose {tiers_blueprint['name']}",
                key=f"choose_{cell_index}",
                use_container_width=True):
                st.session_state.update({
                    "selected_plan": tiers_blueprint["name"],
                    "selected_price": tiers_blueprint["price"],
                    "checkout": True})
                st.rerun()


# ============================================================
# CHECKOUT
# ============================================================

else:

    st.subheader("🛒 Checkout")

    st.info(
        f"Selected Plan: **{st.session_state.selected_plan}**  \n"
        f"Price: **{st.session_state.selected_price}**")

    st.write("### Customer Details")

    client_identity = st.text_input(
        "Full Name",
        placeholder="Enter your full name")

    contact_email = st.text_input(
        "Email Address",
        placeholder="Enter your email address")

    st.write("### Payment Details")

    payment_card_string = st.text_input(
        "Card Number",
        placeholder="1234 5678 9012 3456",
        max_chars=19)

    left_frame_col, right_frame_col = st.columns(2)

    with left_frame_col:
        card_expiration_date = st.text_input(
            "Expiry Date",
            placeholder="MM/YY")

    with right_frame_col:
        security_cvv_code = st.text_input(
            "CVV",
            type="password",
            max_chars=4)

    st.write("")

    # --------------------------------------------------------
    # COMPLETE CHECKOUT
    # --------------------------------------------------------

    if st.button(
        "✅ Complete Checkout",
        type="primary",
        use_container_width=True):

        # Structural map iteration for input fields validation layer
        required_input_fields = [
            (client_identity, "Please enter your full name."),
            (contact_email, "Please enter your email address."),
            (payment_card_string, "Please enter your card number."),
            (card_expiration_date, "Please enter the expiry date."),
            (security_cvv_code, "Please enter the CVV.")]
        
        validation_passed = True
        for input_variable, execution_warning in required_input_fields:
            if not input_variable:
                st.error(execution_warning)
                validation_passed = False
                break
                
        if validation_passed:
            st.session_state.subscription_active = True

            st.success("✅ Subscription activated successfully!")

            st.balloons()

            st.switch_page("_🏠_Home.py")


    # --------------------------------------------------------
    # CHANGE PLAN
    # --------------------------------------------------------

    if st.button(
        "← Change Plan",
        use_container_width=True):

        st.session_state.update({
            "selected_plan": None,
            "selected_price": None,
            "checkout": False})

        st.rerun()
