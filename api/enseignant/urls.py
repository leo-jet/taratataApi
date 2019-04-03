from rest_framework.routers import DefaultRouter
from .views import EnseignantListView, EnseignantViewSet
from django.urls import path, include
from api.models import Eleve

urlpatterns = [
    path('list/', EnseignantListView.as_view(), name='enseignant-list'),
]

router = DefaultRouter()
router.register('', EnseignantViewSet, basename='enseignant')

urlpatterns += router.urls