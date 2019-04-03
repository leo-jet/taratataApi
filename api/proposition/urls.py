from rest_framework.routers import DefaultRouter
from .views import PropositionListView, PropositionViewSet
from django.urls import path, include


urlpatterns = [
    path('list/', PropositionListView.as_view(), name='proposition-list')
]

router = DefaultRouter()
router.register('', PropositionViewSet, basename='proposition')

urlpatterns += router.urls