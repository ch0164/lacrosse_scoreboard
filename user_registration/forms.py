from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    is_coach = forms.BooleanField(required=False, label="Are you a lacrosse coach?")

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "is_coach",
            "email",
            "username",
            "password1",
            "password2",
        ]
    