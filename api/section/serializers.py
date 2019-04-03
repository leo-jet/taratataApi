from rest_framework import serializers
from api.models import Section


class SectionSerializer(serializers.ModelSerializer):
    idChapitre = serializers.ReadOnlyField(source='chapitre.id')
    class Meta:
        model = Section
        fields = ('id', 'intitule', 'numero', 'contenuFichier', 'contenuVideo', 'idChapitre', 'contenu')
        depth = 4

    def create(self, validated_data):
        section = Section.objects.create(**validated_data)
        section.save()
        return section

class SectionSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'intitule', 'numero', 'contenuFichier', 'contenuVideo')
        depth = 4

    def create(self, validated_data):
        section = Section.objects.create(**validated_data)
        section.save()
        return section