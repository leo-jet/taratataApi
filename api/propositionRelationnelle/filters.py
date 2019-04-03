from django_filters import rest_framework as filters
from api.models import PropositionRelationnelle


class PropositionRelationnelleFilter(filters.FilterSet):
    class Meta:
        model = PropositionRelationnelle
        fields = ('enonceA', 'enonceB')
