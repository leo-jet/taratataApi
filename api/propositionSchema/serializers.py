from rest_framework import serializers
from api.models import PropositionSchema


class PropositionSchemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropositionSchema
        fields = '__all__'
        depth = 4

    def create(self, validated_data):
        proposition = PropositionSchema.objects.create(**validated_data)
        proposition.save()
        return proposition