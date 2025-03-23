from django import forms
from .models import Booking,Review, CustomProfile


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

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=200, required=True)
    id_passport = forms.ImageField(required=True)
    selfie_image = forms.ImageField(required=True) # webcam selfie upload
    class Meta:
        model = CustomProfile
        fields = ['username', 'email', 'password', 'confirm_password', 'phone_number', 'address', 'id_passport', 'selfie_image']
    
