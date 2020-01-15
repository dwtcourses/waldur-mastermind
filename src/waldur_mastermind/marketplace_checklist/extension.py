from waldur_core.core import WaldurExtension


class MarketplaceChecklistExtension(WaldurExtension):

    @staticmethod
    def django_app():
        return 'waldur_mastermind.marketplace_checklist'

    @staticmethod
    def is_assembly():
        return True

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in
