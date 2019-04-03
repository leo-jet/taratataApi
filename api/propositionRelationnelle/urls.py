from rest_framework.routers import DefaultRouter
from .views import PropositionRelationnelleListView, PropositionRelationnelleViewSet
from django.urls import path, include


urlpatterns = [
    path('list/', PropositionRelationnelleListView.as_view(), name='propositionRelationnelle-list')
]

router = DefaultRouter()
router.register('', PropositionRelationnelleViewSet, basename='propositionRelationnelle')

urlpatterns += router.urls