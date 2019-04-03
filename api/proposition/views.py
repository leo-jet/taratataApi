from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import PropositionSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Proposition, Question
from django_filters import rest_framework as filters
from .filters import PropositionFilter


class PropositionViewSet(viewsets.ModelViewSet):
    serializer_class = PropositionFilter
    queryset = Proposition.objects.all()
    filterset_fields = ('enonce',)

    def list(self, request):
        queryset = Proposition.objects.all()
        serializer = PropositionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Proposition.objects.all()
        proposition = get_object_or_404(queryset, pk=pk)
        serializer = PropositionSerializer(proposition)
        return Response(serializer.data)

    def create(self, request):
        serializer = PropositionSerializer(data=request.data, context={'request': request})
        idQuestion = request.data.get('idQuestion', None)
        status = 200
        message = None
        if serializer.is_valid() and idQuestion:
            proposition = serializer.save()
            question = Question.objects.filter(idQuestion=idQuestion).first()
            proposition.question = question
            proposition.save()
            return Response(PropositionSerializer(proposition, many=False).data)
        else:
            return Response(serializer.errors,
                            status=400)

    def update(self, request, pk=None):
        instance = Proposition.objects.filter(id=pk).first()
        serializer = PropositionSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = Proposition.objects.filter(idProposition=pk).first()
        instance.delete()
        return Response("Proposition bien supprime", status=201)


class PropositionListView(generics.ListAPIView):
    queryset = Proposition.objects.all()
    serializer_class = PropositionSerializer
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('proposition',)
    filterset_class = PropositionFilter