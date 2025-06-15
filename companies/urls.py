from django.urls import path
from companies.views import register_company


urlpatterns = [
    path('register/', register_company, name='company-register'),
]
