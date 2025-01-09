from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from .models import Petition, AdminSettings  # Import the Petition model from the current app
from signatures.models import PetitionSignature  # Import the PetitionSignature model from the signatures app
from petitioners.forms import PetitionForm  # Import the PetitionForm
from .forms import ThresholdUpdateForm, PetitionResponseForm, AdminLoginForm  # Import the PetitionForm
from django.db import connection
from .decorators import jwt_required
from petitioners.models import Petitioners  # Import the Petitioners model from the petitioners app
from django.contrib.auth.hashers import check_password
from django.contrib import messages

def petitions(request):
    # Check if the 'status' query parameter is present
    status = request.GET.get('status')
    sort_order = request.GET.get('sort', 'latest')  # Default to 'latest'

    if status and status.lower() == 'open':
        petitions = Petition.objects.filter(status__iexact='open')
    else:
        petitions = Petition.objects.all()

    # Sort petitions based on user selection
    if sort_order == 'oldest':
        petitions = petitions.order_by('created_at')  # Oldest first
    else:
        petitions = petitions.order_by('-created_at')  # Latest first

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
    if not request.session.get('petitioner_email'):
        return JsonResponse({"error": "Authentication required"}, status=401)

    if request.method == 'POST':
        user_email = request.session.get('petitioner_email')
        
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

@jwt_required
def admin_dashboard(request):
    if request.session.get('admin_email') != 'admin@petition.parliament.sr':
        return redirect('admin_login')

    # Get current threshold
    admin_settings = AdminSettings.objects.first()
    threshold = admin_settings.signature_threshold if admin_settings else 100

    # Get petitions that reached threshold
    threshold_petitions = Petition.objects.filter(
    signature_count__gte=threshold,
    status='open'
    ).select_related() 

    return render(request, 'admin_dashboard.html', {
        'threshold': threshold,
        'threshold_petitions': threshold_petitions
    })

@jwt_required
def update_threshold(request):
    if request.method == 'POST':
        form = ThresholdUpdateForm(request.POST)
        if form.is_valid():
            admin_settings = AdminSettings.objects.first()
            admin_settings.signature_threshold = form.cleaned_data['signature_threshold']
            admin_settings.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@jwt_required
def add_petition_response(request, petition_id):
    if request.method == 'POST':
        form = PetitionResponseForm(request.POST)
        if form.is_valid():
            petition = Petition.objects.get(petition_id=petition_id)
            petition.response = form.cleaned_data['response']
            petition.status = 'closed'
            petition.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                admin_settings = AdminSettings.objects.first()
                if (email == admin_settings.admin_email and 
                    check_password(password, admin_settings.password_hash)):
                    request.session['admin_email'] = email
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, "Invalid credentials.")
            except AdminSettings.DoesNotExist:
                messages.error(request, "Admin settings not found.")
        
        return render(request, 'admin_login.html', {'form': form})
    else:
        form = AdminLoginForm()
        return render(request, 'admin_login.html', {'form': form})

def user_dashboard(request):
    if not request.session.get('petitioner_email'):
        return redirect('login')
    
    user_email = request.session.get('petitioner_email')
    filter_type = request.GET.get('filter', 'all')  # Default to 'all'
    
    # Get user's created petitions
    created_petitions = Petition.objects.filter(petitioner_email=user_email)
    
    # Get user's signed petitions
    signed_petitions = Petition.objects.filter(
        petitionsignature__petitioner_email__petitioner_email=user_email
    )
    
    # Filter based on user selection
    if filter_type == 'created':
        petitions = created_petitions
    elif filter_type == 'signed':
        petitions = signed_petitions
    else:  # 'all'
        petitions = (created_petitions | signed_petitions).distinct()
    
    context = {
        'petitions': petitions,
        'filter_type': filter_type,
        'created_count': created_petitions.count(),
        'signed_count': signed_petitions.count()
    }
    
    return render(request, 'user_dashboard.html', context)