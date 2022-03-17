from django.contrib import admin

from .models import Coach, Player, Roster
from user_registration.models import CustomUser

# Register your models here.
admin.site.register(Coach)
admin.site.register(Player)
admin.site.register(Roster)
admin.site.register(CustomUser)

