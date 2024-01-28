from django.apps import AppConfig


class HorariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'horarios'

    def ready(self, *args, **kwargs) -> None:
        import horarios.signals
        super_ready = super().ready(*args, **kwargs)
        return super_ready
