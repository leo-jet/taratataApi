from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import QuizzSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Quizz
from django_filters import rest_framework as filters
from .filters import QuizzFilter


class QuizzViewSet(viewsets.ModelViewSet):
    serializer_class = QuizzFilter
    queryset = Quizz.objects.all()
    filterset_fields = ('intitule', 'dateCreation')

    def list(self, request):
        queryset = Quizz.objects.all()
        serializer = QuizzSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Quizz.objects.all()
        quiz = get_object_or_404(queryset, pk=pk)
        serializer = QuizzSerializer(quiz)
        return Response(serializer.data)

    def create(self, request):
        serializer = QuizzSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Quiz creee'})
        else:
            return Response(serializer.errors,
                            status=400)

    def update(self, request, pk=None):
        instance = Quizz.objects.filter(idQuizz=pk).first()
        serializer = QuizzSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = Quizz.objects.filter(idQuizz=pk).first()
        instance.delete()
        return Response("Quiz bien supprime", status=201)


class QuizzListView(generics.ListAPIView):
    queryset = Quizz.objects.all()
    serializer_class = QuizzSerializer
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('intitule', 'dateCreation')
    filterset_class = QuizzFilter