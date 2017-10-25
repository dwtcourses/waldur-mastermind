from django.utils import timezone

from nodeconductor_assembly_waldur.invoices import registrators as invoices_registrators

from .log import event_logger
from . import models


def log_expert_request_creation(sender, instance, created=False, **kwargs):
    if not created:
        return

    event_logger.waldur_expert_request.info(
        'User {user_username} with full name {user_full_name} has created '
        'request for experts under {customer_name} / {project_name}.',
        event_type='expert_request_created',
        event_context={
            'expert_request': instance,
        })


def log_expert_request_state_changed(sender, instance, created=False, **kwargs):
    if created:
        return

    if not instance.tracker.has_changed('state'):
        return

    if instance.state == models.ExpertRequest.States.ACTIVE:
        event_logger.waldur_expert_request.info(
            'Expert request {expert_request_name} has been activated.',
            event_type='expert_request_activated',
            event_context={
                'expert_request': instance,
            })
    elif instance.state == models.ExpertRequest.States.CANCELLED:
        event_logger.waldur_expert_request.info(
            'Expert request {expert_request_name} has been cancelled.',
            event_type='expert_request_cancelled',
            event_context={
                'expert_request': instance,
            })
    elif instance.state == models.ExpertRequest.States.COMPLETED:
        event_logger.waldur_expert_request.info(
            'Expert request {expert_request_name} has been completed.',
            event_type='expert_request_completed',
            event_context={
                'expert_request': instance,
            })


def log_expert_bid_creation(sender, instance, created=False, **kwargs):
    if not created:
        return

    event_logger.waldur_expert_bid.info(
        'User {user_username} with full name {user_full_name} has created '
        'bid for request {request_name} under {customer_name} / {project_name}.',
        event_type='expert_bid_created',
        event_context={
            'expert_bid': instance,
        })


def add_completed_expert_request_to_invoice(sender, instance, created=False, **kwargs):
    if created:
        return

    state = instance.state
    if state != models.ExpertRequest.States.COMPLETED or state == instance.tracker.previous('state'):
        return

    if not instance.issue or not hasattr(instance, 'contract'):
        return

    invoices_registrators.RegistrationManager.register(instance, timezone.now())


def terminate_invoice_when_expert_request_deleted(sender, instance, **kwargs):
    invoices_registrators.RegistrationManager.terminate(instance, timezone.now())


def set_project_name_on_expert_request_creation(sender, instance, created=False, **kwargs):
    if created:
        request = instance
        request.project_name = request.project.name
        request.project_uuid = request.project.uuid.hex
        request.customer = request.project.customer
        request.save(update_fields=('project_name', 'project_uuid', 'customer'))


def update_expert_request_on_project_name_update(sender, instance, **kwargs):
    project = instance
    if project.tracker.has_changed('name'):
        models.ExpertRequest.objects.filter(project=project).update(project_name=project.name)


def set_team_name_on_expert_contract_creation(sender, instance, created=False, **kwargs):
    if created:
        contract = instance
        contract.team_name = contract.team.name
        contract.team_uuid = contract.team.uuid.hex
        contract.team_customer = contract.team.customer
        contract.save(update_fields=('team_name', 'team_uuid', 'team_customer'))


def update_expert_contract_on_project_name_update(sender, instance, **kwargs):
    project = instance
    if project.tracker.has_changed('name'):
        models.ExpertContract.objects.filter(team=project).update(team_name=project.name)