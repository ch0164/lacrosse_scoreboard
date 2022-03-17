from django import forms

from core.constants import *

class PlayerEntryForm(forms.Form):
    player_number = forms.IntegerField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    position = forms.CharField(widget=forms.Select(choices=POSITION_CHOICES))
    class_standing = forms.CharField(widget=forms.Select(choices=CLASS_STANDING_CHOICES))
    weight_pounds = forms.IntegerField()
    height_feet = forms.IntegerField()
    height_inches = forms.IntegerField()
    major = forms.CharField(max_length=100)
    hometown = forms.CharField(max_length=100)

