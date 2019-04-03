from rest_framework.routers import DefaultRouter
from .views import PropositionSchemaListView, PropositionSchemaViewSet
from django.urls import path, include


urlpatterns = [
    path('list/', PropositionSchemaListView.as_view(), name='question-list')
]

router = DefaultRouter()
router.register('', PropositionSchemaViewSet, basename='question')

urlpatterns += router.urls