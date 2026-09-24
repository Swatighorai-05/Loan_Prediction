# 📊 Pie Chart for Loan Breakdown
if loan_amount > 0 or total_interest > 0:
    fig, ax = plt.subplots()

    labels = ["Principal amount", "Interest amount"]
    sizes = [loan_amount, total_interest]
    colors = ["#DCE3F3", "#4361EE"]

    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        wedgeprops={"edgecolor": "white"}
    )

    ax.axis("equal")
    st.pyplot(fig)
else:
    st.info("Enter a loan amount greater than ₹0 to view the loan breakdown.")
