from rest_framework import serializers
from api.models import Enseignant
from django.contrib.auth.models import User


class EnseignantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Enseignant
        fields = ("username", "sexe", "ville", "quartier", "nom", "prenom", "dateNaissance", "lieuNaissance", "telephone", "email", "specialite", "situation")
        depth = 4