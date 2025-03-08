from django import forms
from .models import Booking,Review


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
   