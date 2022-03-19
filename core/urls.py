from django.urls import path
import core.views as views

urlpatterns = [
    path('', views.home),
    path('published-scorebooks/', views.view_scorebook),
    path('scorebook/', views.view_scorebook),
    path('edit-scorebook/', views.edit_scorebook),
    path('roster/', views.view_roster),
    path('save-roster/', views.edit_roster),
    path('edit_player/<int:player_id>', views.edit_player, name="edit_player"),
]
