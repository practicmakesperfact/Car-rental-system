from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/book/', views.book_car, name='book_car'),
    path('rental-history/', views.rental_history, name='rental_history'),
    path('about/', views.about, name='about'),
    path('locations/', views.locations, name='locations'),
    path('rewards/', views.user_rewards, name='user_rewards'),
    path('rewards/redeem/', views.redeem_rewards,name='redeem_rewards'),
    path('cars/<int:car_id>/add_review/', views.add_review, name='add_review'),

#     path('profile/', views.profile, name='profile'),
#     path('reviews/', views.reviews_list, name='reviews_list'),
#     path('location/', views.location_list, name='location_list'),
#     path('payment/', views.payment, name='payment'),

# authentications urls
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
