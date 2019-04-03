from rest_framework import serializers
from api.models import ChapitreClasse


class ChapitreClasseSerializer(serializers.ModelSerializer):
    devoirs = serializers.ReadOnlyField()
    sections = serializers.ReadOnlyField()
    class Meta:
        model = ChapitreClasse
        fields = ('id', 'sections', 'titre', 'numero', 'dateDebut', 'dateFin', 'description', 'contenuFichier', 'contenuVideo', 'devoirs')
        depth = 4

    def create(self, validated_data):
        chapitre = ChapitreClasse.objects.create(**validated_data)
        chapitre.save()
        return chapitre

class ChapitreClasseSerializerDetail(serializers.ModelSerializer):
    devoirs = serializers.ReadOnlyField()
    sections = serializers.ReadOnlyField()
    class Meta:
        model = ChapitreClasse
        fields = ('id', 'sections', 'titre', 'numero', 'dateDebut', 'dateFin', 'description', 'contenuFichier', 'contenuVideo', 'devoirs')
        depth = 4

    def create(self, validated_data):
        chapitre = ChapitreClasse.objects.create(**validated_data)
        chapitre.save()
        return chapitre

class ChapitreClasseMobileSerializer(serializers.ModelSerializer):
    devoirs = serializers.ReadOnlyField()
    sections = serializers.ReadOnlyField()
    class Meta:
        model = ChapitreClasse
        fields = ('id', 'titre', 'numero', 'dateDebut', 'dateFin', 'description', 'contenuFichier', 'contenuVideo', '')
        depth = 4

    def create(self, validated_data):
        chapitre = ChapitreClasse.objects.create(**validated_data)
        chapitre.save()
        return chapitre