from django.contrib import admin
from .models import Car, Booking, CustomProfile, Payment, Location,Review,Reward
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.mail import send_mail
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
        
        # for email notification
        def mark_as_completed(self, request, queryset):
            for booking in queryset:
                if booking.status != "Completed" and booking.payment_status == "Paid":
                    booking.status = "Completed"
                    booking.save()
                    # Send email notification
                    subject = f"Booking {booking.id} Completed - Ethio Car Rental"
                    message = f"""
                    Dear {booking.user.username},

                    We are pleased to inform you that your booking (ID: {booking.id}) has been marked as Completed.
                    Details:
                    - Car: {booking.car.name}
                    - Start Date: {booking.start_date}
                    - End Date: {booking.end_date}
                    - Total Price: ETB {booking.total_price}

                    Thank you for choosing Ethio Car Rental!

                    Best regards,
                    The Ethio Car Rental Team
                    """
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [booking.user.email],
                        fail_silently=True,
                    )
            self.message_user(request, f"{queryset.count()} booking(s) marked as Completed and notification(s) sent.")

        mark_as_completed.short_description = "Mark selected bookings as Completed"
    
        
admin.site.register(Booking,BookingAdmin)


class RewardAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')
    search_fields = ('user__username',)
    
admin.site.register(Reward,RewardAdmin)    
    
class CustomProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'extracted_name')
    readonly_fields = ('id_front_image_preview', 'id_back_image_preview')

    def id_front_image_preview(self, obj):
        if obj.id_front_image:
            return mark_safe(f'<img src="{obj.id_front_image.url}" width="150" height="150" />')
        return "No Image"
    id_front_image_preview.short_description = "Front Image"

    def id_back_image_preview(self, obj):
        if obj.id_back_image:
            return mark_safe(f'<img src="{obj.id_back_image.url}" width="150" height="150" />')
        return "No Image"
    id_back_image_preview.short_description = "Back Image"

admin.site.register(CustomProfile, CustomProfileAdmin)

admin.site.register(Payment)
admin.site.register(Location)
admin.site.register(Review) 




