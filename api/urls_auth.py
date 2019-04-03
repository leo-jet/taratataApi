from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from django.urls import path
from .views_account import enregistrment, check_number, confirmation

urlpatterns = [
    path('obtain_token/', obtain_jwt_token),
    path('refresh_token/', refresh_jwt_token),
    path('verify_token/', verify_jwt_token),
    path('enregistrement/', enregistrment),
    path('confirmation/', confirmation),
    path('check_number/', check_number),
]