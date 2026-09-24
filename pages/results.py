import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Loan EMI Calculation Function
def calculate_emi(principal, rate, tenure):
    monthly_rate = rate / (12 * 100)  
    months = tenure * 12  

    if monthly_rate > 0:
        emi = (principal * monthly_rate * ((1 + monthly_rate) ** months)) / (((1 + monthly_rate) ** months) - 1)
    else:
        emi = principal / months  

    total_payment = emi * months
    total_interest = total_payment - principal

    return round(emi), round(total_interest), round(total_payment)

# Fetch stored values (Ensure Defaults)
loan_status = st.session_state.get("loan_status", "No Prediction Made")
loan_amount = max(st.session_state.get("loan_amount", 1000000), 0)  
annual_income = max(st.session_state.get("annual_income", 500000), 0)
loan_tenure = max(st.session_state.get("loan_duration", 5), 1)  
cibil_score = max(st.session_state.get("cibil_score", 750), 300)
assets = max(st.session_state.get("assets", 2000000), 0)
interest_rate = 6.5  # Default Interest Rate

st.title("Loan Approval Status")

if loan_status == "Loan Is Approved":
    st.success("✅ Congratulations! Your loan is **Approved**.")

    st.header("📊 EMI Calculator")
    col1, col2 = st.columns([3, 1])

    # User Input for Loan Calculation (Updates dynamically)
    with col1:
        loan_amount = st.number_input("Loan Amount", value=loan_amount, min_value=0, format="%d")
        interest_rate = st.number_input("Rate of Interest (p.a)", value=interest_rate, min_value=0.1, max_value=20.0, step=0.1, format="%.2f")
        loan_tenure = st.number_input("Loan Tenure (Years)", value=loan_tenure, min_value=1, max_value=30, format="%d")

    # **Recalculate EMI based on new inputs**
    emi, total_interest, total_amount = calculate_emi(loan_amount, interest_rate, loan_tenure)

    with col2:
        st.metric("Monthly EMI", f"₹{emi:,}")
        st.metric("Total Interest", f"₹{total_interest:,}")
        st.metric("Total Amount", f"₹{total_amount:,}")

    # 📊 **Pie Chart for Loan Breakdown**
    fig, ax = plt.subplots()
    labels = ["Principal amount", "Interest amount"]
    sizes = [loan_amount, total_interest]
    colors = ["#DCE3F3", "#4361EE"]
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140, wedgeprops={"edgecolor": "white"})
    ax.axis("equal")  

    st.pyplot(fig)

else:
    st.error("❌ Sorry! Your loan is **Not Approved**.")
    st.warning("Please check your CIBIL score, income, or loan amount.")
