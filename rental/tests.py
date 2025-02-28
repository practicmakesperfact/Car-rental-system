from django.test import TestCase

# Create your tests here.
from .models import Car, Rental


class CarModelTest(TestCase):
    def test_string_representation(self):
        car = Car(name="Test Car", brand="Test Brand", model_year=2022, transmission="A", seats=4, price_per_day=1000.00)
        self.assertEqual(str(car), "Test Brand Test Car (2022)")

class RentalModelTest(TestCase):
    def test_string_representation(self):       
         rental = Rental(user_id=1, car_id=1, start_date='2023-05-01', end_date='2023-05-05', total_price=500.00 , status='P')
         self.assertEqual(str(rental), "1 - 1 (2025-03-01 to 2025-05-05)")