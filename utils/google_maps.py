import googlemaps
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Google Maps API key from .env
google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")

# Function to get nearest healthcare facilities
def get_nearest_health_facility(location):
    gmaps = googlemaps.Client(key=google_maps_api_key)
    places = gmaps.places(query="healthcare near " + location)
    
    # Ensure there are results
    if 'results' in places:
        # Extract name and vicinity for each facility
        facilities = [{
            'name': place['name'],
            'vicinity': place.get('vicinity', 'Not available'),  # Using .get() to handle missing 'vicinity' key
            'formatted_address': place.get('formatted_address', 'Address not available')  # Fallback to 'formatted_address'
        } for place in places['results']]
        
        return facilities
    else:
        return []
