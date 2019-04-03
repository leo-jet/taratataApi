from rest_framework import serializers
from api.models import Eleve
from django.contrib.auth.models import User


class EleveSerializer(serializers.ModelSerializer):
    classes = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Eleve
        fields = ("idEleve", "username", "nom", "prenom", "ville", "quartier", "email", "dateNaissance", "lieuNaissance", "classes", "solde", "telephone")
        depth = 4

    def create(self, validated_data):
        eleve = Eleve.objects.create(**validated_data)
        username = self.context["request"].data.get("username")
        password = self.context["request"].data.get("password")
        email = self.context["request"].data.get("email")
        if username and password and email:
            user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)
            eleve.user = user
            eleve.save()
        else:
            print(username, email, password)
        return eleve

