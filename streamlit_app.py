import streamlit as st
import pandas as pd
import math


st.title("Mortgage Calculator")

# Input fields for the user to enter data
col1, col2 = st.columns(2)
home_value = col1.number_input("Home Value ($):", min_value=0, value=400000, key="home_value")
down_payment = col1.number_input("Down Payment ($):", min_value=0, value=100000, key="payment")
interest_rate = col2.number_input("Annual Interest Rate (%):", min_value=0.0, value=6.5, key="interest")
loan_term = st.slider("Loan Term (Years):", min_value=1, max_value=30, value=15, key="term")

# Calculate payments
loan_amount = home_value - down_payment
monthly_interest_rate = interest_rate / 100 / 12
number_of_payments = loan_term * 12

# Calculate the monthly payment using the formula
if monthly_interest_rate > 0:
    monthly_payment = loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**number_of_payments / ((1 + monthly_interest_rate)**number_of_payments - 1)
else:
    monthly_payment = loan_amount / number_of_payments


balance = loan_amount
amortization_schedule = []

for i in range(1, number_of_payments + 1):
    interest_payment = balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    balance -= principal_payment
    amortization_schedule.append((i, balance, principal_payment, interest_payment))

months = [x[0] for x in amortization_schedule]
balances = [x[1] for x in amortization_schedule]
principals = [x[2] for x in amortization_schedule]
interests = [x[3] for x in amortization_schedule]

total_interest = sum(interests)
total_principal = sum(principals)
total_paid = total_interest + total_principal

col1, col2, col3 = st.columns(3)
with col1:
    st.write(f"Total Principal Paid: ${total_principal:.2f}")
with col2:
    st.write(f"Total Interest Paid: ${total_interest:.2f}")
with col3:
    st.write(f"Monthly Payment: ${monthly_payment:.2f}")

st.write(f"Total Amount Paid: ${total_paid:.2f}")

# Create a data-frame with the payment schedule.
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i/12) # calculate the year into the loan
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],  
)

st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df)

