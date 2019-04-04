from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import ClasseSerializer, ClasseListSerializerFilteredEnseignant, ClasseEleveSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from api.models import *
from django_filters import rest_framework as filters
from .filters import ClasseFilter
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny


class ClasseViewSet(viewsets.ModelViewSet):
    serializer_class = ClasseSerializer
    queryset = Classe.objects.all()
    filterset_fields = ('nom', 'prix', 'matiere', 'niveau', 'dateDebut', 'dateFin', 'dateFinInscription')

    def list(self, request):
        queryset = Classe.objects.all()
        serializer = ClasseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Classe.objects.all()
        classe = get_object_or_404(queryset, pk=pk)
        serializer = ClasseSerializer(classe)
        return Response(serializer.data)

    def create(self, request):
        serializer = ClasseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            enseignant = Enseignant.objects.filter(user=request.user).first()
            classe = serializer.save()
            enseignantA = EnseigneAClasse()
            enseignantA.classe = classe
            enseignantA.enseignant = enseignant
            enseignantA.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=400)

    def update(self, request, pk=None):
        instance = Classe.objects.filter(idClass=pk).first()
        serializer = ClasseSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = Classe.objects.filter(idClass=pk).first()
        instance.delete()
        return Response("Classe bien supprime", status=201)


class ClasseListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ClasseFilter


class ClasseListFilteredView(generics.ListCreateAPIView):
    queryset = EnseigneAClasse.objects.all()
    serializer_class = ClasseListSerializerFilteredEnseignant
    def list(self, request):
        queryset = self.get_queryset()
        classes = queryset.filter(enseignant__user=request.user)
        serializer = ClasseListSerializerFilteredEnseignant(classes, many=True)
        return Response(serializer.data)

class ClasseListSmallDetail(generics.ListCreateAPIView):
    queryset = EnseigneAClasse.objects.all()
    serializer_class = ClasseListSerializerFilteredEnseignant
    def list(self, request):
        queryset = self.get_queryset()
        classes = queryset.filter(enseignant__user=request.user)
        quasarClasses = []
        for classeEnseigneA in classes:
            classe = classeEnseigneA.classe
            quasarChapitres = []
            chapitres = ChapitreClasse.objects.filter(classe=classe)
            for chapitre in chapitres:
                quasarSections = []
                sections = Section.objects.filter(chapitre=chapitre)
                for section in sections:
                    quasarSections.append({
                        "label": section.intitule,
                        "icon": "fas fa-hand-point-right",
                        "id": "Section;{}".format(section.id)
                    })
                quasarChapitres.append({
                    "label": chapitre.titre,
                    "id": "Chapitre;{}".format(chapitre.id),
                    "icon": "fas fa-list-alt",
                    "children": quasarSections
                })
            quasarClasses.append({
                "label": classe.nom,
                "id": "Classe;{}".format(classe.idClass),
                "icon": "fas fa-chalkboard-teacher",
                "children": quasarChapitres
            })
        return Response(quasarClasses)


class ClasseListSelect(generics.ListCreateAPIView):
    queryset = EnseigneAClasse.objects.all()
    serializer_class = ClasseListSerializerFilteredEnseignant
    def list(self, request):
        queryset = self.get_queryset()
        classes = queryset.filter(enseignant__user=request.user)
        quasarClasses = []
        for classeEnseigneA in classes:
            classe = classeEnseigneA.classe
            quasarClasses.append({
                "label": classe.nom,
                "value": classe.idClass
            })
        return Response(quasarClasses)


class ClasseListEleve(generics.ListCreateAPIView):
    queryset = EnseigneAClasse.objects.all()
    serializer_class = ClasseEleveSerializer
    def list(self, request):
        queryset = self.get_queryset()
        classes = [eclasse.classe for eclasse in queryset.filter(enseignant__user=request.user)]
        serializer = ClasseEleveSerializer(classes, many=True)
        return Response(serializer.data)

@csrf_exempt
def inscription_cours(request):
    message = ""
    status = 200
    problemeSolde = False
    reste = 0
    if request.method == 'POST':
        username = request.POST.get("username", None)
        idClasse = request.POST.get("idClasse", None)
        if idClasse and username:
            eleve = Eleve.objects.filter(user__username=username).first()
            print(eleve, username)
            classe = Classe.objects.filter(idClass=idClasse).first()
            if eleve.solde >= classe.prix:
                inscription = Inscription()
                inscription.classe = classe
                inscription.eleve = eleve
                inscription.save()
                data = {
                    "message": "inscrition reussie"
                }
                eleve.solde -= classe.prix
                eleve.save()
            else:
                status = 404
                reste = classe.prix - eleve.solde
                problemeSolde = True
                message = "Votre solde est insuffisant pour vous inscrire à ce cours"
        else:
            status = 404
            message = "Il manque un parametre"
    else:
        status = 404
        message = "Cette méthode n'est pas autorisée"
    data = {
        "message": message,
        "problemeSolde": problemeSolde,
        "reste": reste
    }
    return JsonResponse(
            status=status, data=data)