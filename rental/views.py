from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Car, Booking, CustomProfile
from .forms import BookingForm, ReviewForm
from datetime import datetime
from decimal import Decimal
from .utils import update_car_location,apply_loyalty_discount

# Create your views here.

def home(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'rental/home.html', {'cars': cars})

@login_required
def book_car(request, car_id):
    """handles booking car"""
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()
        days = (end_date - start_date).days + 1
        total_price = car.price_per_day * Decimal(days)
        
        booking = Booking.objects.create(
            user=request.user,
            car=car,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price
        )
        car.is_available = False
        car.save()
        messages.success(request, 'Car booked successfully!')
        return redirect('rental_history')
    return render(request, 'rental/book_car.html', {'car': car})

@login_required
def rental_history(request):
    rentals = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'rental/rental_history.html', {'rentals': rentals})



def track_car(request,car_id):
    """
    calls the utility functions to fetch GPS  data and display car location.
    """
    success = update_car_location(car_id)
    car = Car.objects.get(id=car_id)
    return render(request, 'track_car.html',{'car':car, 'success':success})
    
    
    
def confirm_booking(request,booking_id):
    """confirms a booking and applies a loyalty discount if available"""
    booking = Booking.objects.get(id=booking_id)
    if request.method =='POST':
        total_price = apply_loyalty_discount(request.user,booking.total_price)
        booking.status = 'Confirmed'
        booking.save()
        return redirect('booking_success')
    return render(request,'confirm_booking.html',{'booking':booking})

    
        
    
    
def register(request):
    if request.method == 'POST':
       username = request.POST['username']
       email = request.POST['email']
       password = request.POST['password']
       user = User.objects.create_user(username=username, email=email, password=password)
       user.save()
       messages.success(request, 'Account created successfully! You can now login.')
       return redirect('login')
        
    return render(request, 'rental/register.html')
def user_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'rental/login.html')
def user_logout(request):
    logout(request)
    return redirect('home')

def about(request):
    return render(request, 'rental/about.html')

def car_list(request):
    """
    Displays a list of available cars with search functionality.
    """
    cars = Car.objects.filter(is_available=True)
    search_query = request.GET.get('search', '').strip()
    if search_query:
        cars = cars.filter(name__icontains=search_query)
    return render(request, 'rental/car_list.html', {'cars': cars, 'search_query': search_query})


def car_detail(request, car_id):
    """
    displays a ditail information about a spacific car
    """
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'rental/car_detail.html', {'car': car})

def locations(request):
    return render(request, 'rental/locations.html')

@login_required
def profile(request):
    profile = get_object_or_404(CustomProfile, user=request.user)
    return render(request, 'rental/profile.html', {'profile': profile})