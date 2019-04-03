from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import PropositionRelationnelleSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import PropositionRelationnelle, Question
from django_filters import rest_framework as filters
from .filters import PropositionRelationnelleFilter


class PropositionRelationnelleViewSet(viewsets.ModelViewSet):
    serializer_class = PropositionRelationnelleFilter
    queryset = PropositionRelationnelle.objects.all()

    def list(self, request):
        queryset = PropositionRelationnelle.objects.all()
        serializer = PropositionRelationnelleSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = PropositionRelationnelle.objects.all()
        proposition = get_object_or_404(queryset, pk=pk)
        serializer = PropositionRelationnelleSerializer(proposition)
        return Response(serializer.data)

    def create(self, request):
        serializer = PropositionRelationnelleSerializer(data=request.data, context={'request': request})
        idQuestion = request.data.get('idQuestion', None)
        status = 200
        message = None
        if serializer.is_valid() and idQuestion:
            proposition = serializer.save()
            question = Question.objects.filter(idQuestion=idQuestion).first()
            proposition.question = question
            proposition.save()
            return Response(PropositionRelationnelleSerializer(proposition, many=False).data)
        else:
            return Response(serializer.errors,
                            status=400)

    def update(self, request, pk=None):
        instance = PropositionRelationnelle.objects.filter(idPropositionRelationnelle=pk).first()
        serializer = PropositionRelationnelleSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = PropositionRelationnelle.objects.filter(idPropositionRelationnelle=pk).first()
        instance.delete()
        return Response("Chapitre bien supprime", status=201)


class PropositionRelationnelleListView(generics.ListAPIView):
    queryset = PropositionRelationnelle.objects.all()
    serializer_class = PropositionRelationnelleSerializer
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('enonceA', 'enonceB')
    filterset_class = PropositionRelationnelleFilter