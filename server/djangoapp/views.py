# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    try:
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        data = {"userName": username}
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    except Exception as e:
        logger.error("Login error: {}".format(e))
        return JsonResponse({"status": "Failed", "error": str(e)}, status=400)
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except:
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        login(request, user)
        return JsonResponse({"userName":username,"status":"Authenticated"})
    else :
        return JsonResponse({"userName":username,"error":"Already Registered"})

# Create an `about` view to render a static page
def about(request):
    return render(request, 'About.html')

# Create a `contact` view to render a static page
def contact(request):
    return render(request, 'Contact.html')

# # Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

# Create a `add_review` view to submit a review
def add_review(request):
    if(request.user.is_authenticated == False):
        return JsonResponse({"status":403,"message":"Unauthorized"})
    data = json.loads(request.body)
    try:
        response = post_review(data)
        return JsonResponse({"status":200})
    except:
        return JsonResponse({"status":401,"message":"Error in posting review"})

# Create a `get_cars` view to return all car makes and models
def get_cars(request):
    from .models import CarMake, CarModel
    count = CarMake.objects.filter().count()
    if(count == 0):
        # Seed some data if empty
        make1 = CarMake.objects.create(name="Toyota", description="Japanese Car")
        make2 = CarMake.objects.create(name="Ford", description="American Car")
        CarModel.objects.create(name="Camry", car_make=make1, type="Sedan", year=2023)
        CarModel.objects.create(name="F-150", car_make=make2, type="Truck", year=2023)
        
    car_models = CarModel.objects.select_related('car_make').all()
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})
