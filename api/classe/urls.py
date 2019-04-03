from rest_framework.routers import DefaultRouter
from .views import ClasseViewSet, ClasseListView, ClasseListFilteredView, ClasseListSmallDetail, ClasseListSelect, ClasseListEleve, inscription_cours
from django.urls import path, include
from api.models import Eleve

urlpatterns = [
    path('list/', ClasseListView.as_view(), name='classe-list'),
    path('list_filtered/', ClasseListFilteredView.as_view(), name='classe-list-filtered'),
    #use to display tree in dialog/quiz.js
    path('list_small_detail/', ClasseListSmallDetail.as_view(), name='classe-list-filtered'),
    path('list_select/', ClasseListSelect.as_view(), name='classe-list-filtered'),
    path('list_select_with_eleve/', ClasseListEleve.as_view(), name='classe-list-filtered-with-eleve'),
    path('inscription/', inscription_cours),
]

router = DefaultRouter()
router.register('', ClasseViewSet, basename='classe')

urlpatterns += router.urls