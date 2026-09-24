import streamlit as st
import pandas as pd
import webbrowser
from predict import predict_loan


# ==========================================================
# Initialize session state for theme mode
# ==========================================================

if "theme" not in st.session_state:
    st.session_state["theme"] = "light"


# ==========================================================
# Function to toggle theme
# ==========================================================

def toggle_theme():
    if st.session_state["theme"] == "light":
        st.session_state["theme"] = "dark"
    else:
        st.session_state["theme"] = "light"


# ==========================================================
# Define Styles for Light and Dark Mode
# ==========================================================

if st.session_state["theme"] == "light":

    bg_color = "#FFFFFF"
    text_color = "#000000"
    button_bg = "#007BFF"
    switch_bg = "#DDD"
    switch_circle = "#FFF"
    switch_icon = "🌞"

else:

    bg_color = "#000000"
    text_color = "#FFFFFF"
    button_bg = "#1E90FF"
    switch_bg = "#007BFF"
    switch_circle = "#FFF"
    switch_icon = "🌙"


# ==========================================================
# Custom CSS
# ==========================================================

st.markdown(
    f"""
    <style>

        .stApp {{
            background-color: {bg_color};
        }}

        .container {{
            text-align: center;
            padding: 30px;
            background-color: {bg_color};
            border-radius: 15px;
            width: 50%;
            color: {text_color};
        }}

        h1, h2, h3, h4, h5, h6, p, label {{
            color: {text_color} !important;
        }}

        .stButton>button {{
            background-color: {button_bg};
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
            width: 100%;
        }}

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# Header
# ==========================================================

col1, col2 = st.columns([6, 1])


with col1:
    st.title("🏦 Loan Prediction App")


with col2:

    toggle_state = st.checkbox(
        switch_icon,
        value=(st.session_state["theme"] == "dark")
    )


if toggle_state != (st.session_state["theme"] == "dark"):

    toggle_theme()
    st.rerun()


# ==========================================================
# Main container
# ==========================================================

st.markdown(
    '<div class="container">',
    unsafe_allow_html=True
)

st.markdown(
    "### Fill in the details to check your loan status."
)


# ==========================================================
# Slider + Text Input Function
# ==========================================================

def slider_with_text(
    label,
    min_val,
    max_val,
    step,
    format_str,
    key,
    suffix=""
):

    col1, col2 = st.columns([3, 1])

    # ------------------------------------------------------
    # Initialize session state
    # ------------------------------------------------------

    if key not in st.session_state:
        st.session_state[key] = min_val


    # ------------------------------------------------------
    # Slider
    #
    # IMPORTANT:
    # We do NOT give the slider a manual session-state key.
    # This prevents StreamlitWidgetAlreadyInstantiatedError.
    # ------------------------------------------------------

    slider_value = col1.slider(
        label,
        min_value=min_val,
        max_value=max_val,
        value=int(st.session_state[key]),
        step=step,
        format=format_str
    )


    # ------------------------------------------------------
    # IMPORTANT:
    # Save the CURRENT slider value
    # ------------------------------------------------------

    st.session_state[key] = int(slider_value)


    # ------------------------------------------------------
    # Text input
    # ------------------------------------------------------

    text_value = col2.text_input(
        "",
        value=str(st.session_state[key])
    )


    # ------------------------------------------------------
    # Clean text input
    # ------------------------------------------------------

    cleaned_value = (
        text_value
        .replace("₹", "")
        .replace(",", "")
        .replace(suffix, "")
        .strip()
    )


    # ------------------------------------------------------
    # Handle manual text input
    # ------------------------------------------------------

    try:

        new_value = int(cleaned_value)

        if min_val <= new_value <= max_val:

            if new_value != st.session_state[key]:

                st.session_state[key] = new_value

                # Rerun so the slider receives the new value
                st.rerun()

    except ValueError:

        pass


    # ------------------------------------------------------
    # Return the latest value
    # ------------------------------------------------------

    return int(st.session_state[key])


# ==========================================================
# Loan-related Inputs
# ==========================================================

no_of_dep = slider_with_text(
    "No of Dependents",
    0,
    10,
    1,
    "%d",
    "no_of_dep"
)


# ==========================================================
# Education
# ==========================================================

grad = st.radio(
    "Education",
    ["Graduated", "Not Graduated"],
    horizontal=True
)


# ==========================================================
# Self Employed
# ==========================================================

self_emp = st.radio(
    "Self Employed",
    ["Yes", "No"],
    horizontal=True
)


# ==========================================================
# Loan Amount
# ==========================================================

Loan_Amount = slider_with_text(
    "Loan Amount",
    0,
    50000000,
    100000,
    "₹ %d",
    "Loan_Amount",
    "₹"
)


# ==========================================================
# Annual Income
# ==========================================================

Annual_Income = slider_with_text(
    "Annual Income",
    10000,
    10000000,
    50000,
    "₹ %d",
    "Annual_Income",
    "₹"
)


# ==========================================================
# Loan Duration
# ==========================================================

Loan_Dur = slider_with_text(
    "Loan Duration (Years)",
    1,
    30,
    1,
    "%d Yr",
    "Loan_Dur",
    "Yr"
)


# ==========================================================
# CIBIL Score
# ==========================================================

Cibil = slider_with_text(
    "Cibil Score",
    300,
    900,
    10,
    "%d",
    "Cibil"
)


# ==========================================================
# Assets
# ==========================================================

Assets = slider_with_text(
    "Assets Value",
    0,
    50000000,
    100000,
    "₹ %d",
    "Assets",
    "₹"
)


# ==========================================================
# Convert categorical values
# ==========================================================

grad_s = 0 if grad == "Graduated" else 1

emp_s = 0 if self_emp == "No" else 1


# ==========================================================
# Predict Button
# ==========================================================

if st.button("Predict"):

    # ------------------------------------------------------
    # Make sure the latest values are stored
    # ------------------------------------------------------

    Loan_Amount = int(Loan_Amount)
    Annual_Income = int(Annual_Income)
    Loan_Dur = int(Loan_Dur)
    Cibil = int(Cibil)
    Assets = int(Assets)
    no_of_dep = int(no_of_dep)


    # ------------------------------------------------------
    # Store input values
    # ------------------------------------------------------

    st.session_state["loan_amount"] = Loan_Amount

    st.session_state["annual_income"] = Annual_Income

    st.session_state["loan_duration"] = Loan_Dur

    st.session_state["cibil_score"] = Cibil

    st.session_state["assets"] = Assets


    # ------------------------------------------------------
    # Run prediction
    # ------------------------------------------------------

    result_text = predict_loan(
        no_of_dep,
        grad_s,
        emp_s,
        Annual_Income,
        Loan_Amount,
        Loan_Dur,
        Cibil,
        Assets
    )


    # ------------------------------------------------------
    # Store prediction result
    # ------------------------------------------------------

    st.session_state["loan_status"] = result_text


    # ------------------------------------------------------
    # Go to Results page
    # ------------------------------------------------------

    st.switch_page("pages/results.py")


# ==========================================================
# Close container
# ==========================================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
)
