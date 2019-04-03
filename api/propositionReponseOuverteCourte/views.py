from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import PropositionReponseOuverteCourteSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import PropositionReponseOuverteCourte
from django_filters import rest_framework as filters
from .filters import PropositionReponseOuverteCourteFilter


class PropositionReponseOuverteCourteViewSet(viewsets.ModelViewSet):
    serializer_class = PropositionReponseOuverteCourteFilter
    queryset = PropositionReponseOuverteCourte.objects.all()

    def list(self, request):
        queryset = PropositionReponseOuverteCourte.objects.all()
        serializer = PropositionReponseOuverteCourteSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = PropositionReponseOuverteCourte.objects.all()
        proposition = get_object_or_404(queryset, pk=pk)
        serializer = PropositionReponseOuverteCourteSerializer(proposition)
        return Response(serializer.data)

    def create(self, request):
        serializer = PropositionReponseOuverteCourteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'PropositionReponseOuverteCourte creee'})
        else:
            return Response(serializer.errors,
                            status=400)

    def update(self, request, pk=None):
        instance = PropositionReponseOuverteCourte.objects.filter(idPopositionQROC=pk).first()
        serializer = PropositionReponseOuverteCourteSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = PropositionReponseOuverteCourte.objects.filter(idPopositionQROC=pk).first()
        instance.delete()
        return Response("PropositionReponseOuverteCourte bien supprime", status=201)


class PropositionReponseOuverteCourteListView(generics.ListAPIView):
    queryset = PropositionReponseOuverteCourte.objects.all()
    serializer_class = PropositionReponseOuverteCourteSerializer
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('enonce',)
    filterset_class = PropositionReponseOuverteCourteFilter