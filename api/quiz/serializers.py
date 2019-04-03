from rest_framework import serializers
from api.models import Quizz


class QuizzSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quizz
        fields = '__all__'
        depth = 4

    def create(self, validated_data):
        quiz = Quizz.objects.create(**validated_data)
        quiz.save()
        return quiz