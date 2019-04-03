from django_filters import rest_framework as filters
from api.models import Devoir


class DevoirFilter(filters.FilterSet):
    class Meta:
        model = Devoir
        fields = ('chapitre__id', 'titre')
