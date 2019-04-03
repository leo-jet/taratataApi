from rest_framework.routers import DefaultRouter
from .views import RepondAListView, RepondAViewSet
from django.urls import path, include


urlpatterns = [
    path('list/', RepondAListView.as_view(), name='reponda-list')
]

router = DefaultRouter()
router.register('', RepondAViewSet, basename='reponda')

urlpatterns += router.urls