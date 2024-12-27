from django.urls import path
from .views import petitions, create_petition, sign_petition  # Import the sign_petition view

urlpatterns = [
    path('', petitions, name='petition_list'),  # This will match /slpp/petitions/
    path('create/', create_petition, name='create_petition'),  # This will match /slpp/petitions/create/
    path('sign/<int:petition_id>/', sign_petition, name='sign_petition'),  # This will match /slpp/petitions/sign/<petition_id>/
]