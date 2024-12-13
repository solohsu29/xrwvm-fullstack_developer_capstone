from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create a `login_user` view to handle sign-in requests
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                return JsonResponse({"userName": username, "status": "Invalid credentials"}, status=401)
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return JsonResponse({"error": "Something went wrong."}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)

# Create a `logout_request` view to handle sign-out requests
def logout_request(request):
    logout(request)
    return JsonResponse({"userName": "", "status": "Logged out"})

# Create a `registration` view to handle sign-up requests
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')

            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"}, status=400)

            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email
            )
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        except Exception as e:
            logger.error(f"Error during registration: {e}")
            return JsonResponse({"error": "Something went wrong."}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)

# Create a `get_cars` view to return a list of cars
def get_cars(request):
    try:
        if CarMake.objects.count() == 0:
            initiate()

        car_models = CarModel.objects.select_related('car_make')
        cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name} for car_model in car_models]
        return JsonResponse({"CarModels": cars})
    except Exception as e:
        logger.error(f"Error fetching cars: {e}")
        return JsonResponse({"error": "Unable to fetch cars."}, status=500)

# Create a `get_dealerships` view to return a list of dealerships
def get_dealerships(request, state="All"):
    try:
        endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
        dealerships = get_request(endpoint)
        return JsonResponse({"status": 200, "dealers": dealerships})
    except Exception as e:
        logger.error(f"Error fetching dealerships: {e}")
        return JsonResponse({"error": "Unable to fetch dealerships."}, status=500)

# Create a `get_dealer_details` view to return dealer details
def get_dealer_details(request, dealer_id):
    try:
        if dealer_id:
            endpoint = f"/fetchDealer/{dealer_id}"
            dealership = get_request(endpoint)
            return JsonResponse({"status": 200, "dealer": dealership})
        return JsonResponse({"status": 400, "message": "Bad Request"})
    except Exception as e:
        logger.error(f"Error fetching dealer details: {e}")
        return JsonResponse({"error": "Unable to fetch dealer details."}, status=500)

# Create a `get_dealer_reviews` view to return reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    try:
        if dealer_id:
            endpoint = f"/fetchReviews/dealer/{dealer_id}"
            reviews = get_request(endpoint)
            for review_detail in reviews:
                response = analyze_review_sentiments(review_detail['review'])
                review_detail['sentiment'] = response.get('sentiment', "Unknown")
            return JsonResponse({"status": 200, "reviews": reviews})
        return JsonResponse({"status": 400, "message": "Bad Request"})
    except Exception as e:
        logger.error(f"Error fetching dealer reviews: {e}")
        return JsonResponse({"error": "Unable to fetch reviews."}, status=500)

# Create an `add_review` view to submit a review
def add_review(request):
    if request.method == "POST" and not request.user.is_anonymous:
        try:
            data = json.loads(request.body)
            post_review(data)
            return JsonResponse({"status": 200, "message": "Review submitted successfully."})
        except Exception as e:
            logger.error(f"Error posting review: {e}")
            return JsonResponse({"status": 401, "message": "Error in posting review."})
    return JsonResponse({"status": 403, "message": "Unauthorized or invalid request."}, status=403)
