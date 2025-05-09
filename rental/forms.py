# import pytesseract
# import cv2
from PIL import Image #(PLI=Python Imaging Library)
from django import forms
from django.core.exceptions import ValidationError
from .models import Booking,Review, CustomProfile ,User
from django.contrib.auth.forms import UserCreationForm
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

    
    #for users upload images of their ID/passport
class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, label="Full Name")
    email = forms.EmailField(required=True)
    id_front_image = forms.ImageField(required=True, label="ID/Passport Front Image")
    id_back_image = forms.ImageField(required=True, label="ID/Passport Back Image")

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password1', 'password2', 'id_front_image', 'id_back_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text for password fields
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Use email as username
        if commit:
            user.save()
            # Create or update the CustomProfile
            CustomProfile.objects.create(
                user=user,
                id_front_image=self.cleaned_data['id_front_image'],
                id_back_image=self.cleaned_data['id_back_image'],
            )
        return user
class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = CustomProfile
        fields = [
            'phone_number',
            'address',
            'id_front_image',
            'id_back_image',
            'extracted_name',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }