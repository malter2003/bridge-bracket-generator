from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/registerlogout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('accounts/logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('accounts/register', views.registerPage, name='register-page'),
    path('tournaments/', views.TournamentListView.as_view(), name='tournaments'),
    path('tournament/<int:pk>', views.tournament_detail_view, name='tournament-detail'),
    path('tournaments/create/', views.createTournament, name='tournament-create'),
    path('tournament/<int:pk>/delete/', views.deleteTournament, name='tournament-delete'),
    path('tournament/<int:pk>/update/', views.updateTournament, name='tournament-update'),
]
