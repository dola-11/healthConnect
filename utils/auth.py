import firebase_admin
from firebase_admin import credentials, auth

def initialize_firebase():
    """Initialize Firebase Admin SDK if not already initialized."""
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_credentials.json")
        firebase_admin.initialize_app(cred)

def sign_up(email, password):
    """Register a new user with Firebase Authentication."""
    try:
        user = auth.create_user(email=email, password=password)
        return {"success": True, "message": f"User {email} created successfully!", "uid": user.uid}
    except firebase_admin.exceptions.FirebaseError as e:
        return {"success": False, "message": f"Error: {str(e)}"}

def login(email, password):
    """Simulate user login. Firebase Admin SDK does not support password verification."""
    try:
        user = auth.get_user_by_email(email)
        return {"uid": user.uid}
    except firebase_admin.exceptions.FirebaseError:
        return None

def is_user_logged_in():
    """Check if the user is logged in by checking session state."""
    return "user_id" in st.session_state and st.session_state["user_id"] is not None