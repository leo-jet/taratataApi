from django_filters import rest_framework as filters
from api.models import PropositionSchema


class PropositionSchemaFilter(filters.FilterSet):
    class Meta:
        model = PropositionSchema
        fields = ('annotation',)
