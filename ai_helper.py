import google.generativeai as genai
import os
from dotenv import load_dotenv
from healthutils import get_health_data_summary

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'),
                transport="rest",
                client_options={"api_endpoint": "generativelanguage.googleapis.com"})

def get_chatbot_response(message, user_id):
    summary = get_health_data_summary(user_id)
    data = summary['latest']
    
    try:
        # Create a Gemini model instance
        model = genai.GenerativeModel('gemini-pro')

        # Create a chat instance with the system prompt
        chat = model.start_chat(history=[
    {
        "role": "user",
        "parts": [
            "You are a helpful medical assistant. Provide accurate, cautious, and evidence-based information related to heart disease risks. Always advise consulting healthcare professionals for personalized medical advice."
        ]
    },
    {
        "role": "model",
        "parts": [
            "I understand. I will provide general health information about heart disease while emphasizing the importance of consulting healthcare professionals for personalized advice."
        ]
    },
    {
        "role": "user",
        "parts": [
            f"Here is the patient's latest health data:\n"
            f"- Blood Pressure: {data['blood_pressure']} mmHg\n"
            f"- Heart Rate: {data['heart_rate']} bpm\n"
            f"- Body Temperature: {data['temperature']} °C\n"
            f"- Weight: {data['weight']} kg\n"
            f"- Risk Score: {data['risk_score']}% (represents the probability of developing heart disease)\n"
            f"- Timestamp: {data['timestamp']}\n\n"
            "Based on this information, provide general insights on potential heart disease risks and answer their queries."
        ]
    }
])


        # Get response from the model
        response = chat.send_message(message)
        return response.text

    except Exception as e:
        return f"I apologize, but I'm unable to process your request at the moment. Please try again later. Error: {str(e)}"