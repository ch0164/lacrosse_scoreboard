from django.urls import path
from .views import PlayerView, RosterView

urlpatterns = [
    path('', PlayerView.as_view()),
    path('roster', RosterView.as_view())
]