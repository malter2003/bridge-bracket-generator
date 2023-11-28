from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import allowed_users
from .generator import Generator
import json

def index(request):
    return render( request, 'bracket_app/index.html')

class TournamentListView(generic.ListView):
    model = Tournament

def tournament_detail_view(request, pk):
    tournament = Tournament.objects.get(pk=pk)

    jsonDec = json.decoder.JSONDecoder()
    players = jsonDec.decode(tournament.players)

    context = {
        'tournament': tournament,
        'player_list': players,
        'path': "bracket_images/" + str(pk) + "_bracket.png",
        'size': len(players)
    }

    return render(request, 'bracket_app/tournament_detail.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['maker'])
def createTournament(request):
    form = TournamentForm()
    
    if request.method == 'POST':
        tournament_data = request.POST.copy()
        
        form = TournamentForm(tournament_data)
        if form.is_valid():
            tournament = form.save(commit=False)

            player_list = stringToList(tournament.players)
            tournament.players = json.dumps(player_list)
            tournament.save()

            Generator(800, 800, 50, player_list, tournament.pk).draw()

            return redirect('tournament-detail', pk=tournament.pk)

    context = {'form': form}
    return render(request, 'bracket_app/tournament_form.html', context)    

def stringToList(string):
    string = string.replace('\r', '')
    return string.split('\n')

@login_required(login_url='login')
@allowed_users(allowed_roles=['maker'])
def updateTournament(request, pk):
  tournament = get_object_or_404(Tournament, pk=pk)

  if request.method == 'POST':

    form = TournamentForm(request.POST, instance = tournament)
    if form.is_valid():
      player_list = stringToList(tournament.players)
      tournament.players = json.dumps(player_list)
      form.save()
      Generator(800, 800, 50, player_list, tournament.pk).draw()
      return redirect('tournament-detail', pk=pk)
  else:
    player_list = json.loads(tournament.players)
    tournament.players = "\n".join(player_list)
    form = TournamentForm(instance=tournament)

    context={
     'form': form,
     'tournament': tournament,
    }
  return render(request, 'bracket_app/tournament_update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['maker'])
def deleteTournament(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    if request.method == 'POST':
        tournament.delete()
        # Redirect back to the tournament detail page
        return redirect('tournaments')

    context = {'tournament': tournament}
    return render(request, 'bracket_app/tournament_delete.html', context)


def registerPage(request):
    form = CreateUserForm()
    print('y')
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print('z')
        if form.is_valid():
            print('x')
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='maker')
            user.groups.add(group)
            print('yay')

            messages.success(request, 'Account was created for: ' + username)
            return redirect('login')
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)
    