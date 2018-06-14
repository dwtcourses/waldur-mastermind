from __future__ import unicode_literals

import six
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from waldur_core.core import models as core_models
from waldur_core.core.fields import JSONField
from waldur_core.structure import models as structure_models

from .attribute_types import ATTRIBUTE_TYPES


@python_2_unicode_compatible
class ServiceProvider(core_models.UuidMixin,
                      structure_models.TimeStampedModel):
    customer = models.OneToOneField(structure_models.Customer, related_name='+', on_delete=models.CASCADE)
    enable_notifications = models.BooleanField(default=True)

    class Meta(object):
        verbose_name = _('Service provider')

    def __str__(self):
        return six.text_type(self.customer)

    @classmethod
    def get_url_name(cls):
        return 'marketplace-service-provider'


@python_2_unicode_compatible
class Category(core_models.UuidMixin,
               structure_models.TimeStampedModel):
    title = models.CharField(blank=False, max_length=255)
    icon = models.ImageField(upload_to='marketplace_category_icons', blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta(object):
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return six.text_type(self.title)

    @classmethod
    def get_url_name(cls):
        return 'marketplace-category'


@python_2_unicode_compatible
class Section(structure_models.TimeStampedModel):
    key = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(blank=False, max_length=255)
    category = models.ForeignKey(Category, related_name='sections')

    def __str__(self):
        return six.text_type(self.title)


@python_2_unicode_compatible
class Attribute(structure_models.TimeStampedModel):
    key = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(blank=False, max_length=255)
    section = models.ForeignKey(Section, related_name='attributes')
    type = models.CharField(max_length=255, choices=ATTRIBUTE_TYPES)
    available_values = JSONField(blank=True, null=True)

    def __str__(self):
        return six.text_type(self.title)


@python_2_unicode_compatible
class Offering(core_models.UuidMixin, core_models.NameMixin,
               core_models.DescribableMixin, structure_models.TimeStampedModel):
    thumbnail = models.ImageField(upload_to='marketplace_service_offering_thumbnails', blank=True, null=True)
    full_description = models.TextField(blank=True)
    rating = models.IntegerField(default=0)
    category = models.ForeignKey(Category, related_name='offerings')
    provider = models.ForeignKey(ServiceProvider, related_name='offerings')
    features = JSONField(default=[])
    geolocations = JSONField(default=[], blank=True,
                             help_text=_('List of latitudes and longitudes. For example: '
                                         '[{"latitude": 123, "longitude": 345}, {"latitude": 456, "longitude": 678}]'))
    is_active = models.BooleanField(default=True)

    class Meta(object):
        verbose_name = _('Offering')

    def __str__(self):
        return six.text_type(self.name)

    @classmethod
    def get_url_name(cls):
        return 'marketplace-offering'