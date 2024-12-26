from django.urls import path
from .views import petitions # Import your test view

urlpatterns = [
    path('', petitions, name='petitions'),  # Map the root of petitions to the petitions view
]
