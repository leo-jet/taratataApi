from rest_framework.routers import DefaultRouter
from .views import DevoirViewSet,DevoirListView
from django.urls import path, include
from api.models import Eleve

urlpatterns = [
    path('list/',DevoirListView.as_view(), name='devoir-list'),
    path('list_filtered/',DevoirListView.as_view(), name='devoir-list-filtered')
]

router = DefaultRouter()
router.register('',DevoirViewSet, basename='devoir')

urlpatterns += router.urls