# *HealthConnect* 🏥💙  

HealthConnect is an AI-powered health assistant that provides symptom checking, mental health support , appointment scheduling and emergency assistance. It integrates *BioBERT* for symptom prediction, *Google Maps* for nearby healthcare facilities, *Google Calendar* for appointment scheduling, and *Firebase authentication* for user management.  

---

## *Features* 🚀  

✔️ *Symptom Checker* – Uses a fine-tuned *BioBERT* model to predict possible diseases based on symptoms.  
✔️ *Mental Health Chatbot* – Provides mental health support using AI-powered responses.    
✔️ *Emergency Assistance* – Locates the nearest healthcare facilities using *Google Maps API*.  
✔️ *Appointment Scheduling* – Integrates with *Google Calendar* to schedule medical appointments.  
✔️ *User Authentication* – Secure login and authentication with *Firebase*.  

---
## **Project Structure** 📂  

HealthConnect/ │ ├── app.py # Main Streamlit app (entry point) ├── requirements.txt # Python dependencies ├── firebase_credentials.json # Firebase Admin SDK credentials ├── google_credentials.json # Google API OAuth credentials │ ├── database/ │ └── healthconnect.db # SQLite database for hydration tracking │ ├── models/ │ ├── biobert_finetuned/ # Fine-tuned BioBERT model for symptom checking │ ├── tokenizer/ # Tokenizer for processing text inputs │ ├── utils/ │ ├── auth.py # Firebase authentication functions │ ├── google_maps.py # Google Maps API functions │ ├── google_calendar.py # Google Calendar API functions │ ├── symptom_checker.py # Symptom checker using BioBERT │ ├── sentiment_analysis.py # Sentiment analysis for mental health │ ├── hydration_tracker.py # Hydration tracking with SQLite │ ├── training/ │ ├── fine_tune.py # Script to fine-tune BioBERT │ ├── predict.py # Script to make predictions using the trained model │ ├── dataset/ # Symptom2Disease dataset for training │ └── .gitignore # Git ignore file

yaml
Copy
Edit

---

## **Setup & Installation** 🛠️  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/your-username/HealthConnect.git
cd HealthConnect
2️⃣ Install Dependencies
Make sure you have Python 3.8+ and install the required packages:

bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Set Up Firebase Authentication
Create a Firebase project on Firebase Console.
Enable Email/Password Authentication.
Download the firebase_credentials.json file and place it in the project root.
4️⃣ Configure Google API Services
Enable Google Maps API and Google Calendar API on Google Cloud Console.
Download the google_credentials.json file and place it in the project root.
5️⃣ Run the Application
bash
Copy
Edit
streamlit run app.py
