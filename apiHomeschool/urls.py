"""apiHomeschool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('connexion/', include('api.urls_auth')),
    path('eleve/', include('api.eleve.urls')),
    path('enseignant/', include('api.enseignant.urls')),
    path('classe/', include('api.classe.urls')),
    path('chapitre/', include('api.chapitre.urls')),
    path('section/', include('api.section.urls')),
    path('reponda/', include('api.reponda.urls')),
    path('quiz/', include('api.quiz.urls')),
    path('question/', include('api.question.urls')),
    path('proposition/', include('api.proposition.urls')),
    path('propositionschema/', include('api.propositionSchema.urls')),
    path('devoir/', include('api.devoir.urls')),
    path('propositionROC/', include('api.propositionReponseOuverteCourte.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
