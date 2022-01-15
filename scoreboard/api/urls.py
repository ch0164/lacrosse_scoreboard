from django.urls import path
from .views import RosterView

urlpatterns = [
    path('', RosterView.as_view()),
]