from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import SectionSerializer, SectionSerializerDetail
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Section, ChapitreClasse
from django_filters import rest_framework as filters
from .filters import SectionFilter


class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionFilter
    queryset = Section.objects.all()

    def list(self, request):
        queryset = Section.objects.all()
        serializer = SectionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Section.objects.all()
        section = get_object_or_404(queryset, pk=pk)
        serializer = SectionSerializerDetail(section)
        return Response(serializer.data)

    def create(self, request):
        idChapitre = request.data.get('idChapitre', None)
        status = 200
        message = None
        if idChapitre:
            serializer = SectionSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                chapitre = ChapitreClasse.objects.filter(id=idChapitre).first()
                section = serializer.save()
                section.chapitre = chapitre
                section.save()
                message = {'message': 'Section creee'}
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
        instance = Section.objects.filter(id=pk).first()
        serializer = SectionSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = Section.objects.filter(id=pk).first()
        instance.delete()
        return Response("Section bien supprime", status=201)


class SectionListView(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SectionFilter


class SectionListSelect(generics.ListCreateAPIView):
    queryset = Section.objects.all()
    def list(self, request):
        queryset = self.get_queryset()
        idChapitre = request.GET.get('idChapitre', None)
        sectionsBD = []
        sections = []
        if idChapitre:
            sectionsBD = queryset.filter(chapitre__id=idChapitre)
            for section in sectionsBD:
                sections.append({
                    "label": section.intitule,
                    "value": section.id,
                    "data": SectionSerializerDetail(section).data
                })
        return Response(sections)