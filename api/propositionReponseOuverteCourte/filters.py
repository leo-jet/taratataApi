from django_filters import rest_framework as filters
from api.models import PropositionReponseOuverteCourte


class PropositionReponseOuverteCourteFilter(filters.FilterSet):
    class Meta:
        model = PropositionReponseOuverteCourte
        fields = ('enonce',)
