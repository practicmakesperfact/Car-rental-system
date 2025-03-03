from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('A', 'Automatic'),
        ('M', 'Manual'),
    ]
    Location =models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model_year = models.IntegerField()
    transmission = models.CharField(max_length=1, choices=TRANSMISSION_CHOICES)
    seats = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cars/')
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)
    gps_tracking = models.BooleanField(default=False)
    description = models.TextField()
    latitude = models.FloatField( null=True, blank=True)  
    longitude = models.FloatField( null=True, blank=True)


    def __str__(self):
        return f"{self.brand} {self.name} ({self.model_year})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    loyality_points_earned =models.IntegerField(default=0)
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
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE,null= True, blank=True)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20,choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    
    def __str__(self):
        return f"Payment for {self.booking}"
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    
    def __str__(self):
        return self.name

    
class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.car.name}"
  
class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()
    
    def __str__(self):
        return f"{self.user.username} - {self.points} points"
    
