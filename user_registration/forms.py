from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from user_registration.models import CustomUser


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    is_coach = forms.BooleanField(required=False, label="Are you a lacrosse coach?")
    is_scorekeeper = forms.BooleanField(required=False, label="Are you a lacrosse scorekeeper?")

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "is_coach",
            "is_scorekeeper",
            "email",
            "username",
            "password1",
            "password2",
        ]
    