from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import RepondASerializer
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import RepondA, Devoir
from django_filters import rest_framework as filters
from .filters import RepondAFilter


class RepondAViewSet(viewsets.ModelViewSet):
    serializer_class = RepondAFilter
    queryset = RepondA.objects.all()
    filterset_fields = ('enonce',)

    def list(self, request):
        queryset = RepondA.objects.all()
        serializer = RepondASerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = RepondA.objects.all()
        proposition = get_object_or_404(queryset, pk=pk)
        serializer = RepondASerializer(proposition)
        return Response(serializer.data)

    def create(self, request):
        serializer = RepondASerializer(data=request.data, context={'request': request})
        idDevoir = request.data.get('idDevoir', None)
        status = 200
        message = None
        if serializer.is_valid() and idDevoir:
            reponda = serializer.save()
            reponda.utilisateur = request.user
            devoir = Devoir.objects.filter(id=idDevoir).first()
            if devoir:
                reponda.quizz = devoir.quizz
            reponda.save()
            return Response(RepondASerializer(reponda, many=False).data)
        else:
            return Response(serializer.errors,
                            status=400)

    def update(self, request, pk=None):
        instance = RepondA.objects.filter(id=pk).first()
        serializer = RepondASerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = RepondA.objects.filter(idProposition=pk).first()
        instance.delete()
        return Response("RepondA bien supprime", status=201)


class RepondAListView(generics.ListAPIView):
    queryset = RepondA.objects.all()
    serializer_class = RepondASerializer
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('proposition',)
    filterset_class = RepondAFilter