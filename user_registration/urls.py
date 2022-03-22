from django.urls import path

from user_registration.views import register

urlpatterns = [
    path("register/", register, name="register"),
]
