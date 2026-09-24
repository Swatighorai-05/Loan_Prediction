import streamlit as st
import matplotlib.pyplot as plt


# -----------------------------
# EMI Calculator
# -----------------------------
def calculate_emi(principal, rate, tenure):
    monthly_rate = rate / (12 * 100)
    months = tenure * 12

    if principal <= 0 or months <= 0:
        return 0, 0, 0

    if monthly_rate > 0:
        emi = (
            principal
            * monthly_rate
            * ((1 + monthly_rate) ** months)
            / (((1 + monthly_rate) ** months) - 1)
        )
    else:
        emi = principal / months

    total_payment = emi * months
    total_interest = total_payment - principal

    return round(emi), round(total_interest), round(total_payment)


# -----------------------------
# Get values from session state
# -----------------------------
loan_status = st.session_state.get("loan_status", "No Prediction Made")

loan_amount = max(
    st.session_state.get("loan_amount", 1000000), 0
)

annual_income = max(
    st.session_state.get("annual_income", 500000), 0
)

loan_tenure = max(
    st.session_state.get("loan_duration", 5), 1
)

cibil_score = max(
    st.session_state.get("cibil_score", 750), 300
)

assets = max(
    st.session_state.get("assets", 2000000), 0
)

interest_rate = 6.5


# -----------------------------
# Calculate EMI
# -----------------------------
emi, total_interest, total_payment = calculate_emi(
    loan_amount,
    interest_rate,
    loan_tenure
)


# -----------------------------
# Page title
# -----------------------------
st.title("Loan Approval Status")


# -----------------------------
# Loan status
# -----------------------------
if loan_status == "Approved":
    st.success("🎉 Congratulations! Your loan is Approved.")
elif loan_status == "Rejected":
    st.error("❌ Sorry! Your loan is Rejected.")
else:
    st.info("No prediction available.")


# -----------------------------
# EMI Calculator
# -----------------------------
st.subheader("📊 EMI Calculator")


col1, col2 = st.columns(2)

with col1:
    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0,
        value=int(loan_amount),
        step=10000
    )

    interest_rate = st.number_input(
        "Rate of Interest (p.a)",
        min_value=0.0,
        value=6.5,
        step=0.1
    )

    loan_tenure = st.number_input(
        "Loan Tenure (Years)",
        min_value=1,
        value=int(loan_tenure),
        step=1
    )


# Recalculate using displayed values
emi, total_interest, total_payment = calculate_emi(
    loan_amount,
    interest_rate,
    loan_tenure
)


with col2:
    st.metric("Monthly EMI", f"₹{emi:,}")
    st.metric("Total Interest", f"₹{total_interest:,}")
    st.metric("Total Amount", f"₹{total_payment:,}")


# -----------------------------
# Pie Chart
# -----------------------------
st.subheader("💰 Loan Breakdown")


if loan_amount > 0 and total_interest > 0:

    labels = [
        "Principal Amount",
        "Interest Amount"
    ]

    sizes = [
        loan_amount,
        total_interest
    ]

    fig, ax = plt.subplots()

    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops={"edgecolor": "white"}
    )

    ax.axis("equal")

    st.pyplot(fig)

    plt.close(fig)

elif loan_amount > 0:

    # This handles zero-interest loans
    st.info(
        "The loan has no interest amount, so a pie chart cannot be displayed."
    )

else:

    # This prevents the 'All wedge sizes are zero' error
    st.info(
        "Enter a loan amount greater than ₹0 to view the loan breakdown."
    )
