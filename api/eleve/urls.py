from rest_framework.routers import DefaultRouter
from .views import EleveViewSet, EleveListView
from django.urls import path

urlpatterns = [
    path('list/', EleveListView.as_view(), name='eleve-list')
]

router = DefaultRouter()
router.register('', EleveViewSet, basename='eleve')

urlpatterns += router.urls