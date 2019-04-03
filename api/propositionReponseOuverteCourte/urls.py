from rest_framework.routers import DefaultRouter
from .views import PropositionReponseOuverteCourteListView, PropositionReponseOuverteCourteViewSet
from django.urls import path, include


urlpatterns = [
    path('list/', PropositionReponseOuverteCourteListView.as_view(), name='propositionReponseOuverteCourteListView-list')
]

router = DefaultRouter()
router.register('', PropositionReponseOuverteCourteViewSet, basename='propositionReponseOuverteCourteListView')

urlpatterns += router.urls