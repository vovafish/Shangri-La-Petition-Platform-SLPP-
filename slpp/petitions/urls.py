from django.urls import path
from .views import petitions  # Import the view for listing petitions

urlpatterns = [
    path('', petitions, name='petition_list'),  # This will match /slpp/petitions/
]