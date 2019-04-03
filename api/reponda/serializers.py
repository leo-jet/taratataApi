from rest_framework import serializers
from api.models import RepondA


class RepondASerializer(serializers.ModelSerializer):

    class Meta:
        model = RepondA
        fields = '__all__'
        depth = 4

    def create(self, validated_data):
        reponda = RepondA.objects.create(**validated_data)
        reponda.save()
        return reponda