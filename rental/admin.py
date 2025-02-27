from django.contrib import admin
from .models import Car, Rental

# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'model_year', 'price_per_day', 'is_available')
    list_filter = ('brand', 'is_available', 'transmission')
    search_fields = ('brand', 'name')

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'start_date', 'end_date', 'total_price', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'car__name')
