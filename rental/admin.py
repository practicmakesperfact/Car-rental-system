from django.contrib import admin
from .models import Car, Booking, CustomProfile, Payment, Location,Review,Reward
from django.utils.safestring import mark_safe
# Register your models here.

#car admin with map preview
class CarAdmin(admin.ModelAdmin):
    list_display =('name','brand','model_year','is_available','latitude','longitude','location_map')
    search_fields = ('name','brand','model_year')
    list_filter = ('is_available',)
    def location_map(self, obj):
        if obj.latitude and obj.longitude:
             return mark_safe(f'<iframe width="250" height="150" src="https://maps.google.com/maps?q={obj.latitude},{obj.longitude}&hl=en&z=14&output=embed"></iframe>')
        return "Location not available"
    
    location_map.short_description = "Map Preview"
admin.site.register(Car,CarAdmin)

# Booking Admin with Search & Filters

class BookingAdmin(admin.ModelAdmin):
        list_display = ('id','user', 'car', 'start_date', 'end_date', 'status','payment_status','total_price','created_at')
        search_fields = ('user__username', 'car__name')
        list_filter = ('status','payment_status')
        actions = ['mark_as_completed']
        
        def mark_as_completed(self,request,queryset):
            queryset.update(status='Completed')
        mark_as_completed.short_description = "Mark selected bookings as completed"
        
admin.site.register(Booking,BookingAdmin)


class RewardAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')
    search_fields = ('user__username',)
    
admin.site.register(Reward,RewardAdmin)    
    
admin.site.register(CustomProfile)
admin.site.register(Payment)
admin.site.register(Location)
admin.site.register(Review) 




