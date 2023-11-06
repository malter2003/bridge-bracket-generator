from django.forms import ModelForm
from .models import *

# create class for tournament form
class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields =('creator', 'title', 'players', 'is_active')