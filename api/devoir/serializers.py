from rest_framework import serializers
from api.models import Devoir


class DevoirSerializer(serializers.ModelSerializer):
    """idClass = serializers.CharField(source='classe.idClass')
    idChapitre = serializers.CharField(source='chapitre.id')
    id__Quizz = serializers.CharField(source='quizz.idQuizz')"""
    class Meta:
        model = Devoir
        fields = '__all__'
        depth = 4

    def create(self, validated_data):
        devoir = Devoir.objects.create(**validated_data)
        devoir.save()
        return devoir


class DevoirMobileSerializer(serializers.ModelSerializer):
    idClass = serializers.CharField(source='classe.idClass')
    idChapitre = serializers.CharField(source='chapitre.id')
    class Meta:
        model = Devoir
        fields = ("dateDebut", "dateFin", "duree", "nombreEssai", "correction", "consignes", "numeroDesQuestions", "titre", "idClass", "idChapitre")
        depth = 4

    def create(self, validated_data):
        devoir = Devoir.objects.create(**validated_data)
        devoir.save()
        return devoir