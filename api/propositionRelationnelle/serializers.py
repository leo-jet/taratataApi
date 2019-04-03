from rest_framework import serializers
from api.models import PropositionRelationnelle


class PropositionRelationnelleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropositionRelationnelle
        fields = '__all__'
        depth = 4

    def create(self, validated_data):
        propositionRelationnelle = PropositionRelationnelle.objects.create(**validated_data)
        propositionRelationnelle.save()
        return propositionRelationnelle