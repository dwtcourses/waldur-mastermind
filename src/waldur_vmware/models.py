from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils import FieldTracker

from waldur_core.core import models as core_models
from waldur_core.structure import models as structure_models


class VMwareService(structure_models.Service):
    projects = models.ManyToManyField(
        structure_models.Project,
        related_name='+',
        through='VMwareServiceProjectLink'
    )

    class Meta:
        unique_together = ('customer', 'settings')
        verbose_name = _('VMware provider')
        verbose_name_plural = _('VMware providers')

    @classmethod
    def get_url_name(cls):
        return 'vmware'


class VMwareServiceProjectLink(structure_models.ServiceProjectLink):

    service = models.ForeignKey(VMwareService)

    class Meta(structure_models.ServiceProjectLink.Meta):
        verbose_name = _('VMware provider project link')
        verbose_name_plural = _('VMware provider project links')

    @classmethod
    def get_url_name(cls):
        return 'vmware-spl'


class VirtualMachineMixin(models.Model):
    class Meta:
        abstract = True

    guest_os = models.CharField(max_length=50, help_text=_('Defines the valid guest operating system '
                                                           'types used for configuring a virtual machine'))
    cores = models.PositiveSmallIntegerField(default=0, help_text=_('Number of cores in a VM'))
    cores_per_socket = models.PositiveSmallIntegerField(default=1, help_text=_('Number of cores in a VM'))
    ram = models.PositiveIntegerField(default=0, help_text=_('Memory size in MiB'))


@python_2_unicode_compatible
class VirtualMachine(VirtualMachineMixin,
                     core_models.RuntimeStateMixin,
                     structure_models.NewResource):
    service_project_link = models.ForeignKey(
        VMwareServiceProjectLink,
        related_name='+',
        on_delete=models.PROTECT
    )

    class RuntimeStates(object):
        POWERED_OFF = 'POWERED_OFF'
        POWERED_ON = 'POWERED_ON'
        SUSPENDED = 'SUSPENDED'

    disk = models.PositiveIntegerField(default=0, help_text=_('Disk size in MiB'))
    template = models.ForeignKey('Template', null=True, on_delete=models.SET_NULL)
    tracker = FieldTracker()

    @classmethod
    def get_url_name(cls):
        return 'vmware-virtual-machine'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Disk(structure_models.NewResource):
    service_project_link = models.ForeignKey(
        VMwareServiceProjectLink,
        related_name='+',
        on_delete=models.PROTECT
    )

    size = models.PositiveIntegerField(help_text=_('Size in MiB'))
    vm = models.ForeignKey(VirtualMachine, related_name='disks')

    @classmethod
    def get_url_name(cls):
        return 'vmware-disk'

    def __str__(self):
        return self.name

    @classmethod
    def get_backend_fields(cls):
        return super(Disk, cls).get_backend_fields() + ('name', 'size')


@python_2_unicode_compatible
class Template(VirtualMachineMixin,
               core_models.DescribableMixin,
               structure_models.ServiceProperty):
    created = models.DateTimeField()
    modified = models.DateTimeField()

    @classmethod
    def get_url_name(cls):
        return 'vmware-template'

    def __str__(self):
        return self.name