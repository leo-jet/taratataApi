from rest_framework import serializers
from api.models import Classe, EnseigneAClasse


class ClasseSerializer(serializers.ModelSerializer):

    enseignants = serializers.ReadOnlyField()
    eleves = serializers.ReadOnlyField()
    chapitres = serializers.ReadOnlyField()

    class Meta:
        model = Classe
        fields = '__all__'
        depth = 4

    def create(self, validated_data):
        classe = Classe.objects.create(**validated_data)
        classe.save()
        return classe

class ClasseListSerializerFilteredEnseignant(serializers.ModelSerializer):
    enseignants = serializers.ReadOnlyField(source='classe.enseignants')
    class Meta:
        model = EnseigneAClasse
        fields = ('classe', 'enseignants')
        depth = 4

    def create(self, validated_data):
        classe = Classe.objects.create(**validated_data)
        classe.save()
        return classe


class ClasseEleveSerializer(serializers.ModelSerializer):
    eleves = serializers.ReadOnlyField()

    class Meta:
        model = Classe
        fields = ('eleves','nom', 'idClass')
        depth = 4

    def create(self, validated_data):
        classe = Classe.objects.create(**validated_data)
        classe.save()
        return classe


class ClasseMobileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classe
        fields = ("idClass", "description", "nom", "prix", "dateDebut", "dateFin", "dateFinInscription", "logo", "tags", "matiere", "niveau")
        depth = 4

    def create(self, validated_data):
        classe = Classe.objects.create(**validated_data)
        classe.save()
        return classe