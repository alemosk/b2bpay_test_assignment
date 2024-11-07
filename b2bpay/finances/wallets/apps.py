from django.apps import AppConfig


class WalletsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'b2bpay.finances.wallets'

    def ready(self):
        import b2bpay.finances.wallets.subscribers  # noqa: F401
