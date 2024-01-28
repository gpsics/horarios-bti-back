from .models import ComponenteCurricular

class ComponenteCurricularService:
    @staticmethod
    def validate_semestre_obrigatorio(semestre, obrigatorio):
        # Verifica se o componente é obrigatório com semestre igual a 0
        if int(semestre) == 0 and obrigatorio:
            return {"num_semestre": "O componente quando obrigatório deve possuir um semestre diferente de 0."}