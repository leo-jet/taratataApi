from rest_framework import serializers
from api.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    questionquiz = serializers.ReadOnlyField()
    class Meta:
        model = Question
        fields = ('idQuestion', 'enonce', 'explication', 'type', 'numero', 'partie', 'image', 'questionquiz')
        depth = 4

    def create(self, validated_data):
        question = Question.objects.create(**validated_data)
        question.save()
        return question


class QuestionMobileSerializer(serializers.ModelSerializer):
    propositions = serializers.ReadOnlyField()
    class Meta:
        model = Question
        fields = ('idQuestion', 'enonce', 'explication', 'type', 'numero', 'partie', 'image', 'propositions')
        depth = 4

    def create(self, validated_data):
        question = Question.objects.create(**validated_data)
        question.save()
        return question