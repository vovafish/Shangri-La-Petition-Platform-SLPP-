from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from .models import Petition  # Import the Petition model from the current app
from signatures.models import PetitionSignature  # Import the PetitionSignature model from the signatures app
from petitioners.forms import PetitionForm  # Import the PetitionForm
from django.db import connection
from .decorators import jwt_required
from petitioners.models import Petitioners  # Import the Petitioners model from the petitioners app

def petitions(request):
    # Check if the 'status' query parameter is present
    status = request.GET.get('status')
    
    if status and status.lower() == 'open':
        # Fetch all open petitions
        petitions = Petition.objects.filter(status__iexact='open')  # Filter petitions with status 'open' (case insensitive)
    else:
        # Fetch all records from the petitions table
        petitions = Petition.objects.all()  # Retrieve all petitions

    # Create a dictionary to hold signed petition statuses
    signed_petitions = {}
    user_email = request.session.get('petitioner_email')
    
    if user_email:
        signed_petition_ids = PetitionSignature.objects.filter(petitioner_email__petitioner_email=user_email).values_list('petition_id', flat=True)
        signed_petitions = {petition_id: True for petition_id in signed_petition_ids}

    return render(request, 'petitions.html', {'petitions': petitions, 'signed_petitions': signed_petitions})  # Pass data to template

@jwt_required
def create_petition(request):
    if not request.session.get('petitioner_email'):
        return redirect('login')
        
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            new_petition = Petition(
                petitioner_email=request.session['petitioner_email'],
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
            # Debugging: Print form errors
            print(form.errors)  # Print errors to the console
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = PetitionForm()
    return render(request, 'create_petition.html', {'form': form})

@jwt_required
def sign_petition(request, petition_id):
    if request.method == 'POST':
        user_email = request.session.get('petitioner_email')
        
        if not user_email:
            return JsonResponse({"error": "You must be logged in to sign a petition."}, status=401)

        try:
            petition = Petition.objects.get(petition_id=petition_id)

            # Check if the user is trying to sign their own petition
            if petition.petitioner_email == user_email:
                return JsonResponse({"error": "You cannot sign your own petition."}, status=400)

            # Check if the user has already signed this petition
            if PetitionSignature.objects.filter(petitioner_email__petitioner_email=user_email, petition_id=petition).exists():
                return JsonResponse({"error": "You have already signed this petition."}, status=400)

            # Retrieve the Petitioners instance
            petitioner_instance = Petitioners.objects.get(petitioner_email=user_email)

            # Create a new signature record
            PetitionSignature.objects.create(petitioner_email=petitioner_instance, petition_id=petition)

            # Increment the signature count
            petition.signature_count += 1
            petition.save()

            return JsonResponse({"status": "success"})
        except Petition.DoesNotExist:
            return JsonResponse({"error": "Petition does not exist."}, status=404)
        except Petitioners.DoesNotExist:
            return JsonResponse({"error": "Petitioner does not exist."}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=405)