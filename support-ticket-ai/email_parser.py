from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_support_email(email_text): 
    prompt = f"""
    You are a support ticket analyzer. Read the following support email 
    and extract key information.
    
    Email:
    {email_text}
    
    Extract and return ONLY a JSON object with these fields:
    - issue_type: (e.g., "Login Issue", "Performance", "Bug", "Feature Request")
    - severity: ("Low", "Medium", "High", "Critical")
    - user_email: (if mentioned, otherwise "Not provided")
    - error_message: (exact error if mentioned, otherwise "None")
    - summary: (one sentence description)
    - keywords: (list of relevant technical terms)
    
    Return ONLY the JSON, no other text.
    """

    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "you are a helpful support ticket analyzer"},
                {"role": "user", "content": prompt}
            ],
            temperature=0
    )

    result = response.choices[0].message.content

    ticket_data = json.loads(result)

    return ticket_data

if __name__ == "__main__":
    sample_email = """
    Subject: Can't login to dashboard
    
    Hi, I've been trying to access my account for the past hour but keep 
    getting "Invalid credentials" error. My username is john.doe@company.com. 
    This is urgent as I need to generate reports for today's meeting.
    """
    print("Analyzing email...")
    ticket = parse_support_email(sample_email)
    print("Extracted ticket Information")
    print(json.dumps(ticket, indent=2))

