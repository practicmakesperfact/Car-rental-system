import requests
import logging
from .models import Car, Booking,Reward

logger = logging.getLogger(__name__)

def update_car_location(car_id):
    """fetch the live location of a car from a GPS  tracking API and updates the database"""
    try: 
            url ="https://third-party-api.com/location" #  Replace with the actual GPS API endpoint
            response =requests.get(url,params={'car_id':car_id},timeout=5)
            if response.status_code==200:
                data = response.json()
                if ('latitude' in data and 'longitude' in data):
                    car = Car.objects.get(id=car_id)
                    car.latitude = data['latitude']
                    car.longitude = data['longitude']
                    car.save()
                    return True
                else:
                    logger.error(f"GPS API response missing coordinates for car ID{car_id} ")
            else:
                logger.error(f"Failed to fetch GPS data for car ID{car_id}: {response.status_code} ")
    except requests.exceptions.RequestException as e:
        logger.error(f"request error while fetching GPS data:{e}")
    except Car.DoesNotExist:
        logger.error(F"Car with ID{car_id} does not found")
    return False
           

def apply_loyalty_discount(user,total_price):
    """applies loyalty points as a discount if the user has enough points"""

    try:
        reward = Reward.objects.get(user = user)
        if reward.points >= 1000:
            discount =min(10,reward.points)
            reward.points -=discount
            reward.save()
            return total_price - discount
    except Exception as e:
        logger.error(f"Error applying loyalty discounts:{e}")
        
    return total_price
        
        