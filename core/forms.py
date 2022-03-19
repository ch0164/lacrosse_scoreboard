from django import forms

from core.constants import *

class PlayerEntryForm(forms.Form):
    player_number = forms.IntegerField(min_value=0)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    position = forms.CharField(widget=forms.Select(choices=POSITION_CHOICES))
    class_standing = forms.CharField(widget=forms.Select(choices=CLASS_STANDING_CHOICES))
    weight_pounds = forms.IntegerField(min_value=0)
    height_feet = forms.IntegerField(min_value=0)
    height_inches = forms.IntegerField(min_value=0)
    major = forms.CharField(max_length=100)
    hometown = forms.CharField(max_length=100)

