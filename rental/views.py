from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Car, Rental
from datetime import datetime
from decimal import Decimal

# Create your views here.

def home(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'rental/home.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'rental/car_detail.html', {'car': car})

@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()
        days = (end_date - start_date).days + 1
        total_price = car.price_per_day * Decimal(days)
        
        rental = Rental.objects.create(
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
    rentals = Rental.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'rental/rental_history.html', {'rentals': rentals})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'rental/register.html', {'form': form})

def about(request):
    return render(request, 'rental/about.html')

def available_cars(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'rental/available_cars.html', {'cars': cars})

def locations(request):
    return render(request, 'rental/locations.html')
