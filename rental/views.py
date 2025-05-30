import requests
import uuid
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.conf import settings
from django.http import HttpResponse
from django.db import IntegrityError
from django.core.files.storage import default_storage
from django.conf import settings
from .models import Car, Booking, CustomProfile, Reward,Payment
from .forms import BookingForm, ReviewForm,CustomUserCreationForm
from .utils import update_car_location,apply_loyalty_discount
from .utils import extract_text_from_image, extract_name_from_text
from datetime import datetime
from decimal import Decimal


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email']
# Create your views here.
@login_required
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
@login_required
def services(request):
    return render(request,'rental/services.html')

@login_required
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
        
        #ensure valid dates selections
        if start_date >=end_date:
            return render(request,'rental/booking_car.html',{
                'car':car,
                'error_message': 'Invalid date selection. End date must be after start date.'
            })
        days = (end_date - start_date).days + 1
        total_price = car.price_per_day * Decimal(days)
        
        Booking.objects.create(
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
    return render(request, 'rental/book_car.html', {'car': car,})

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


@login_required
def track_car(request,car_id):
    """
    calls the utility functions to fetch GPS  data and display car location.
    """
    success = update_car_location(car_id)
    car = Car.objects.get(id=car_id)
    return render(request, 'track_car.html',{'car':car, 'success':success})
    
@login_required
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
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            id_front = form.cleaned_data['id_front_image']
            id_back = form.cleaned_data['id_back_image']

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return render(request, 'rental/register.html', {'form': form})

            try:
                user = form.save(commit=False)
                user.username = email
                user.email = email
                user.first_name = full_name
                user.is_active = False  # Until email verification
                user.save()

                # Check if a profile already exists for this user (shouldn't, but just in case)
                if CustomProfile.objects.filter(user=user).exists():
                    messages.error(request, "A profile already exists for this user(use other image) . or Please login.")
                    user.delete()
                    return render(request, 'rental/register.html', {'form': form})

                # (Optional) Check if ID images already exist based on filename
                if default_storage.exists(f'id_images/front/{id_front.name}') or default_storage.exists(f'id_images/back/{id_back.name}'):
                    messages.error(request, "An ID image with the same name already exists. Please rename your file and try again.")
                    user.delete()
                    return render(request, 'rental/register.html', {'form': form})

                # Create profile
                profile = CustomProfile.objects.create(
                    user=user,
                    phone_number=form.cleaned_data['phone_number'],
                    address=form.cleaned_data['address'],
                    id_front_image=id_front,
                    id_back_image=id_back,
                )

                # OCR processing
                front_text = extract_text_from_image(profile.id_front_image.path)
                back_text = extract_text_from_image(profile.id_back_image.path)
                extracted_name = extract_name_from_text(front_text) or extract_name_from_text(back_text)

                if not extracted_name:
                    messages.error(request, "Could not extract name from ID images.")
                    user.delete()
                    return render(request, 'rental/register.html', {'form': form})

                if extracted_name.lower() == full_name.lower():
                    profile.extracted_name = extracted_name
                    profile.save()
                    messages.success(request, "Registration successful! Please verify your email.")
                    return redirect('login')
                else:
                    messages.error(request, "The name on the ID does not match the entered name.")
                    user.delete()
                    return render(request, 'rental/register.html', {'form': form})

            except IntegrityError:
                messages.error(request, "Something went wrong. Please try again.")
                return render(request, 'rental/register.html', {'form': form})

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'rental/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'rental/login.html')
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def about(request):
    return render(request, 'rental/about.html')
@login_required
def car_list(request):
    """
    Displays a list of available cars with search functionality.
    """
    cars = Car.objects.filter(is_available=True)
    search_query = request.GET.get('search', '').strip()
    if search_query:
        cars = cars.filter(name__icontains=search_query)
    return render(request, 'rental/car_list.html', {'cars': cars, 'search_query': search_query})

@login_required
def car_detail(request, car_id):
    """
    displays a ditail information about a spacific car
    """
    car = get_object_or_404(Car, id=car_id)
    # provide a default image if none is uploaded 
    if not car.image:
        car.image = 'images/default_car_image.jpg'
    return render(request, 'rental/car_detail.html', {'car': car})
@login_required
def locations(request):
    return render(request, 'rental/locations.html')

@login_required
def profile(request):
    profile = get_object_or_404(CustomProfile, user=request.user)
    return render(request, 'rental/profile.html', {'profile': profile})



@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('rental_history')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'rental/update_profile.html', {'form': form})

# Payment Processing

CHAPA_BASE_URL = "https://api.chapa.co/v1/transaction/initialize"

def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    amount = booking.total_price

    payload = {
        'amount': str(amount),
        'currency': 'ETB',
        'email': request.user.email,
        # 'tx_ref': request.user.email,
        'tx_ref': f"car_rental_{booking.id}_{uuid.uuid4().hex[:8]}",
        'callback_url': request.build_absolute_uri("/payment/verify/"),
        'return_url': request.build_absolute_uri("/payment/success/"),
        'customization': {
            'title': 'Car Rental Pay',
            'description': f'Payment for booking ID {booking.id}',
        }
    }

    headers = {'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}', 'Content-Type': 'application/json'}
    response = requests.post(CHAPA_BASE_URL, json=payload, headers=headers)
  
    response_data = response.json()

    if response.status_code != 200 or response_data.get('status') != 'success':
        messages.error(request, 'Failed to process payment. Please try again.')
        return redirect('rental_history')
    
@login_required
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status != "Pending" or booking.payment_status != "Unpaid":
        messages.error(request, "This booking is not eligible for payment.")
        return redirect("rental_history")

    # Validate total_price
    if booking.total_price <= 0:
        messages.error(request, "Invalid booking amount. Total price must be greater than 0.")
        return redirect("rental_history")

    # Validate email
    if not request.user.email:
        messages.error(request, "User email is required for payment. Please update your profile.")
        return redirect("rental_history")

    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            "amount": booking.total_price,
            "payment_method": "Chapa",
            "status": "Pending",
            "transaction_id": f"car_rental_{booking.id}_{uuid.uuid4().hex[:8]}"
        }
    )

    payload = {
        "amount": str(booking.total_price),
        "currency": "ETB", 
        "email": request.user.email,
        "first_name": request.user.first_name or "User",
        "last_name": request.user.last_name or "",
        "tx_ref": payment.transaction_id,
        "callback_url": request.build_absolute_uri("/payment/verify/"),
        "return_url": request.build_absolute_uri("/payment/success/"),
        "customization": {
            "title": "Car Rental Pay",
            "description": f"Payment for booking ID  {booking.id}",
        }
    }

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.chapa.co/v1/transaction/initialize", json=payload, headers=headers)
        response_data = response.json()
        print("Chapa Response:", response_data)
    except requests.exceptions.RequestException as e:
        print("Request Exception:", str(e))
        payment.status = "Failed"
        payment.save()
        booking.payment_status = "Failed"
        booking.status = "Rejected"
        booking.car.is_available = True
        booking.car.save()
        booking.save()
        messages.error(request, "Payment initiation failed due to a network error. Please try again.")
        return redirect("rental_history")

    if response_data.get("status") == "success":
        return redirect(response_data["data"]["checkout_url"])
    else:
        print("Chapa Error Details:", response_data)
        payment.status = "Failed"
        payment.save()
        booking.payment_status = "Failed"
        booking.status = "Rejected"
        booking.car.is_available = True
        booking.car.save()
        booking.save()
        messages.error(request, f"Payment initiation failed: {response_data.get('message', 'Unknown error')}")
        return redirect("rental_history")
    
@login_required
def verify_payment(request):
    tx_ref = request.GET.get("tx_ref")
    if not tx_ref:
        messages.error(request, "Invalid payment verification request.")
        return redirect("payment_fail")

    try:
        payment = Payment.objects.get(transaction_id=tx_ref)
        booking = payment.booking

        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        verify_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
        response = requests.get(verify_url, headers=headers)
        response_data = response.json()

        if response_data.get("status") == "success":
            payment.status = "Completed" # Payment is confirmed by Chapa
            payment.save()
            booking.payment_status = "Paid" # Payment is marked as paid
            booking.status = "pending Admin Approval" # Set intermediate state
            booking.save()
            messages.success(request, "Payment successful! Your booking is waiting for admin confirmation.")
            return redirect("payment_status")
        else:
            payment.status = "Failed"
            payment.save()
            booking.payment_status = "Failed"
            booking.status = "Rejected"
            booking.car.is_available = True
            booking.car.save()
            booking.save()
            messages.error(request, "Payment failed. Please try again.")
            return redirect("payment_fail")

    except Payment.DoesNotExist:
        messages.error(request, "Payment not found.")
        return redirect("payment_fail")

@login_required
def payment_status(request):
    return render(request, "rental/payment_status.html")

@login_required
def payment_fail(request):
    return render(request, "rental/payment_fail.html")

@login_required
def terms(request):
    return render(request, 'rental/terms.html')
@login_required
def privacy(request):
    return render(request, 'rental/privacy.html')
@login_required
def faqs(request):
    return render(request, 'rental/faqs.html')
@login_required
def support(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Basic validation (you can expand this)
        if name and email and message:
            messages.success(request, 'Thank you for your message! Our team will get back to you soon.')
            return redirect('support')
        else:
            messages.error(request, 'Please fill out all fields correctly.')
            return redirect('support')

    return render(request, 'rental/support.html',{
        'TAWK_TO_WIDGET_ID': settings.TAWK_TO_WIDGET_ID
    }) 