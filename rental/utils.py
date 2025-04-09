
import requests
import logging
from .models import Car, Booking,Reward
import pytesseract
from PIL import Image
import re
logger = logging.getLogger(__name__)

# Path to Tesseract executable (update if different)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """Extract text from an image using Tesseract OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return str(e)

def extract_name_from_text(text):
    """Extract the name from the OCR-extracted text."""
    # Simple heuristic: Look for a line starting with "Name" or similar
    lines = text.split('\n')
    for line in lines:
        if re.search(r'^(Name|Full Name|Given Name)\s*[:\s]', line, re.IGNORECASE):
            name = re.sub(r'^(Name|Full Name|Given Name)\s*[:\s]', '', line, flags=re.IGNORECASE)
            return name.strip()
    # Fallback: Look for a line that looks like a name (e.g., two words, capitalized)
    for line in lines:
        if re.match(r'^[A-Z][a-z]+\s[A-Z][a-z]+$', line.strip()):
            return line.strip()
    return None



    
    
    
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
        
        