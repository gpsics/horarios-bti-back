from django.urls import include, path
from rest_framework import routers
from horarios.api.views import ComponenteCurricularViewSet, ProfessorViewSet, TurmaViewSet, HorariosViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'componentes', ComponenteCurricularViewSet, basename='componente')
router.register(r'professores', ProfessorViewSet, basename='professor')
router.register(r'turmas', TurmaViewSet, basename='turma')

urlpatterns = [
    path('', include(router.urls)),

    path('horarios/professores/<int:id_prof>/', HorariosViewSet.as_view({'get': 'horarios_prof'}), name='horarios_prof'),
    path('horarios/componentes/<cod>/', HorariosViewSet.as_view({'get': 'horarios_comp'}), name='horarios_comp'),
    path('horarios/semestre/<semestre>/', HorariosViewSet.as_view({'get': 'horarios_semestre'}), name='horarios_semestre'),
    path('horarios/conflitos/', HorariosViewSet.as_view({'get': 'horarios_conflitos'}), name='horarios_conflitos'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]