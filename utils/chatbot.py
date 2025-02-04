from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Token limit to prevent exceeding model constraints
MAX_HISTORY_LENGTH = 5  # Keeps only the last 5 exchanges

def get_therapist_response(feelings, chat_history):
    """
    Generates a therapist-style response based on the user's feelings and chat history.

    Args:
        feelings (str): User's message describing their emotions.
        chat_history (list): Previous conversation history.

    Returns:
        str: AI-generated response or fallback message in case of content restrictions.
    """

    prompt = """
    You are a compassionate therapist. Your goal is to provide empathetic responses based on the user's feelings.
    Acknowledge their emotions, provide comfort, and suggest mental exercises or activities that could help them feel better.
    Maintain a conversational tone and remember the previous context to offer better responses.
    Keep responses natural, flowing, and engaging in a multi-turn conversation.
    Structure the response as follows:
    - Acknowledge the user's feelings empathetically.
    - Provide advice or perspective on dealing with these feelings.
    - Offer one or two simple mental exercises or activities to improve their mental state.
    Return the response using markdown.
    """

    # Keep only the last few exchanges to avoid exceeding token limits
    limited_chat_history = chat_history[-MAX_HISTORY_LENGTH:]
    full_chat_context = limited_chat_history + ["User: " + feelings]

    model = genai.GenerativeModel('gemini-pro')

    try:
        response = model.generate_content([prompt] + full_chat_context)

        # If no valid response, handle it gracefully
        if not response.candidates or response.candidates[0].finish_reason == 3:
            raise ValueError("AI detected potentially unsafe content.")

        return response.text.replace("Empathetic Acknowledgment:", "").replace("Advice and Perspective:", "").replace("Mental Exercises and Activities:", "")

    except ValueError:
        return "I'm here to support you. If you're struggling, please consider seeking professional help. You're not alone. 💙"