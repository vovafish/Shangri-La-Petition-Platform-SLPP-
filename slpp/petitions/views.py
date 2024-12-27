from django.http import HttpResponse
from django.shortcuts import render
from .models import Petition  # Import the Petition model
from django.db import connection

def petitions(request):
    # Check if the 'status' query parameter is present
    status = request.GET.get('status')
    
    if status and status.lower() == 'open':
        # Fetch all open petitions
        petitions = Petition.objects.filter(status__iexact='open')  # Filter petitions with status 'open' (case insensitive)
    else:
        # Fetch all records from the petitions table
        petitions = Petition.objects.all()  # Retrieve all petitions

    return render(request, 'petitions.html', {'petitions': petitions})  # Pass data to template

def open_petitions(request):
    # Fetch all open petitions
    open_petitions = Petition.objects.filter(status__iexact='open')  # Filter petitions with status 'open' (case insensitive)
    return render(request, 'open_petitions.html', {'petitions': open_petitions})  # Pass data to template