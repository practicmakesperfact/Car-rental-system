from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # authentications urls
    path('', views.user_login, name='login'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='rental/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='rental/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='rental/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='rental/password_reset_complete.html'), name='password_reset_complete'),
   
    path('register', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    path('home', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/book/', views.book_car, name='book_car'),
    path('booking/<int:booking_id>/confirm/', views.confirm_booking, name='confirm_booking'),
    path('rental-history/', views.rental_history, name='rental_history'),
    path('about/', views.about, name='about'),
    path('locations/', views.locations, name='locations'),
    path('rewards/', views.user_rewards, name='user_rewards'),
    path('cars/<int:car_id>/add_review/', views.add_review, name='add_review'),
    path('rentals/<str:category>/', views.rental_list, name='rental_list'),
    path("services/", views.services, name="services"),
    path('profile/', views.profile, name='profile'),
 
    path('location/', views.locations, name='locations'),
    
    #payment
    path('payment/process/<int:booking_id>/', views.initiate_payment, name='process_payment'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
    path('payment/success/', views.payment_status, name='payment_success'),
    path('payment/failed/', views.payment_fail, name='payment_failed'),
    # update profile
    path('profile/update', views.update_profile, name='update_profile'),
    # for Footer Links
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('faqs/', views.faqs, name='faqs'),
    path('support/', views.support, name='support'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
