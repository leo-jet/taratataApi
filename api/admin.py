from django.contrib import admin
from .models import *

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('idEnseignant', 'nom', 'prenom', 'telephone', 'email', 'specialite')

@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ('idEleve', 'nom', 'prenom', 'telephone', 'email', 'dateNaissance')

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('idClass', 'nom', 'prix', 'dateDebut', 'dateFin', 'dateFinInscription', 'matiere', 'niveau')


@admin.register(EnseigneAClasse)
class EnseigneAClasseAdmin(admin.ModelAdmin):
    def get_enseignant(self, obj):
        return "{} {}".format(obj.enseignant.nom, obj.enseignant.prenom)
    def get_classe(self, obj):
        return "{}".format(obj.classe.nom)
    list_display = ('get_enseignant', 'get_classe')

@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    def nom_eleve(self, obj):
        return "{} {}".format(obj.eleve.nom, obj.eleve.prenom)
    def classe(self, obj):
        return obj.classe.nom
    list_display = ("nom_eleve", "classe")


@admin.register(ChapitreClasse)
class ChapitreClasseAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'dateDebut', 'dateFin', 'numero')


@admin.register(Devoir)
class DevoirAdmin(admin.ModelAdmin):
    pass



@admin.register(DemandeInscription)
class DemandeInscriptionAdmin(admin.ModelAdmin):
    pass

@admin.register(Quizz)
class QuizzAdmin(admin.ModelAdmin):
    list_display = ('idQuizz', 'dateCreation', 'dateFin', 'createur')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass



@admin.register(PropositionSchema)
class PropositionSchemaAdmin(admin.ModelAdmin):
    pass



@admin.register(RepondA)
class RepondAAdmin(admin.ModelAdmin):
    pass