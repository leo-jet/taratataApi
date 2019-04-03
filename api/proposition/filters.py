from django_filters import rest_framework as filters
from api.models import Proposition


class PropositionFilter(filters.FilterSet):
    class Meta:
        model = Proposition
        fields = ('enonce',)