import os
import google.generativeai as genai

# Get API key from Streamlit Secrets
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if api_key:
    genai.configure(api_key=api_key)
else:
    print("API key not found")

# Agent 1: Analysis
def analyze_finances(income, expenses):
    savings = income - expenses
    savings_rate = (savings / income) * 100 if income > 0 else 0

    return {
        "savings": savings,
        "savings_rate": savings_rate
    }

# Agent 2: Planning
def generate_plan(data):
    savings = data["savings"]

    sip = savings * 0.3
    emergency = savings * 0.2
    buffer = savings * 0.5

    return {
        "sip": sip,
        "emergency": emergency,
        "buffer": buffer
    }

# Agent 3: Score
def money_health_score(savings_rate):
    if savings_rate > 40:
        return 90
    elif savings_rate > 25:
        return 75
    elif savings_rate > 10:
        return 60
    else:
        return 40

# Agent 4: AI Explanation
def explain_plan(income, expenses, plan, score):

    if not api_key:
        return "Error: API key not found in Streamlit secrets"

    prompt = f"""
    User Income: {income}
    Expenses: {expenses}

    Suggested Plan:
    SIP: {plan['sip']}
    Emergency Fund: {plan['emergency']}
    Buffer: {plan['buffer']}

    Score: {score}

    Explain this in simple Hinglish like a financial advisor.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"
