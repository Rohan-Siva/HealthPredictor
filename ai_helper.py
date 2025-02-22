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
    try:
        # Get health data summary
        summary = get_health_data_summary(user_id)
        data = summary['latest'] if summary else None

        # Create a Gemini model instance
        model = genai.GenerativeModel('gemini-pro')

        # Create a chat instance with the system prompt
        chat = model.start_chat(history=[
            {
                "role": "user",
                "parts": [
                    "You are a helpful medical assistant. Provide accurate, cautious, and evidence-based information related to health metrics. "
                    "When asked about specific health metrics, check the provided health data and give clear answers about the values present. "
                    "If a value is not available or null, clearly state that. Always advise consulting healthcare professionals for personalized medical advice."
                ]
            },
            {
                "role": "model",
                "parts": [
                    "I understand. I will provide information about health metrics from the available data while emphasizing the importance of consulting healthcare professionals for personalized advice."
                ]
            }
        ])

        # Add user's health context if available
        if data:
            risk_score_text = "Not calculated"
            if data['risk_score'] is not None:
                risk_score_text = f"{data['risk_score'] * 100:.1f}%"

            context = {
                "role": "user",
                "parts": [
                    f"Here is the patient's latest health data:\n"
                    f"- Blood Pressure: {data['blood_pressure'] or 'Not recorded'} mmHg\n"
                    f"- Heart Rate: {data['heart_rate'] or 'Not recorded'} bpm\n"
                    f"- Body Temperature: {data['temperature'] or 'Not recorded'} °C\n"
                    f"- Weight: {data['weight'] or 'Not recorded'} kg\n"
                    f"- Risk Score: {risk_score_text} (represents the probability of developing heart disease)\n"
                    f"- Timestamp: {data['timestamp']}\n\n"
                    "When asked about specific metrics, reply with the actual values from this data if available."
                ]
            }
            chat.send_message(context)

        # Get response from the model
        response = chat.send_message(message)
        return response.text

    except Exception as e:
        return f"I apologize, but I'm unable to process your request at the moment. Please try again later. Error: {str(e)}"