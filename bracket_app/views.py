from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render( request, 'bracket_app/index.html')