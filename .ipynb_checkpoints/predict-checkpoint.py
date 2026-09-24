import pickle as pk
import pandas as pd

# Load model and scaler
model = pk.load(open("model.pkl", "rb"))
scaler = pk.load(open("scaler.pkl", "rb"))

def predict_loan(no_of_dep, grad_s, emp_s, Annual_Income, Loan_Amount, Loan_Dur, Cibil, Assets):
    pred_data = pd.DataFrame([[no_of_dep, grad_s, emp_s, Annual_Income, Loan_Amount, Loan_Dur, Cibil, Assets]],
                             columns=['no_of_dependents', 'education', 'self_employed', 'income_annum', 'loan_amount', 'loan_term', 'cibil_score', 'Assets'])
    pred_data = scaler.transform(pred_data)
    predict = model.predict(pred_data)

    return "Loan Is Approved" if predict[0] == 1 else "Loan Is Rejected"
