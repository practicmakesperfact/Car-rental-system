from django.contrib import admin
from .models import Car, Rental, CustomProfile, Payment, Location,Review

# Register your models here.

admin.site.register(Car)
admin.site.register(Rental)
admin.site.register(CustomProfile)
admin.site.register(Payment)
admin.site.register(Location)
admin.site.register(Review) 

