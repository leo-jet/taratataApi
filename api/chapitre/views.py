from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import ChapitreClasseSerializer, ChapitreClasseSerializerDetail
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import ChapitreClasse, Classe
from django_filters import rest_framework as filters
from .filters import ChapitreClasseFilter


class ChapitreClasseViewSet(viewsets.ModelViewSet):
    serializer_class = ChapitreClasseFilter
    queryset = ChapitreClasse.objects.all()

    def list(self, request):
        queryset = ChapitreClasse.objects.all()
        serializer = ChapitreClasseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ChapitreClasse.objects.all()
        chapitre = get_object_or_404(queryset, pk=pk)
        serializer = ChapitreClasseSerializerDetail(chapitre)
        return Response(serializer.data)

    def create(self, request):
        idClasse = request.data.get('idClasse', None)
        status = 200
        message = None
        if idClasse:
            serializer = ChapitreClasseSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                classe = Classe.objects.filter(idClass=idClasse).first()
                chapitre = serializer.save()
                chapitre.classe = classe
                chapitre.save()
                message = {'message': 'Chapitre creee'}
                status = 200
            else:
                message = serializer.errors
                status = 400
        else:
            status = 400
            print(request.data)
            message = request.data
        return Response(message, status=status)

    def update(self, request, pk=None):
        instance = ChapitreClasse.objects.filter(id=pk).first()
        serializer = ChapitreClasseSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = ChapitreClasse.objects.filter(id=pk).first()
        instance.delete()
        return Response("Chapitre bien supprime", status=201)


class ChapitreClasseListView(generics.ListAPIView):
    queryset = ChapitreClasse.objects.all()
    serializer_class = ChapitreClasseSerializer
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ChapitreClasseFilter


class ChapitreClasseListSelect(generics.ListCreateAPIView):
    queryset = ChapitreClasse.objects.all()
    def list(self, request):
        queryset = self.get_queryset()
        idClass = request.GET.get('idClass', None)
        chapitres = []
        if idClass:
            chapitresDB = queryset.filter(classe__idClass=idClass)
            for chapitre in chapitresDB:
                serializer = ChapitreClasseSerializerDetail(chapitre)
                chapitres.append({
                    "label": chapitre.titre,
                    "value": chapitre.id,
                    "data": serializer.data,

                })
            return Response(chapitres)
        else:
            return Response("Paramètres n'existe pas")