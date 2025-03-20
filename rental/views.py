from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Car, Booking, CustomProfile, Reward
from .forms import BookingForm, ReviewForm
from datetime import datetime
from decimal import Decimal
from .utils import update_car_location,apply_loyalty_discount

# Create your views here.

def home(request):
    # get 10 featured products in the home page
    featured_cars = Car.objects.filter(is_available = True).order_by('-id')[:9]
    
    #featch cars by category for services 
    tour_cars = Car.objects.filter(category='tour-package', is_available=True)[:5]
    airport_cars = Car.objects.filter(category='airport-transfer', is_available=True)[:5]
    wedding_cars = Car.objects.filter(category='wedding_cars', is_available=True)[:5]  
    corporate_cars = Car.objects.filter(category='corporate-rentals', is_available=True)[:5]
    context = {
        'featured_cars': featured_cars,
        'tour_cars': tour_cars,
        'airport_cars': airport_cars,
        'wedding_cars': wedding_cars,
        'corporate_cars': corporate_cars,
    
    }
    return render(request, 'rental/home.html',context)

def services(request):
    return render(request,'rental/services.html')
def rental_list(request, category):
    """
    display list of cars in a specific category
    """
    CATEGORY_MAP = {
        'tour-package': 'tour-package',
        'airport-transfer': 'airport-transfer',
        'wedding-cars': 'wedding-cars',  
        'corporate-rentals': 'corporate-rentals',
    }
    mapped_category = CATEGORY_MAP.get(category,category)
    cars= Car.objects.filter(category=mapped_category, is_available=True)
    print(f"DEBUG: Category - {category}, Cars found - {cars.count()}") 
    return render(request, 'rental/rental_list.html', {'cars': cars, 'category': category})


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

def add_review(request,car_id):
    """
    allow users to add  a review for a car they have rented 
    """
    car = get_object_or_404(Car,id=car_id)
    
    #ensure user has booked this car before reviewing
    has_rented = Booking.objects.filter(user = request.user, car=car, status= 'Completed').exists()
    
      
    if not has_rented:
        messages.error(request, 'You must rent this car before you can review it.')
        return redirect('rental_history')
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.car = car
            review.save()
            car.update_rating()
            messages.success(request, 'Review submitted successfully!')
            return redirect('car_detail', car_id=car.id)
        else:
            print('Invalid form, re-rendering page')
      # return the review from if get request
    form = ReviewForm()
    return render(request, 'rental/add_review.html', {'form': form, 'car': car})
        
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

    
@login_required
def user_rewards(request):
    """displays the logged user's reward points"""
    reward,created = Reward.objects.get_or_create(user=request.user)
    return render(request,"rental/user_rewards.html",{'reward':reward})    

@login_required
def redeem_rewards(request):
    """allow users to redeem reward points for a booking discount for next booking."""
    reward, created = Reward.objects.get_or_create(user=request.user)
    discount =  reward.redeem_points()
    if discount > 0:
        messages.success(request,  f"You redeemed points a ${discount} discount on your next booking.")
    else:
        messages.error(request, "You don't have enough points to redeem. you need at least 100 points.")
    return redirect('user_rewards')
        
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
    # provide a default image if none is uploaded 
    if not car.image:
        car.image = 'images/default_car_image.jpg'
    return render(request, 'rental/car_detail.html', {'car': car})

def locations(request):
    return render(request, 'rental/locations.html')

@login_required
def profile(request):
    profile = get_object_or_404(CustomProfile, user=request.user)
    return render(request, 'rental/profile.html', {'profile': profile})