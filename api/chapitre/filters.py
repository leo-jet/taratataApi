from django_filters import rest_framework as filters
from api.models import ChapitreClasse


class ChapitreClasseFilter(filters.FilterSet):
    class Meta:
        model = ChapitreClasse
        fields = ('classe__idClass',)