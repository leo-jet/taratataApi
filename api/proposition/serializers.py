from rest_framework import serializers
from api.models import Proposition


class PropositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proposition
        fields = '__all__'
        depth = 4

    def create(self, validated_data):
        proposition = Proposition.objects.create(**validated_data)
        proposition.save()
        return proposition