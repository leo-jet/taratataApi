from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import DevoirSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import *
from django_filters import rest_framework as filters
from .filters import DevoirFilter


class DevoirViewSet(viewsets.ModelViewSet):
    serializer_class = DevoirSerializer
    queryset = Devoir.objects.all()

    def list(self, request):
        queryset = Devoir.objects.all()
        serializer = DevoirSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Devoir.objects.all()
        devoir = get_object_or_404(queryset, pk=pk)
        serializer = DevoirSerializer(devoir)
        return Response(serializer.data)

    def create(self, request):
        serializer = DevoirSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            idChapitre = request.data.get("idChapitre", None)
            idClasse = request.data.get("idClasse", None)
            if idChapitre and idClasse:
                chapitre = ChapitreClasse.objects.filter(id=idChapitre).first()
                classe = Classe.objects.filter(idClass=idClasse).first()
                devoir = serializer.save()
                devoir.chapitre = chapitre
                devoir.classe = classe
                devoir.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=400)

    def update(self, request, pk=None):
        instance = Devoir.objects.filter(id=pk).first()
        serializer = DevoirSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = Devoir.objects.filter(id=pk).first()
        instance.delete()
        return Response("Devoir bien supprime", status=201)


class DevoirListView(generics.ListAPIView):
    queryset = Devoir.objects.all()
    serializer_class = DevoirSerializer
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('classe__idClass', 'chapitre__id')
    filterset_class = DevoirFilter