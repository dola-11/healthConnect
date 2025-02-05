import os
import json
import numpy as np
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from utils import auth  # Assuming Firebase Auth utility is in the utils folder

# Define paths for the model and tokenizer
MODEL_PATH = "/Users/apple/Desktop/healthConnect/model/Model_with_Tokenizer/model"  # Path to the directory containing the model and tokenizer

# Load the trained model and tokenizer
model = tf.saved_model.load('/Users/apple/Desktop/healthConnect/model/Model_with_Tokenizer/model/')

# Load tokenizer
MODEL_NAME = "dmis-lab/biobert-base-cased-v1.1"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)  # Tokenizer is also in the same directory

# Disease label mappings 
label2int = {
    'Psoriasis': 0,
    'Varicose Veins': 1,
    'Typhoid': 2,
    'Chicken pox': 3,
    'Impetigo': 4,
    'Dengue': 5,
    'Fungal infection': 6,
    'Common Cold': 7,
    'Pneumonia': 8,
    'Dimorphic Hemorrhoids': 9,
    'Arthritis': 10,
    'Acne': 11,
    'Bronchial Asthma': 12,
    'Hypertension': 13,
    'Migraine': 14,
    'Cervical spondylosis': 15,
    'Jaundice': 16,
    'Malaria': 17,
    'Urinary tract infection': 18,
    'Allergy': 19,
    'Gastroesophageal reflux disease': 20,
    'Drug reaction': 21,
    'Peptic ulcer disease': 22,
    'Diabetes': 23
}

int2label = {v: k for k, v in label2int.items()}

# Maximum length for input text
MAX_LENGTH = 512


def predict_diseases(symptoms: str):
    """
    Function to get disease prediction based on user input symptoms.
    
    Parameters:
    - symptoms (str): A string containing the user's symptoms.

    Returns:
    - (dict): A dictionary with predicted disease and its confidence score.
    """
    

    # Assuming 'output' is your TFSequenceClassifierOutput object
    symptoms = tokenizer(symptoms, return_tensors="tf", padding=True, truncation=True, max_length=512)
    output = model(symptoms)
    logits = output["logits"]

    # Apply softmax to get probabilities
    probabilities = tf.nn.softmax(logits, axis=-1)

    # Get the top N class indices and their probabilities
    top_n = 3  # Set N to the desired number of top results
    top_n_indices = tf.argsort(probabilities, axis=-1, direction='DESCENDING')[:, :top_n]
    top_n_probs = tf.gather(probabilities, top_n_indices, batch_dims=1)

    # Convert to numpy for easy manipulation (if needed)
    top_n_indices = top_n_indices.numpy()[0]
    top_n_probs = top_n_probs.numpy()[0]

    

    return [(int2label[pred], probab) for pred, probab in zip(top_n_indices, top_n_probs)]
