from django_filters import rest_framework as filters
from api.models import Section


class SectionFilter(filters.FilterSet):
    class Meta:
        model = Section
        fields = ('intitule', 'numero', )