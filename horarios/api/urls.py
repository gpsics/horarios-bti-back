from django.urls import include, path
from rest_framework import routers
from horarios.api.views import ComponenteCurricularViewSet, ProfessorViewSet, TurmaViewSet, ListaHorariosComponente, ListaHorariosProfessor, ListaHorariosSemestre

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'componentes', ComponenteCurricularViewSet)
router.register(r'professores', ProfessorViewSet)
router.register(r'turmas', TurmaViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('horarios/professores/<int:pk>/', ListaHorariosProfessor.as_view()),
    path('horarios/componentes/<cod>/', ListaHorariosComponente.as_view()),
    path('horarios/semestre/<semestre>/', ListaHorariosSemestre.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]