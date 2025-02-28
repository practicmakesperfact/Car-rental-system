from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('A', 'Automatic'),
        ('M', 'Manual'),
    ]
    
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model_year = models.IntegerField()
    transmission = models.CharField(max_length=1, choices=TRANSMISSION_CHOICES)
    seats = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cars/')
    is_available = models.BooleanField(default=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.brand} {self.name} ({self.model_year})"

class Rental(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
        ('C', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.car.name} ({self.start_date} to {self.end_date})"
class CustomProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    def __str__(self):
        return self.user.username

class Payment(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Payment for {self.rental}"
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    
    def __str__(self):
        return self.name
    
class Review(models.Model):
    Car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Review by {self.user.username} for {self.Car.name}"
  