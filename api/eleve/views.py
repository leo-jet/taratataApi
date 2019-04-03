from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import EleveSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import *
from django_filters import rest_framework as filters
from .filters import EleveFilter


class EleveViewSet(viewsets.ModelViewSet):
    serializer_class = EleveSerializer
    queryset = Eleve.objects.all()
    filterset_fields = ('nom', 'prenom')

    def list(self, request):
        queryset = Eleve.objects.all()
        serializer = EleveSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Eleve.objects.all()
        eleve = get_object_or_404(queryset, pk=pk)
        serializer = EleveSerializer(eleve)
        return Response(serializer.data)

    def create(self, request):
        serializer = EleveSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            myuser = {
                'username' : request.data.get("username"),
                'password' : request.data.get("password"),
            }
            serializer.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=400)

    def update(self, request, pk=None):
        print(pk, request.data)
        instance = Eleve.objects.filter(idEleve=pk).first()
        serializer = EleveSerializer(instance, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = Eleve.objects.filter(idEleve=pk).first()
        instance.delete()
        return Response("Eleve bien supprime", status=201)


class EleveListView(generics.ListAPIView):
    queryset = Eleve.objects.all()
    serializer_class = EleveSerializer
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('nom', 'prenom')
    filterset_class = EleveFilter