from rest_framework.routers import DefaultRouter
from .views import QuestionListView, QuestionViewSet, QuestionListSelectView
from django.urls import path, include


urlpatterns = [
    path('list/', QuestionListView.as_view(), name='question-list'),
    path('list_by_selection/', QuestionListSelectView.as_view(), name='question-list-by-selection')
]

router = DefaultRouter()
router.register('', QuestionViewSet, basename='question')

urlpatterns += router.urls