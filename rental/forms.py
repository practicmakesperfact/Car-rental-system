import pytesseract
import cv2
from PIL import Image #(PLI=Python Imaging Library)
from django import forms
from django.core.exceptions import ValidationError
from .models import Booking,Review, CustomProfile ,User
from django.contrib.auth.models import User


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['car','start_date', 'end_date']
        widgets ={
            'start_date': forms.DateInput(attrs={'type': 'date', 'class':'input-field'}),
            'end_date': forms.DateInput(attrs={'type': 'date','class':'input-field'}),
        }
          

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-400 rounded-lg focus:ring-0 focus:border-blue-500 outline-none',
                'step': 0.5,
                'min': 1,
                'max': 5,
                'placeholder': 'Rate from 1 to 5'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-400 rounded-lg focus:ring-0 focus:border-blue-500 outline-none',
                'rows': 4,
                'placeholder': 'Write your review here...'
            }),
        }
# set tesseract OCR path(windows only)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True,label='Full Name')
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput,required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput,required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=200, required=True)
    id_front = forms.ImageField(required=True,label='Upload ID/passport front page')
    id_back = forms.ImageField(required=True,label='Upload ID/passport back page')
    is_passport_name = forms.CharField(max_length=100, required=True,label='Name on ID/Passport')
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def extract_text_from_image(self, image_file):
        """ extract text from the uploaded image using OCR"""
        image = Image.open(image_file)
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text.lower()
    
    def clean(self):
        """ custom validation for password and confirm password """
        cleaned_data = super().clean()
        username = cleaned_data.get('username', '').strip().lower()
        # extract text from ID/passport back and front images
        id_front_text = self.extract_text_from_image(cleaned_data.get('id_front'))
        id_back_text = self.extract_text_from_image(cleaned_data.get('id_back'))
        
        # check if the name contains  the I full name(username)
        if username not in id_front_text and username not in id_back_text:
            raise forms.ValidationError("Name on ID/Passport does not match the name on the form.")
        
       # check if password matches 
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Try again.")
        return cleaned_data
         
    def save(self,commit=True):
        """ save the user and create a custom profile """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            CustomProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address'],
                id_front=self.cleaned_data['id_front'],
                id_back=self.cleaned_data['id_back'],
                is_passport_name=self.cleaned_data['is_passport_name']
                
            )
        return user
        