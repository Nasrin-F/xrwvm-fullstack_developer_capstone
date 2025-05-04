# views.py

from django.http import JsonResponse
from .restapis import get_request
import logging
from django.views.decorators.csrf import csrf_exempt


# Get an instance of a logger (optional, for debugging)
logger = logging.getLogger(__name__)

# Create your views here.
# Updated the `get_dealerships` to handle missing data and log the response.
def get_dealerships(request, state="All"):
    logger.info(f"Fetching dealers for state: {state}")

    # If the state is 'All', use the appropriate endpoint
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"

    # Fetch the dealer data from the external API
    dealerships = get_request(endpoint)
    
    if dealerships:
        logger.info(f"Dealerships fetched successfully: {len(dealerships)} dealers found")
        return JsonResponse({"status": 200, "dealers": dealerships})
    else:
        logger.error(f"No dealers found for state: {state}")
        return JsonResponse({"status": 500, "message": "No dealers found"})

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

# Function to get details for a specific dealer
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{str(dealer_id)}"
        dealership = get_request(endpoint)
        if dealership:
            logger.info(f"Dealer details fetched for dealer id {dealer_id}")
            return JsonResponse({"status": 200, "dealer": dealership})
        else:
            logger.error(f"Dealer with ID {dealer_id} not found.")
            return JsonResponse({"status": 404, "message": "Dealer not found"})
    else:
        logger.error("Bad Request: No dealer_id provided")
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Function to get reviews for a specific dealer
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{str(dealer_id)}"
        reviews = get_request(endpoint)
        
        if reviews:
            for review_detail in reviews:
                response = analyze_review_sentiments(review_detail['review'])
                review_detail['sentiment'] = response.get('sentiment', 'Unknown')
            
            logger.info(f"Reviews fetched for dealer {dealer_id}")
            return JsonResponse({"status": 200, "reviews": reviews})
        else:
            logger.error(f"No reviews found for dealer with ID {dealer_id}")
            return JsonResponse({"status": 404, "message": "Reviews not found"})
    else:
        logger.error("Bad Request: No dealer_id provided")
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Function to add a review
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            logger.info(f"Review posted successfully")
            return JsonResponse({"status": 200})
        except Exception as e:
            logger.error(f"Error in posting review: {str(e)}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        logger.error("Unauthorized user trying to post a review")
        return JsonResponse({"status": 403, "message": "Unauthorized"})
