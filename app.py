import streamlit as st
import pandas as pd
import webbrowser
from predict import predict_loan


# ==========================================================
# THEME
# ==========================================================

if "theme" not in st.session_state:
    st.session_state["theme"] = "light"


def toggle_theme():
    if st.session_state["theme"] == "light":
        st.session_state["theme"] = "dark"
    else:
        st.session_state["theme"] = "light"


if st.session_state["theme"] == "light":
    bg_color = "#FFFFFF"
    text_color = "#000000"
    button_bg = "#007BFF"
    switch_icon = "🌞"
else:
    bg_color = "#000000"
    text_color = "#FFFFFF"
    button_bg = "#1E90FF"
    switch_icon = "🌙"


# ==========================================================
# CSS
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

        .stButton > button {{
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
# HEADER
# ==========================================================

col1, col2 = st.columns([6, 1])

with col1:
    st.title("🏦 Loan Prediction App")

with col2:

    toggle_state = st.checkbox(
        switch_icon,
        value=(st.session_state["theme"] == "dark"),
        key="theme_checkbox"
    )

    if toggle_state != (st.session_state["theme"] == "dark"):
        toggle_theme()
        st.rerun()


# ==========================================================
# MAIN CONTAINER
# ==========================================================

st.markdown(
    '<div class="container">',
    unsafe_allow_html=True
)

st.markdown(
    "### Fill in the details to check your loan status."
)


# ==========================================================
# SYNCHRONIZED SLIDER + NUMBER INPUT
# ==========================================================

def sync_slider_to_input(key):
    """
    When slider changes, update the number input.
    """
    st.session_state[f"{key}_input"] = st.session_state[key]


def sync_input_to_slider(key):
    """
    When number input changes, update the slider.
    """
    st.session_state[key] = st.session_state[f"{key}_input"]


def slider_with_text(
    label,
    min_val,
    max_val,
    step,
    format_str,
    key,
    suffix=""
):

    # ------------------------------------------------------
    # Initialize values
    # ------------------------------------------------------

    if key not in st.session_state:
        st.session_state[key] = min_val

    input_key = f"{key}_input"

    if input_key not in st.session_state:
        st.session_state[input_key] = min_val


    # ------------------------------------------------------
    # Create columns
    # ------------------------------------------------------

    col1, col2 = st.columns([3, 1])


    # ------------------------------------------------------
    # Slider
    # ------------------------------------------------------

    with col1:

        st.slider(
            label,
            min_value=min_val,
            max_value=max_val,
            step=step,
            format=format_str,
            key=key,
            on_change=sync_slider_to_input,
            args=(key,)
        )


    # ------------------------------------------------------
    # Number input
    # ------------------------------------------------------

    with col2:

        st.number_input(
            label,
            min_value=min_val,
            max_value=max_val,
            step=step,
            key=input_key,
            label_visibility="collapsed",
            on_change=sync_input_to_slider,
            args=(key,)
        )


    # ------------------------------------------------------
    # Return the current value
    # ------------------------------------------------------

    return int(st.session_state[key])


# ==========================================================
# INPUTS
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
# EDUCATION
# ==========================================================

grad = st.radio(
    "Education",
    ["Graduated", "Not Graduated"],
    horizontal=True,
    key="education"
)


# ==========================================================
# SELF EMPLOYED
# ==========================================================

self_emp = st.radio(
    "Self Employed",
    ["Yes", "No"],
    horizontal=True,
    key="self_employed"
)


# ==========================================================
# LOAN AMOUNT
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
# ANNUAL INCOME
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
# LOAN DURATION
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
# CIBIL SCORE
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
# ASSETS
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
# CONVERT CATEGORICAL VALUES
# ==========================================================

grad_s = 0 if grad == "Graduated" else 1

emp_s = 0 if self_emp == "No" else 1


# ==========================================================
# PREDICT BUTTON
# ==========================================================

if st.button("Predict"):

    # ------------------------------------------------------
    # Get FINAL values
    # ------------------------------------------------------

    no_of_dep = int(st.session_state["no_of_dep"])
    Loan_Amount = int(st.session_state["Loan_Amount"])
    Annual_Income = int(st.session_state["Annual_Income"])
    Loan_Dur = int(st.session_state["Loan_Dur"])
    Cibil = int(st.session_state["Cibil"])
    Assets = int(st.session_state["Assets"])


    # ------------------------------------------------------
    # Store values for results page
    # ------------------------------------------------------

    st.session_state["loan_amount"] = Loan_Amount

    st.session_state["annual_income"] = Annual_Income

    st.session_state["loan_duration"] = Loan_Dur

    st.session_state["cibil_score"] = Cibil

    st.session_state["assets"] = Assets


    # ------------------------------------------------------
    # Prediction
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
    # Go to results page
    # ------------------------------------------------------

    st.switch_page("pages/results.py")


# ==========================================================
# CLOSE CONTAINER
# ==========================================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
)
