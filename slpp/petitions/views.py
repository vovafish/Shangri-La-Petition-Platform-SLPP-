from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Petition  # Import the Petition model
from petitioners.forms import PetitionForm  # Import the PetitionForm
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

def create_petition(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            # Create a new petition instance
            new_petition = Petition(
                petitioner_email=form.cleaned_data['petitioner_email'],
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                status='open',  # Automatically set status to 'open'
                response='',  # Leave response empty
                signature_count=0  # Set signature count to 0
            )
            new_petition.save()  # Save the new petition to the database
            return redirect('petition_list')  # Redirect to the list of petitions after creation
    else:
        form = PetitionForm()
    return render(request, 'create_petition.html', {'form': form})  # Render the form template