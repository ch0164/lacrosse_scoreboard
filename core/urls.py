from django.urls import path
from .views import PlayerListView, index, HomeView, PublishedScorebooksView, RosterView, LoginView, \
    EditScorebookView, ScorebookView, CreatePlayerView, CreateRosterView, ListPlayerView, ListRosterView

urlpatterns = [
    path('', HomeView),
    path("<int:id>", index, name="index"),
    path('published-scorebooks/', PublishedScorebooksView),
    path('scorebook/', ScorebookView),
    path('edit-scorebook/', EditScorebookView),
    path('roster/', PlayerListView.as_view()),
    path('create-player/', CreatePlayerView.as_view()),
    path('create-roster/', CreateRosterView.as_view()),
    path('list-player/', ListPlayerView.as_view()),
    path('list-roster/', ListRosterView.as_view()),

]