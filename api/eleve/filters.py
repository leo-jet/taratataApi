from django_filters import rest_framework as filters
from api.models import Eleve


class EleveFilter(filters.FilterSet):
    class Meta:
        model = Eleve
        fields = ('nom', 'prenom')
