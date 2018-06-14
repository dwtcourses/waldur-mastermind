from __future__ import unicode_literals

from waldur_mastermind.marketplace import views


def register_in(router):
    router.register(r'marketplace-service-providers', views.ServiceProviderViewSet,
                    base_name='marketplace-service-provider'),
    router.register(r'marketplace-categories', views.CategoryViewSet,
                    base_name='marketplace-category'),