from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import QuestionSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Question, Section
from django_filters import rest_framework as filters
from .filters import QuestionFilter
import json


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionFilter
    queryset = Question.objects.all()
    filterset_fields = ('session', 'type')

    def list(self, request):
        queryset = Question.objects.all()
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Question.objects.all()
        chapitre = get_object_or_404(queryset, pk=pk)
        serializer = QuestionSerializer(chapitre)
        return Response(serializer.data)

    def create(self, request):
        print("hello")
        print(request.FILES)
        print(request.data)
        serializer = QuestionSerializer(data=request.data, context={'request': request})
        idSection = request.data.get('idSection', None)
        status = 200
        message = None
        if serializer.is_valid() and idSection:
            section = Section.objects.filter(id=idSection).first()
            question = serializer.save()
            question.section = section
            question.chapitre = section.chapitre
            question.save()
            return Response(QuestionSerializer(question, many=False).data)
        else:
            return Response(serializer.errors,
                            status=400)

    def update(self, request, pk=None):
        instance = Question.objects.filter(idQuestion=pk).first()
        serializer = QuestionSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = Question.objects.filter(idQuestion=pk).first()
        instance.delete()
        return Response("Chapitre bien supprime", status=201)


class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('type', 'session')
    filterset_class = QuestionFilter


#Use when selecting tree
class QuestionListSelectView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    def list(self, request):
        queryset = self.get_queryset()
        selectionJson = request.GET.get("selections", None)
        if selectionJson:
            selections = json.loads(selectionJson)
            sectionID = [selection.split(";")[1] for selection in selections]
            questions = Question.objects.filter(section__id__in=sectionID)
        return Response(QuestionSerializer(questions, many=True))