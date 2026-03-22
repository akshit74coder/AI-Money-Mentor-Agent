import streamlit as st
from agents import analyze_finances, generate_plan, money_health_score, explain_plan
from utils import format_currency

st.set_page_config(page_title="AI Money Mentor", layout="centered")

st.title("💰 AI Money Mentor")
st.write("Plan your finances smartly using AI 🚀")

# Inputs
income = st.number_input("Monthly Income (₹)", min_value=0)
expenses = st.number_input("Monthly Expenses (₹)", min_value=0)

if st.button("Generate Plan"):

    if income == 0:
        st.error("Please enter your income")
    else:
        # Agent flow
        analysis = analyze_finances(income, expenses)
        plan = generate_plan(analysis)
        score = money_health_score(analysis["savings_rate"])

        # Display results
        st.subheader("📊 Analysis")
        st.write(f"Savings: {format_currency(analysis['savings'])}")
        st.write(f"Savings Rate: {analysis['savings_rate']:.2f}%")

        st.subheader("📈 Plan")
        st.write(f"SIP Investment: {format_currency(plan['sip'])}")
        st.write(f"Emergency Fund: {format_currency(plan['emergency'])}")
        st.write(f"Buffer: {format_currency(plan['buffer'])}")

        st.subheader("💯 Money Health Score")
        st.progress(score)
        st.write(f"Score: {score}/100")

        # AI explanation
        with st.spinner("AI is generating advice..."):
            explanation = explain_plan(income, expenses, plan, score)

        st.subheader("🤖 AI Advice")
        st.write(explanation)
