from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Airport, Flight, Person
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.paginator import Paginator

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "flights/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "flights/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "flights/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "flights/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flights/register.html")

@login_required(login_url='/login')
def index(request):
    flights = Flight.objects.all().order_by('id').reverse()
    paginator = Paginator(flights, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'flights': flights,
        'page_obj':page_obj
    }
    return render(request, "flights/index.html", context)

@login_required(login_url='/login')
def flight_view(request, id):
    flight = get_object_or_404(Flight, id=id)
    context = {
        'flight':flight
    }
    return render(request, "flights/flight.html", context)

@login_required(login_url='/login')
def airport_view(request, code):
    airport = get_object_or_404(Airport, code=code)
    flights = Flight.objects.filter(Q(origin=airport) | Q(destination=airport)).order_by('id').reverse()
    paginator = Paginator(flights, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'airport':airport,
        'flights':flights,
        'page_obj':page_obj
    }
    return render(request, "flights/airport.html", context)

@login_required(login_url='/login')
def all_airports(request):
    airports = Airport.objects.all().order_by('name')
    paginator = Paginator(airports, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'airports':airports,
        'page_obj':page_obj
    }
    return render(request, "flights/airports.html", context)

@login_required(login_url='/login')
def book(request, id):
    flight = get_object_or_404(Flight, id=id)
    user = request.user
    if request.method == "POST":
        try:
            person = get_object_or_404(Person, user=user)
            person.flights.add(flight)
            flight.passengers.add(user)
            return redirect('index')
        except:
            person = Person.objects.create(user=user)
            person.flights.add(flight)
            flight.passengers.add(user)
            return redirect('index')
    else:
        return render(request, "flights/book.html", {
            'flight':flight
        })

@login_required(login_url='/login')
def cancel_book(request, id):
    flight = get_object_or_404(Flight, id=id)
    user = request.user
    if request.method == "POST":
        try:
            person = get_object_or_404(Person, user=user)
            person.flights.remove(flight)
            flight.passengers.remove(user)
            return redirect('index')
        except:
            return redirect('index')
    else:
        return render(request, "flights/cancel.html", {
            'flight':flight
        })

@login_required(login_url='/login')
def my_flights(request):
    flights = Flight.objects.filter(passengers=request.user).order_by('id').reverse()
    paginator = Paginator(flights, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'flights': flights,
        'page_obj':page_obj
    }
    return render(request, "flights/myflights.html", context)
