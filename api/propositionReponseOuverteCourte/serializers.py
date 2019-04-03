from rest_framework import serializers
from api.models import PropositionReponseOuverteCourte


class PropositionReponseOuverteCourteSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropositionReponseOuverteCourte
        fields = '__all__'
        depth = 4

    def create(self, validated_data):
        proposition = PropositionReponseOuverteCourte.objects.create(**validated_data)
        proposition.save()
        return proposition