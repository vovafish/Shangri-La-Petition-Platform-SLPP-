from django.urls import path
from .views import petitions, create_petition  # Import the create_petition view

urlpatterns = [
    path('', petitions, name='petition_list'),  # This will match /slpp/petitions/
    path('create/', create_petition, name='create_petition'),  # This will match /slpp/petitions/create/
]