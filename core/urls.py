from django.urls import path
from .views import EditRoster, EditPlayer, HomeView, PublishedScorebooksView, RosterView, \
    EditScorebookView, ScorebookView

urlpatterns = [
    path('', HomeView),
    #path("<int:id>", index, name="index"),
    path('published-scorebooks/', PublishedScorebooksView),
    path('scorebook/', ScorebookView),
    path('edit-scorebook/', EditScorebookView),
    path('roster/', RosterView),
    path('save-roster/', EditRoster),
    path('edit_player/<int:player_id>', EditPlayer, name="edit_player"),
    # path('create-player/', CreatePlayerView.as_view()),
    # path('create-roster/', CreateRosterView.as_view()),
    # path('list-player/', ListPlayerView.as_view()),
    # path('list-roster/', ListRosterView.as_view()),

]