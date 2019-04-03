from django_filters import rest_framework as filters
from api.models import Quizz


class QuizzFilter(filters.FilterSet):
    class Meta:
        model = Quizz
        fields = ('dateCreation', 'intitule')
