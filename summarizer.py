import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_gpt(text, style="concise"):
    """Generate summary using OpenAI GPT."""
    prompt = f"Summarize this CE email thread in a {style} style (2–3 sentences). Focus on issue, resolution, and tone:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def suggest_actions(summary):
    """Return a list of suggested discrete actions."""
    prompt = f"""
    From this customer email summary, suggest 2-3 short, actionable steps.
    Keep each action under 2 words (e.g., 'Initiate refund', 'Request photos').
    The actions should be warehouse-related and easy to understand.
    
    Summary:
    {summary}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    actions_text = response.choices[0].message.content.strip()
    # Split into list by linebreak/dash
    actions = [a.strip(" -•") for a in actions_text.split("\n") if a.strip()]
    return actions[:3]