from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from .models import Petition  # Import the Petition model
from petitioners.forms import PetitionForm  # Import the PetitionForm
from django.db import connection
from .decorators import jwt_required

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

# def open_petitions(request):
#     # Fetch all open petitions
#     open_petitions = Petition.objects.filter(status__iexact='open')  # Filter petitions with status 'open' (case insensitive)
#     return render(request, 'open_petitions.html', {'petitions': open_petitions})  # Pass data to template

@jwt_required
def create_petition(request):
    if not request.session.get('petitioner_email'):
        return redirect('login')
        
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            new_petition = Petition(
                petitioner_email=form.cleaned_data['petitioner_email'],
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                status='open',
                response='',
                signature_count=0
            )
            new_petition.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('petition_list')
    else:
        form = PetitionForm(initial={'petitioner_email': request.session.get('petitioner_email')})
    return render(request, 'create_petition.html', {'form': form})

def sign_petition(request, petition_id):
    if request.method == 'POST':
        try:
            petition = Petition.objects.get(petition_id=petition_id)
            if petition.status.lower() == 'open':
                petition.signature_count += 1  # Increment the signature count
                petition.save()  # Save the updated petition
                return HttpResponse(status=204)  # No content response
            else:
                return HttpResponse("This petition is not open for signing.", status=400)
        except Petition.DoesNotExist:
            return HttpResponse("Petition does not exist.", status=404)
    return HttpResponse("Invalid request method.", status=405)