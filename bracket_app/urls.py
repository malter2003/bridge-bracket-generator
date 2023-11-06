from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tournaments/', views.TournamentListView.as_view(), name='tournaments'),
    path('tournament/<int:pk>', views.tournament_detail_view, name='tournament-detail'),
    path('tournaments/create/', views.createTournament, name='tournament-create'),
    path('tournament/<int:pk>/delete/', views.deleteTournament, name='tournament-delete'),
    path('tournament/<int:pk>/update/', views.updateTournament, name='tournament-update'),
]
