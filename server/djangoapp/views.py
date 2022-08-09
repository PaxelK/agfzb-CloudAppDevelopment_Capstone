from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, Car, CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    
    return render(request, 'djangoapp/about.html', context)    


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    
    return render(request, 'djangoapp/contact.html', context)    

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if(request.method == "POST"):
        username = request.POST['username'] 
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)   

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')   

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}

    # If just a GET request, just render the registration page anew
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        
        #For POST-requests, do the following:
        #1. check if entered info already exists by using get on User object with username
        #2. If user does not exist, create a new user object and login
        #3. If user already exist, go render registration page anew
        
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}

    if request.method == "GET":
        # URL for the ibmcloud "get-dealerships" API endpoint 
        url = "https://d74e98ea.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context["dealerships"] = dealerships
        context["dealer_names"] = dealer_names
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)
    
    #return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    context = {}
    
    # Get dealer
    url = "https://d74e98ea.eu-gb.apigw.appdomain.cloud/api/dealership"
    dealer = get_dealer_by_id_from_cf(url, id)
    # Get reviews 
    url_reviews = "https://d74e98ea.eu-gb.apigw.appdomain.cloud/api/review"
    reviews = get_dealer_reviews_from_cf(url_reviews, id=id)

    context["dealer"] = dealer
    context["reviews"] = reviews
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, id):
    context = {}
    if request.method == 'GET':
        context["id"]=id
        return render(request, 'djangoapp/add_review.html', context)
    
    elif request.method == 'POST':
        url = "https://d74e98ea.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealer = get_dealer_by_id_from_cf(url, id)
        
        payload = {}

        payload["dealership"] = dealer["id"]
        payload["name"] = request.user.username
        payload["purchase"] = False
        if "purchased" in request.POST:
            if request.POST["purchased"] == 'on':
                payload["purchase"] = True
        payload["purchase_date"] = request.POST["purchase_date"]
        payload["car_make"] = request.POST["car_make"]
        payload["car_model"] = request.POST["car_model"]
        payload["car_year"] = request.POST["car_year"]
        payload["id"] = request.user.id
        payload["review"] = request.POST["review"]
        url = "https://d74e98ea.eu-gb.apigw.appdomain.cloud/api/review"

        result = post_request(url, payload)

        return redirect("djangoapp:dealer_details", id=id)

