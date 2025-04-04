from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone


# Create your models here.

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('A', 'Automatic'),
        ('M', 'Manual'),
    ]
    
    CATEGORY_CHOICES = [
        ('tour-package', 'Tour Package'),
        ('airport-transfer', 'Airport Transfer'),
        ('wedding-cars', 'Wedding Cars'),
        ('corporate-rentals', 'Corporate Rentals'),
    ]
    
    Location =models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model_year = models.IntegerField()
    transmission = models.CharField(max_length=1, choices=TRANSMISSION_CHOICES)
    seats = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)
    gps_tracking = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField( null=True, blank=True)  
    longitude = models.FloatField( null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='tour-package')
    
    def update_rating(self):
        """update the cars average rating."""
        self.rating = Review.calculate_average_rating(self)
        self.save()
    
    def get_category_display_name(self):
        """return the human readable name for the category"""
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
    def __str__(self):
        return f"{self.brand} {self.name} ({self.model_year})-{self.get_category_display_name()}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('pending Admin Approval', 'Pending Admin Approval'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    PAYMENT_STATUS_CHOICES =[
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Unpaid')
    loyality_points_earned =models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)   
    
    def save(self, *args, **kwargs):
        """ 
        calculate total price, available discount and loyalty points before saving the booking
        """
        if self.start_date and self.end_date:
            days =(self.end_date - self.start_date).days
            self.total_price = days *self.car.price_per_day
            #apply discount if available in the rewards model 
            reward, created = Reward.objects.get_or_create(user=self.user)
            discount =reward.use_discount()
            self.total_price = max(0,self.total_price - discount)
            # calculate loyalty points (1 per $100 spent)
            self.loyality_points_earned = int(self.total_price // 100)
            super().save(*args, **kwargs)
               
    def __str__(self):
        return f"{self.user.username} - {self.car.name} ({self.start_date} to {self.end_date})"
class CustomProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    id_front = models.ImageField(upload_to='id_documents/',null=True, blank=False)
    id_back = models.ImageField(upload_to='id_documents/',null=True, blank=False)
    def __str__(self):
        return self.user.username

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE,null= True, blank=True)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100, choices=[('Chapa', 'Chapa')], default='Chapa')
    transaction_id = models.CharField(max_length=100,unique=True, null=True, blank=True)
    status = models.CharField(max_length=20,choices=[('Pending', 'Pending'), ('Completed', 'Completed'),('Failed', 'Failed')],default='Pending')
    
    def __str__(self):
        return f"Payment for {self.booking} - status: {self.status}"
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    
    def __str__(self):
        return self.name

    
class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('car', 'user')
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.car.name}"
    
    @staticmethod
    def calculate_average_rating(car):
        """ calculate avareage rating for car """
        reviews = Review.objects.filter(car=car)
        if reviews.exists():
              return round(reviews.aggregate(models.Avg('rating'))['rating__avg'],1)
        return 0.0
  
class Reward(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    discount_available = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    
    def __str__(self):
        return f"{self.user.username} - {self.points} points,Discount: ETB{self.discount_available}"
    
    
    def add_points(self, amount):
        """
        add reward point to user.
        """
        self.points += amount
        self.save()
        
    def redeem_points(self):
            """
            Redeem reward points if user has enough.
            """
            if self.points <100:
                return 0
            redeemable_points =(self.points // 100) * 100
            discount = (redeemable_points//100)* 10
            self.points -= redeemable_points
            self.discount_available += discount
            self.save()
            return discount
        
    def use_discount(self):
        """use available discouunt for the next booking"""
        discount =self.discount_available
        self.discount_available = 0
        self.save()
        return discount
    
