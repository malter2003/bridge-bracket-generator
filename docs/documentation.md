[GitHub Repository](https://github.com/malter2003/bridge-bracket-generator)

[Kanban Board](https://github.com/users/malter2003/projects/1/views/1)

# Setup

To set up your local environment, there are a couple of steps that you must follow. Follow the instructions below to get the site running locally.

### Clone the Repository

The first step  is to clone the repository. If you have an SSH key, do `git clone git@github.com:malter2003/bridge-bracket-generator.git`. If you only have a GitHub account, then do `https://github.com/malter2003/bridge-bracket-generator.git` to clone with HTTPS.

![](/home/bdamja/.config/marktext/images/2023-11-05-20-23-04-image.png)

### Setup Virtual Environment

This step requires python 3.8 or later. If you don't have python 3.8 or later, install that. Then, do `python -m venv djvenv` to instantiate a Django virtual environment. 

Activate the virtual environment by doing `source djvenv/bin/activate`. You will know that it properly activated if it displays `(djvenv)` next to the command line prefix.

### Install Django

While the virtual environment is activated, perform the command `pip install django` to install the latest version of Django. Be sure to also do `python3 -m pip install --upgrade pip` to upgrade pip.

### Start the Local Server

Ensure you don't already have something running on `127.0.0.1:8000`. Then, run the server by doing `python manage.py runserver` while in the virtual environment. This will start the server, and you should be able to go to `127.0.0.1:8000` or `localhost:8000` to access the site.

# Understanding the Code

### The model

Django follows the model-view-template architectural pattern. The model essentially represents the data and the database schema. Models in Django include attributes such as fields and relationships. The good thing about models, is that both the database entries and the forms can pull from the same model. In my project so far, I only have the model for the `Tournament` set up. The code looks like this:

```python
class Tournament(models.Model):
    creator = models.CharField("Creator", max_length=200)
    title = models.CharField("Title", max_length=200)
    players = models.TextField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tournament-detail", args=[str(self.id)])```
```

This defines a class `Tournament` that inherits from Django's `models.Model`. It has 2 character fields, a text field, and a boolean field. `def __str__(self):` means that when you call `str(tournament_instance)` you get the title of the tournament, meaning you have an easy way to represent them. `def get_absolute_url(self):` defines the canonical URL for this model as `tournament-detail`, where it finds the corresponding URL from `urlpatterns` in `urls.py`. Both the database and the TournamentForm use this model.

### List View

Currently, the Tournaments are displayed using a generic list view.

```python
class TournamentListView(generic.ListView):
    model = Tournament
```

When a user navigates to the `tournaments` path, they get routed to see `tournament_list.html`

```django
{% extends 'bracket_app/base_template.html' %}

{% block content %}
<h1>Tournament List</h1>
{% if tournament_list %}
<ul>
   {% for tournament in tournament_list %}
   <li>
      {{ tournament.title }} - Organizer: {{ tournament.creator }}
      <a class="btn btn-primary" href="{{ tournament.get_absolute_url }}" role="button">View</a>
      <a class="btn btn-danger" href="{% url 'tournament-delete' pk=tournament.id %}" role="button">Delete</a>
      <a class="btn btn-secondary" href="{% url 'tournament-update' pk=tournament.id %}" role="button">Update</a>
   </li>
   {% endfor %}
</ul>
{% else %}
<p>There are no tournaments.</p>
{% endif %}
{% endblock %}
```

Because this path uses the TournamentList view, it expects to have all of the tournaments in a tournament_list, thanks to Django's abstraction. If the list isn't empty, it iterates through each tournament and displays it top to bottom. Each line comes with buttons for viewing, updating, or deleting.

### Detail View

The detail view for the tournament doesn't use Django's generic models.

```python
def tournament_detail_view(request, pk):
    tournament = Tournament.objects.get(pk=pk)

    jsonDec = json.decoder.JSONDecoder()
    players = jsonDec.decode(tournament.players)

    context = {
        'tournament': tournament,
        'player_list': players,
    }

    return render(request, 'bracket_app/tournament_detail.html', context)
```

This defines the detail view for a tournament. The method takes the request and the primary key. It retrieves the tournament entry from the database and converts it to a python object, taking advantage of Object Relational Mapping (ORM) provided by Django.

Notice the next two lines. In the database, the players are stored as a string representing a JSON array. `jsonDec.decode(tournament.players)` takes a JSON string and converts into some kind of python object. In this case, it's an array of strings.

A context dictionary is then defined, given the tournament and the player_list in pythonic format. The tournament_detail.html is then rendered, with the context given.

```django
{% extends 'bracket_app/base_template.html' %}

{% load static %}

{% block content %}
<h1>Tournament Name: {{ tournament.title }}</h1>

<p><strong>Active:</strong> {{ tournament.is_active }}</p>
<p><strong>Organizer:</strong> {{ tournament.creator }}</p>

<p><strong>Players:</strong></p>
<ul>
    {% for player in player_list %}
    <li>
        <p> {{ player }} </p>
    </li>
    {% endfor %}
</ul>

{% endblock %}
```

This displays the tournament title, whether it's active or not, and the organizer. The file knows about `tournament` and `player_list` since it was provided in the context. It iterates through each player in the list and displays their name, in HTML list form.

Note: eventually this will hopefully display an actual bracket.

### CRUD Actions

The view functions in the project follow the CRUD methodology (Create, Read, Update, Delete) which manipulate tournament objects in the database. 

##### Create

```python
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

            return redirect('tournament-detail', pk=tournament.pk)

    context = {'form': form}
    return render(request, 'bracket_app/tournament_form.html', context) 

def stringToList(string):
    string = string.replace('\r', '')
    return string.split('\n') 
```

This view method allows users to create a tourament object in the database through a form. When the user submits the form with a POST request, it processes the data from the POST and converts it into a form. If the form is valid, it saves it to a tournament object, but doesn't save it to the database quite yet.

A player_list list of strings is created using the helper method, given the data of the players text box. It's then converted into a JSON string. Essentially what is happening is this:

```
player1
player2
player3
```

Becomes this:

```
"[\"player1\", \"player2\", \"player3\"]"
```

And the string is then stored in the database, and the user is redirected to the tournament detail page.

##### Update

```python
def updateTournament(request, pk):
  tournament = get_object_or_404(Tournament, pk=pk)

  if request.method == 'POST':

    form = TournamentForm(request.POST, instance = tournament)
    if form.is_valid():
      player_list = stringToList(tournament.players)
      tournament.players = json.dumps(player_list)
      form.save()
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
```

This view function handles the updating of a tournament. It first retrieves the tournament object given a primary key, and throws a 404 if it doesn't exist in the database. If the user is submitting the form (POST in this context) it processes the data and saves it to the database, similar to the `createTournament` method.

If it's not a POST then it must be a GET request (initial view). So, it retrieves the player list, converts it from a JSON string to a python list, and sets it as the initial value in the user's form. It then redirects them to the update page with the form data filled in.

##### Delete

```python
def deleteTournament(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    if request.method == 'POST':
        tournament.delete()
        # Redirect back to the tournament detail page
        return redirect('tournaments')

    context = {'tournament': tournament}
    return render(request, 'bracket_app/tournament_delete.html', context)
```

This view function handles the deletion of a tournament. It takes the primary key and retreives the tournament object from the database, or redirecting to 404 if not found. If it is a POST request that means the user confirmed the deletion, so the tournament is deleted from the database and they're redirected to the tournaments list view. If it's not a POST then it must be a GET, in which they're redirected to the deletion confirmation page.
