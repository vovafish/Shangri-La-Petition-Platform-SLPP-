from django.http import HttpResponse
from django.shortcuts import render
from .models import BioID  # Import your model
from django.db import connection

def petitions(request):
    # Fetch all records from the bioid table
    bioids = BioID.objects.all()
    return render(request, 'petitions.html', {'bioids': bioids})  # Pass data to template