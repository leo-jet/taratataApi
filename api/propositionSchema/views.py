from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import PropositionSchemaSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import PropositionSchema, Question
from django_filters import rest_framework as filters
from .filters import PropositionSchemaFilter


class PropositionSchemaViewSet(viewsets.ModelViewSet):
    serializer_class = PropositionSchemaFilter
    queryset = PropositionSchema.objects.all()
    filterset_fields = ('annotation',)

    def list(self, request):
        queryset = PropositionSchema.objects.all()
        serializer = PropositionSchemaSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = PropositionSchema.objects.all()
        proposition = get_object_or_404(queryset, pk=pk)
        serializer = PropositionSchemaSerializer(proposition)
        return Response(serializer.data)

    def create(self, request):
        serializer = PropositionSchemaSerializer(data=request.data, context={'request': request})
        idQuestion = request.data.get('idQuestion', None)
        status = 200
        message = None
        if serializer.is_valid() and idQuestion:
            proposition = serializer.save()
            question = Question.objects.filter(idQuestion=idQuestion).first()
            proposition.question = question
            proposition.save()
            return Response(PropositionSchemaSerializer(proposition, many=False).data)
        else:
            return Response(serializer.errors,
                            status=400)

    def update(self, request, pk=None):
        instance = PropositionSchema.objects.filter(idPropositionSchema=pk).first()
        serializer = PropositionSchemaSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = PropositionSchema.objects.filter(idPropositionSchema=pk).first()
        instance.delete()
        return Response("PropositionSchema bien supprime", status=201)


class PropositionSchemaListView(generics.ListAPIView):
    queryset = PropositionSchema.objects.all()
    serializer_class = PropositionSchemaSerializer
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('annotation',)
    filterset_class = PropositionSchemaFilter