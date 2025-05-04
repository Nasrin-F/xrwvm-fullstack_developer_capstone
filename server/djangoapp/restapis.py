import os
import requests
from dotenv import load_dotenv
from django.http import JsonResponse

load_dotenv()

# Load backend and sentiment URLs from environment
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

print("BACKEND_URL is:", backend_url)  # Debugging: check if .env loads correctly


# ✅ Generic GET request to external service
def get_request(endpoint, **kwargs):
    request_url = backend_url + endpoint
    print(f"GET from: {request_url} | Params: {kwargs}")
    try:
        response = requests.get(request_url, params=kwargs)
        print("Status Code:", response.status_code)
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return None


# ✅ Add a review to the backend
def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    print("POST to:", request_url)
    try:
        response = requests.post(request_url, json=data_dict)
        print("Response JSON:", response.json())
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return None


# ✅ Analyze sentiment from a review using external analyzer
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    print("Analyzing Sentiment at:", request_url)
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print("Sentiment analysis error:", e)
        return {"sentiment": "unknown"}
