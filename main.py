import streamlit as st
from utils.auth import login, sign_up, is_user_logged_in, initialize_firebase
from utils.google_maps import get_nearest_health_facility
from utils.google_calendar import create_appointment
#from utils.sentiment_analysis import analyze_mood
from utils.hydration_tracker import store_hydration
from utils.symptom_checker import predict_diseases
from utils.chatbot import get_therapist_response  # Import the chatbot functionality

# Initialize Firebase
initialize_firebase()

# Streamlit UI
st.title("HealthConnect - Your AI-Powered Wellness Assistant")

# Firebase Authentication
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if not st.session_state["user_id"]:
    st.sidebar.header("Authentication")
    auth_choice = st.sidebar.radio("Choose an option", ["Login", "Sign Up"])

    if auth_choice == "Sign Up":
        st.subheader("Create a New Account")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Enter a password", type="password")
        if st.button("Sign Up"):
            if email and password:
                response = sign_up(email, password)
                if response["success"]:
                    st.success(response["message"])
                else:
                    st.error(response["message"])
            else:
                st.warning("Please provide both email and password.")

    elif auth_choice == "Login":
        st.subheader("Log In to Your Account")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        if st.button("Login"):
            user = login(email, password)
            if user:
                st.session_state["user_id"] = user["uid"]
                st.success("Login Successful!")
            else:
                st.error("Invalid email or password.")
else:
    st.sidebar.success(f"Logged in as: {st.session_state['user_id']}")

    # Add a chatbot toggle button in the sidebar
    chatbot_icon = st.sidebar.button("🧠 Chat with Therapist")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Check if chatbot is active
    if chatbot_icon:
        st.session_state["chatbot_active"] = True

    # Toggle to close the chatbot
    if "chatbot_active" in st.session_state and st.session_state["chatbot_active"]:
        st.sidebar.button("Close Chatbot", on_click=lambda: st.session_state.update({"chatbot_active": False}))

        # Chatbot UI
        st.title("🧠 AI Therapist Chatbot")
        st.write("### Share how you're feeling, and I'll provide ongoing support in a chat format.")

        # Display chat messages from history
        for message in st.session_state.chat_history:
            with st.chat_message("user"):
                st.markdown(message["user"])
            with st.chat_message("assistant"):
                st.markdown(message["assistant"])

        # User Input for chatbot
        user_input = st.chat_input("How are you feeling today?")

        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)

            # Get response from AI therapist with limited history for context
            chat_history_context = [f"User: {msg['user']}\nAI: {msg['assistant']}" for msg in st.session_state.chat_history]
            response = get_therapist_response(user_input, chat_history_context)

            with st.chat_message("assistant"):
                st.markdown(response)

            # Append to chat history and enforce token limit
            st.session_state.chat_history.append({"user": user_input, "assistant": response})
            st.session_state.chat_history = st.session_state.chat_history[-5:]  # Limit history to last 5 exchanges

    else:
        # Main app content when chatbot is not active
        # Symptom Checker
        st.header("Symptom Checker")
        symptoms_input = st.text_input("Enter your symptoms:")
        if symptoms_input:
            # Get predicted diseases based on the symptoms
            predicted_diseases = predict_diseases(symptoms_input)
            
            # Display the diseases and their confidence
            if predicted_diseases:
                st.write("### Predicted Diseases:")
                for disease, confidence in predicted_diseases:
                    st.write(f"- **{disease}**: {confidence:.2f}")
            else:
                st.write("Sorry, no diseases could be predicted based on the input.")

        # # Mental Health Support
        # st.header("Mental Health Support")
        # mood_input = st.text_area("How are you feeling today?")
        # if mood_input:
        #     mood_analysis = analyze_mood(mood_input)
        #     st.write(f"Sentiment: {mood_analysis['label']} (Confidence: {mood_analysis['score']})")
        #     if mood_analysis["label"] == "NEGATIVE":
        #         st.write("Consider practicing mindfulness or speaking to a counselor.")

        # # Hydration Tracking
        # st.header("Track Hydration")
        # glasses = st.number_input("Enter glasses of water consumed today:", min_value=0)
        # if st.button("Log Hydration"):
        #     store_hydration(st.session_state["user_id"], glasses)
        #     st.write(f"You’ve drunk {glasses} glasses of water today!")

        # Appointment Scheduling
        st.header("Schedule an Appointment")
        appointment_date = st.date_input("Choose Appointment Date")
        appointment_time = st.time_input("Choose Appointment Time")
        appointment_details = st.text_input("Appointment Details")
        if st.button("Schedule Appointment"):
            create_appointment(appointment_date, appointment_time, appointment_details)
            st.success("Appointment scheduled successfully!")

        # Emergency Assistance (Google Maps)
        st.header("Emergency Assistance")
        location = st.text_input("Enter your location (e.g., city):")

        if location:
            facilities = get_nearest_health_facility(location)
            
            if facilities:
                st.write("Nearby Healthcare Facilities:")
                for facility in facilities:
                    # Fallback to 'formatted_address' if 'vicinity' is not available
                    address = facility['vicinity'] if facility['vicinity'] != 'Not available' else facility['formatted_address']
                    st.write(f"- {facility['name']} at {address}")
            else:
                st.write("No healthcare facilities found nearby.")

    # Logout Option
    if st.sidebar.button("Logout"):
        st.session_state["user_id"] = None
        st.success("Logged out successfully!")