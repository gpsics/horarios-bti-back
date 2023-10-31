from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, GroupViewSet
from horarios.api.views import ComponenteCurricularViewSet, ProfessorViewSet, TurmaViewSet, ListaTurmasProfessor, ListaTurmasComponente, ListaTurmasSemestre, ListaHorariosComponente, ListaHorariosSemestre, ListaHorariosProfessor
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'componentes', ComponenteCurricularViewSet)
router.register(r'professores', ProfessorViewSet)
router.register(r'turmas', TurmaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('admin/', admin.site.urls),

    path('turmas/professores/<int:pk>/', ListaTurmasProfessor.as_view()),
    path('turmas/componentes/<cod>/', ListaTurmasComponente.as_view()),
    path('turmas/semestre/<semestre>/', ListaTurmasSemestre.as_view()),

    path('horarios/professores/<int:pk>/', ListaHorariosProfessor.as_view()),
    path('horarios/componentes/<cod>/', ListaHorariosComponente.as_view()),
    path('horarios/semestre/<semestre>/', ListaHorariosSemestre.as_view())
]

