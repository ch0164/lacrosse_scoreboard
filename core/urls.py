from django.urls import path
import core.views as views

urlpatterns = [
    path('', views.home),
    path('published-scorebooks/', views.view_scorebook),
    path('scorebook/', views.view_scorebook),
    path('create-scorebook/', views.create_scorebook),
    path('edit-scorebook/', views.edit_scorebook),
    path('edit-player/<int:player_id>/', views.edit_player, name="edit_player"),
    path('roster/', views.view_roster),
    path('delete-player/<int:player_id>', views.delete_player, name="delete_player"),
]
