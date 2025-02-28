from django import forms
from .models import Rental,Review


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['car','start_date', 'end_date']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['car','rating', 'comment']