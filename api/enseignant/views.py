from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import EnseignantSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import *


class EnseignantViewSet(viewsets.ModelViewSet):
    serializer_class = EnseignantSerializer
    queryset = Enseignant.objects.all()
    def list(self, request):
        queryset = Enseignant.objects.all()
        serializer = EnseignantSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Enseignant.objects.all()
        enseignant = get_object_or_404(queryset, pk=pk)
        serializer = EnseignantSerializer(enseignant)
        return Response(serializer.data)

    def create(self, request):
        serializer = EnseignantSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=400)

    def update(self, request, pk=None):
        instance = Enseignant.objects.filter(idEnseignant=pk).first()
        serializer = EnseignantSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = Enseignant.objects.filter(idEnseignant=pk).first()
        instance.delete()
        return Response("Enseignant bien supprime", status=201)

class EnseignantListView(generics.RetrieveAPIView):
    queryset = Enseignant.objects.all()
    serializer_class = EnseignantSerializer
    def list(self, request):
        queryset = self.get_queryset()
        serializer = EnseignantSerializer(queryset, many=True)
        return Response(serializer.data)