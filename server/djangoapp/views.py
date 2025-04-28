# Import necessary libraries and models
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from .models import CarMake, CarModel
import json
from django.views.decorators.csrf import csrf_exempt

# Get an instance of a logger (optional, for debugging)
import logging
logger = logging.getLogger(__name__)

# Create your views here.

# Login view to handle sign-in request
@csrf_exempt
def login_user(request):
    try:
        # Get username and password from request
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        
        # Try to authenticate the user with the provided credentials
        user = authenticate(username=username, password=password)
        response_data = {"userName": username}
        
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            response_data = {"userName": username, "status": "Authenticated"}
        else:
            response_data = {"userName": username, "status": "Authentication failed"}
        
        return JsonResponse(response_data)

    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        return JsonResponse({"error": "An error occurred during login."})

# Logout view to handle sign-out request
def logout_request(request):
    try:
        logout(request)  # Django's logout function clears the session
        return JsonResponse({"status": "Logged out successfully"})
    except Exception as e:
        logger.error(f"Logout failed: {str(e)}")
        return JsonResponse({"error": "An error occurred during logout."})

# Registration view to handle sign-up request
@csrf_exempt
def registration(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            email = data.get('email')
            
            # Check if the user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "User already exists"})
            
            # Create a new user
            user = User.objects.create_user(username=username, password=password, email=email)
            return JsonResponse({"status": "User registered successfully", "userName": username})
        else:
            return JsonResponse({"error": "Invalid request method"})
    
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")
        return JsonResponse({"error": "An error occurred during registration."})

# View to get the list of cars
def get_cars(request):
    try:
        # Check if there are any car makes in the database
        count = CarMake.objects.filter().count()
        logger.info(f"CarMake count: {count}")
        
        # If no car makes are present, you can call the 'initiate()' function to populate data (uncomment it if needed)
        if count == 0:
            # initiate()  # You should define this method to populate the database
            pass
        
        # Retrieve all car models and include the related car make information
        car_models = CarModel.objects.select_related('car_make')
        cars = []
        
        # Loop through each car model and append the details to a list
        for car_model in car_models:
            cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
        
        # Return the list of cars as a JSON response
        return JsonResponse({"CarModels": cars})
    
    except Exception as e:
        logger.error(f"Error retrieving cars: {str(e)}")
        return JsonResponse({"error": "An error occurred while fetching the car data."})
