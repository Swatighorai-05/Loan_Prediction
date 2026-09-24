import streamlit as st
import pandas as pd
import webbrowser
from predict import predict_loan

# Initialize session state for theme mode
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

# Function to toggle theme
def toggle_theme():
    st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"

# Define Styles for Light and Dark Mode
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

st.markdown(f"""
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
""", unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])
with col1:
    st.title("🏦 Loan Prediction App")
with col2:
    toggle_state = st.checkbox(switch_icon, value=(st.session_state["theme"] == "dark"))

if toggle_state != (st.session_state["theme"] == "dark"):
    toggle_theme()
    st.rerun()

st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown("### Fill in the details to check your loan status.")

# Function for synchronized slider & text input
def slider_with_text(label, min_val, max_val, step, format_str, key, suffix=""):
    col1, col2 = st.columns([3, 1])

    if key not in st.session_state:
        st.session_state[key] = min_val

    slider_value = col1.slider(label, min_val, max_val, st.session_state[key], step=step, format=format_str, key=f"slider_{key}")
    text_value = col2.text_input("", value=f"{slider_value}", key=f"text_{key}")

    if text_value != str(st.session_state[key]):
        try:
            new_value = int(text_value.replace("₹", "").replace(",", "").replace(suffix, "").strip())
            if min_val <= new_value <= max_val:
                st.session_state[key] = new_value
                st.rerun()
        except ValueError:
            pass

    return st.session_state[key]

# Loan-related inputs
no_of_dep = slider_with_text("No of Dependents", 0, 10, 1, "%d", "no_of_dep")
grad = st.radio("Education", ["Graduated", "Not Graduated"], horizontal=True)
self_emp = st.radio("Self Employed", ["Yes", "No"], horizontal=True)
Loan_Amount = slider_with_text("Loan Amount", 0, 50000000, 100000, "₹ %d", "Loan_Amount", "₹")
Annual_Income = slider_with_text("Annual Income", 10000, 10000000, 50000, "₹ %d", "Annual_Income", "₹")
Loan_Dur = slider_with_text("Loan Duration (Years)", 1, 30, 1, "%d Yr", "Loan_Dur", "Yr")
Cibil = slider_with_text("Cibil Score", 300, 900, 10, "%d", "Cibil")
Assets = slider_with_text("Assets Value", 0, 50000000, 100000, "₹ %d", "Assets", "₹")

# Convert categorical values
grad_s = 0 if grad == "Graduated" else 1
emp_s = 0 if self_emp == "No" else 1

# Predict Button
if st.button("Predict"):
    result_text = predict_loan(no_of_dep, grad_s, emp_s, Annual_Income, Loan_Amount, Loan_Dur, Cibil, Assets)

    # Store results in session state
    st.session_state["loan_status"] = result_text
    st.session_state["loan_amount"] = Loan_Amount
    st.session_state["annual_income"] = Annual_Income
    st.session_state["loan_duration"] = Loan_Dur
    st.session_state["cibil_score"] = Cibil
    st.session_state["assets"] = Assets

    # Redirect to results page
    st.switch_page("pages/results.py")  # If using Streamlit 1.25+
    # Alternatively, open in browser:
    # webbrowser.open("http://localhost:8501/results")

st.markdown('</div>', unsafe_allow_html=True)
