from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Movie, Review
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'category', 'trailer_link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actors': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'trailer_link': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 10:
            raise ValidationError("Rating must be between 1 and 10.")
        return rating

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
