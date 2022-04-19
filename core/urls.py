from django.urls import path
import core.views as views

urlpatterns = [
    # View scorebook views below.
    path('', views.home),
    path('view-scorebook/<int:scorebook_id>', views.view_scorebook,
         name="view_scorebook"),

    # Edit Scorebook views below.
    path('create-scorebook/', views.create_scorebook),
    path('edit-scorebook/', views.edit_scorebook),
    path('update-stats/', views.update_stats),
    path('edit-score/<int:score_id>/',
         views.scorebook_edit_score, name="edit_score"),
    path('edit-personal-foul/<int:penalty_id>/',
         views.scorebook_edit_personal_foul, name="edit_personal_foul"),
    path('edit-technical-foul/<int:penalty_id>/',
         views.scorebook_edit_technical_foul, name="edit_technical_foul"),
    path('edit-timeout/<int:timeout_id>/',
         views.scorebook_edit_timeout, name="edit_timeout"),
    path('edit-scorebook-player/<int:player_id>/',
         views.scorebook_edit_player, name="edit_scorebook_player"),

    # Delete Scorebook redirects below.
    path('delete-score/<int:score_id>', views.scorebook_delete_score,
         name="delete_score"),
    path('delete-penalty/<int:penalty_id>', views.scorebook_delete_penalty,
         name="delete_penalty"),
    path('delete-timeout/<int:timeout_id>', views.scorebook_delete_timeout,
         name="delete_timeout"),
    path('delete-scorebook-player/<int:player_id>',
         views.scorebook_delete_player,
         name="delete_scorebook_player"),

    # Roster view URLs below.
    path('edit-player/<int:player_id>/', views.edit_player, name="edit_player"),
    path('delete-player/<int:player_id>', views.delete_player,
         name="delete_player"),
    path('roster/', views.view_roster),
]
