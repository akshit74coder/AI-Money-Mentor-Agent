import os
from google import genai

# Initialize client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


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

    if not os.getenv("GEMINI_API_KEY"):
        return "Error: API key not found"

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
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"
