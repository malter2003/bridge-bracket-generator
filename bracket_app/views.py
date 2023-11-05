from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import *
from .forms import *
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
    }

    return render(request, 'bracket_app/tournament_detail.html', context)



def createTournament(request):
    form = TournamentForm()
    
    if request.method == 'POST':
        # Create a new dictionary with form data
        tournament_data = request.POST.copy()
        
        form = TournamentForm(tournament_data)
        if form.is_valid():
            # Save the form without committing to the database
            tournament = form.save(commit=False)

            player_list = stringToList(tournament.players)

            tournament.players = json.dumps(player_list)
            tournament.save()

            # Redirect back to the tournament detail page
            return redirect('tournament-detail', pk=tournament.pk)

    context = {'form': form}
    return render(request, 'bracket_app/tournament_form.html', context)    

def stringToList(string):
    string = string.replace('\r', '')
    return string.split('\n')
