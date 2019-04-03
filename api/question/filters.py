from django_filters import rest_framework as filters
from api.models import Question


class QuestionFilter(filters.FilterSet):
    class Meta:
        model = Question
        fields = {
            'idQuestion': ['in'],
        }
