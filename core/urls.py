from django.urls import path
from .views import HomeView, CreatePlayerView, CreateRosterView, ListPlayerView, ListRosterView

urlpatterns = [
    #path('', HomeView.as_view()),
    path('create-player', CreatePlayerView.as_view()),
    path('create-roster', CreateRosterView.as_view()),
    path('list-player', ListPlayerView.as_view()),
    path('list-roster', ListRosterView.as_view()),

]