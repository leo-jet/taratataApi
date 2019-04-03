from rest_framework.routers import DefaultRouter
from .views import QuizzListView, QuizzViewSet
from django.urls import path, include


urlpatterns = [
    path('list/', QuizzListView.as_view(), name='quizz-list')
]

router = DefaultRouter()
router.register('', QuizzViewSet, basename='quizz')

urlpatterns += router.urls