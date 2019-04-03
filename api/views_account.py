from api.enseignant.serializers import EnseignantSerializer
from api.eleve.serializers import EleveSerializer
from api.classe.serializers import ClasseMobileSerializer
from api.section.serializers import SectionSerializer
from api.devoir.serializers import DevoirMobileSerializer
from api.question.serializers import QuestionMobileSerializer
from .models import Enseignant, Eleve, Classe, Section, Devoir, Question
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .sms import SMSRobot
from random import randint

def jwt_response_payload_handler(token, user=None, request=None):
    print(request.user_agent)
    groups = []
    mesclasses = []
    chapitres = []
    devoirs = []
    myuser = None
    sections = []
    questions = []
    myQuestions = []
    mobile = request.POST.get("mobile", None)
    for g in user.groups.all():
        groups.append(g.name)
    if 'enseignant' in groups:
        enseignant = Enseignant.objects.filter(user=user).first()
        myuser = EnseignantSerializer(enseignant).data
    else:
        eleve = Eleve.objects.filter(user=user).first()
        myuser = EleveSerializer(eleve).data
        if mobile:
            idClassesList = [classe['idClasse'] for classe in myuser['classes']]
            classes = Classe.objects.filter(idClass__in=idClassesList)
            for classe in classes:
                chapitres = chapitres + classe.chapitres
            idChapitreList = [chapitre['id'] for chapitre in chapitres]
            sectionsDB = Section.objects.filter(chapitre_id__in=idChapitreList)
            devoirDB = Devoir.objects.filter(chapitre_id__in=idChapitreList)
            devoirs = DevoirMobileSerializer(devoirDB, many=True).data
            for devoir in devoirs:
                numQuestions = devoir['numeroDesQuestions'].split(";")
                questionsDB = Question.objects.filter(idQuestion__in=numQuestions)
                tmp = QuestionMobileSerializer(questionsDB, many=True).data
                questions = questions + [quest for quest in tmp if quest not in questions]

            sections = SectionSerializer(sectionsDB, many=True).data
            mesclasses = ClasseMobileSerializer(classes, many=True).data
            myQuestions = questionParserForMobile(questions)
        else:
            mesclasses = myuser['classes']
    return {
        'token': token,
        'user': myuser,
        'classes': mesclasses,
        'chapitres': chapitres,
        'sections': sections,
        'devoirs': devoirs,
        'questions': myQuestions
    }

def questionParserForMobile(questions):
    myQuestions = []
    for question in questions:
        if question["type"] == "schema":
            propositions = []
            for proposition in question["propositions"]:
                propositions.append({
                    "id": proposition["id"],
                    "enonce": proposition["numero"],
                    "label": proposition["reponse"],
                    "value": proposition["reponse"],
                    "proposition": None,
                    "solution": proposition["reponse"]
                })
            myQuestions.append({
                "id": question["idQuestion"],
                "enonce": question["image"],
                "type": question["type"],
                "propositions": {
                    "type": "croquis",
                    "lists": propositions
                }
            })
        if question["type"] == "qcm":
            propositions = []
            for proposition in question["propositions"]:
                propositions.append({
                    "id": proposition["id"],
                    "checked": False,
                    "enonce": proposition["enonce"],
                    "solution": proposition["solution"]
                })
            myQuestions.append({
                "id": question["idQuestion"],
                "enonce": question["enonce"],
                "type": question["type"],
                "propositions": {
                    "type": "qcm",
                    "lists": propositions
                }
            })
        if question["type"] == "qr":
            propositions = []
            enonce = []
            for proposition in question["propositions"]:
                propositions.append({
                    "id": proposition["id"],
                    "enonce": proposition["enonceA"],
                    "proposition": None,
                    "solution": proposition["enonceB"]
                })
                enonce.append({
                    "label": proposition["enonceB"],
                    "value": proposition["enonceB"]
                })
            myQuestions.append({
                "id": question["idQuestion"],
                "enonce": enonce,
                "type": question["type"],
                "propositions": {
                    "type": "qr",
                    "lists": propositions
                }
            })
    return myQuestions

@csrf_exempt
def enregistrment(request):
    message = ""
    status = 200
    problemeSolde = False
    reste = 0
    if request.method == 'POST':
        nom = request.POST.get("nom", None)
        prenom = request.POST.get("prenom", None)
        numero = request.POST.get("numero", None)
        motpass = request.POST.get("pass", None)
        if numero and prenom and nom and motpass:
            eleve = Eleve.objects.filter(telephone=numero).first()
            if not eleve:
                premier_nom = nom.split(' ')[0]
                premier_prenom = prenom.split(' ')[0]
                username = "{}.{}".format(premier_prenom[0].lower(), premier_nom.lower())
                user = User.objects.filter(username=username).first()
                if user:
                    username += ".1"
                user, created = User.objects.get_or_create(
                    username=username
                )
                if created:
                    user.is_active = True
                    user.is_superuser = True
                    user.first_name = nom
                    user.set_password(motpass)
                    user.last_name = prenom
                    user.save()
                    eleve = Eleve()
                    eleve.user = user
                    eleve.nom = nom
                    eleve.telephone = numero
                    eleve.prenom = prenom
                    eleve.active = False
                    sms = SMSRobot()
                    code = randint(1000, 9999)
                    eleve.code = code
                    envoi = sms.send_message(destinataire=numero, message=str(code))
                    print(envoi.status, envoi.date_sent, envoi.price)
                    eleve.save()
                    message = "Elève bien crée"
                else:
                    status = 404
                    message = "L'utilisateur existe déjà"
            else:
                status = 404
                message = "L'utilisateur existe déjà"
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

@csrf_exempt
def check_number(request):
    message = "L'élève existe"
    status = 200
    numeroExiste = True
    if request.method == 'POST':
        numero = request.POST.get("numero", None)
        if numero:
            eleve = Eleve.objects.filter(telephone=numero).first()
            if not eleve:
                message = "L'élève n'existe pas"
                numeroExiste = False
        else:
            status = 404
            message = "Il manque un parametre"
    else:
        status = 404
        message = "Cette méthode n'est pas autorisée"
    data = {
        "message": message,
        "numeroExiste": numeroExiste,
    }
    return JsonResponse(
            status=status, data=data)

@csrf_exempt
def confirmation(request):
    message = ""
    status = 200
    problemeSolde = False
    error = 0
    if request.method == 'POST':
        username = request.POST.get("username", None)
        code = request.POST.get("code", None)
        if code and username:
            eleve = Eleve.objects.filter(user__username=username, code=code).first()
            if eleve:
                eleve.active = True
                eleve.save()
                message = "Compte validé"
            else:
                status = 404
                erreur = 1
                message = "Code  ou identifiant incorrect!"
        else:
            status = 404
            message = "Il manque un parametre"
    else:
        status = 404
        message = "Cette méthode n'est pas autorisée"
    data = {
        "message": message,
        "erreur": 1
    }
    return JsonResponse(
            status=status, data=data)
