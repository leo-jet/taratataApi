from rest_framework.routers import DefaultRouter
from .views import SectionListView, SectionViewSet, SectionListSelect
from django.urls import path, include


urlpatterns = [
    path('list/', SectionListView.as_view(), name='section-list'),
    path('list_chapitre_select/', SectionListSelect.as_view(), name='section-list')
]

router = DefaultRouter()
router.register('', SectionViewSet, basename='section')

urlpatterns += router.urls