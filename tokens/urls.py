from django.urls import path
from tokens.views import generate_token, validate_token

urlpatterns = [
    path('', generate_token, name='token-generate'),
    path('validate/', validate_token, name='token-validate'),
]
