from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, GroupViewSet
from horarios.views import ComponenteCurricularViewSet, ProfessorViewSet, TurmaViewSet, ListaTurmasProfessor, ListaTurmasComponente
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
    path('professores/<int:pk>/turmas/', ListaTurmasProfessor.as_view()),
    path('componentes/<pk>/turmas/', ListaTurmasComponente.as_view())
]

