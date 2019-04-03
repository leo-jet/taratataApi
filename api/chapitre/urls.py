from rest_framework.routers import DefaultRouter
from .views import ChapitreClasseListView, ChapitreClasseViewSet, ChapitreClasseListSelect
from django.urls import path, include


urlpatterns = [
    path('list/', ChapitreClasseListView.as_view(), name='chapitre-list'),
    path('list_classe_select/', ChapitreClasseListSelect.as_view(), name='chapitre-list')
]

router = DefaultRouter()
router.register('', ChapitreClasseViewSet, basename='chapitre')

urlpatterns += router.urls