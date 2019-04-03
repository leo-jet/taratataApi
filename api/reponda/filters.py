from django_filters import rest_framework as filters
from api.models import RepondA


class RepondAFilter(filters.FilterSet):
    class Meta:
        model = RepondA
        fields = ('quizz__idQuizz',)