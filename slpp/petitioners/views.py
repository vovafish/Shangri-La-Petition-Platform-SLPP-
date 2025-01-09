from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from .models import Petitioners
from petitions.models import BioID
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.hashers import make_password, check_password

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['petitioner_email']
            fullname = form.cleaned_data['fullname']
            dob = form.cleaned_data['dob']
            password = form.cleaned_data['password']
            bioid_code = form.cleaned_data['bioid']

            # Check if the BioID exists and is not used
            try:
                bioid = BioID.objects.get(code=bioid_code)
                if bioid.used >= 1:
                    messages.error(request, "This BioID has already been used.")
                    return render(request, 'register.html', {'form': form})

                # Hash the password
                password_hash = make_password(password)

                # Create a new user
                petitioner = Petitioners(
                    petitioner_email=email,
                    fullname=fullname,
                    dob=dob,
                    password_hash=password_hash,
                    bioid=bioid_code
                )
                petitioner.save()  # Save the new user to the database

                # Update the BioID usage
                bioid.used += 1
                bioid.save()

                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login')  # Redirect to the login page after successful registration
            except BioID.DoesNotExist:
                messages.error(request, "Invalid BioID provided.")
                return render(request, 'register.html', {'form': form})
        else:
            # Debugging: Print form errors
            print(form.errors)  # Print errors to the console
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['petitioner_email']
            password = form.cleaned_data['password']

            try:
                petitioner = Petitioners.objects.get(petitioner_email=email)
                if check_password(password, petitioner.password_hash):
                    # Successful login
                    request.session['petitioner_email'] = email  # Store email in session
                    messages.success(request, "Login successful!")
                    return redirect('home')  # Redirect to home.html after successful login
                else:
                    messages.error(request, "Invalid email or password.")
            except Petitioners.DoesNotExist:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    # Clear all existing messages first
    storage = messages.get_messages(request)
    storage.used = True  # Mark all current messages as used
    
    # Clear the session
    request.session.flush()
    
    # Add only the logout message
    messages.success(request, "You have been logged out.")
    return redirect('login')

def home(request):
    return render(request, 'home.html')  # Render your home.html template
