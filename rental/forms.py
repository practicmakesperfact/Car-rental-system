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
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=200, required=True)
    id_front_image = forms.ImageField(required=True, label="ID/Passport Front Image")
    id_back_image = forms.ImageField(required=True, label="ID/Passport Back Image")

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password1', 'password2',
                  'phone_number', 'address', 'id_front_image', 'id_back_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email

    def clean_id_front_image(self):
        image = self.cleaned_data.get('id_front_image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Front image is too large (max 5MB).")
            if not image.content_type in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("Front image must be JPEG or PNG.")
        return image

    def clean_id_back_image(self):
        image = self.cleaned_data.get('id_back_image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Back image is too large (max 5MB).")
            if not image.content_type in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("Back image must be JPEG or PNG.")
        return image

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # using email as username
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        user.is_active = False  # Require email verification

        if commit:
            user.save()
            CustomProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address'],
                id_front_image=self.cleaned_data['id_front_image'],
                id_back_image=self.cleaned_data['id_back_image'],
                extracted_name="",  # to be updated after OCR
            )
        return user
