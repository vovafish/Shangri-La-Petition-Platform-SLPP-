from django.urls import path
from . import views

urlpatterns = [
    path('', views.petitions, name='petition_list'),  # This will match /slpp/petitions/
    path('create/', views.create_petition, name='create_petition'),  # This will match /slpp/petitions/create/
    path('sign/<int:petition_id>/', views.sign_petition, name='sign_petition'),  # This will match /slpp/petitions/sign/<petition_id>/
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/threshold/update/', views.update_threshold, name='update_threshold'),
    path('admin/petition/response/<int:petition_id>/', views.add_petition_response, name='add_petition_response'),  # This will match /slpp/petitions/sign/<petition_id>/
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
]