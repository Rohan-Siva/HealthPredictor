import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
openai = OpenAI(api_key="")

def get_chatbot_response(message):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful medical assistant. Provide accurate but cautious medical information. Always advise consulting healthcare professionals for specific medical advice."
                },
                {"role": "user", "content": message}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I'm unable to process your request at the moment. Please try again later. Error: {str(e)}"
