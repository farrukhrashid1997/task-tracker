from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Ticket, TicketComment
from .tasks import send_ticket_assignment
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Ticket)
def track_ticket_assignment_changes(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_ticket = Ticket.objects.get(pk=instance.pk)
            instance._old_assigned_to_id = old_ticket.assigned_to_id
        except Ticket.DoesNotExist:
            instance._old_assigned_to_id = None
    else:
        instance._old_assigned_to_id = None

@receiver(post_save, sender=Ticket)
def handle_ticket_assignment(sender, instance, created, **kwargs):

    try:
        if created:            
            if instance.assigned_to:
                send_ticket_assignment.delay(instance.id, instance.assigned_to.id)
            
            clear_dashboard_cache()
            
        else:
            old_assigned_to_id = getattr(instance, '_old_assigned_to_id', None)
            current_assigned_to_id = instance.assigned_to.id if instance.assigned_to else None
            
            if old_assigned_to_id != current_assigned_to_id and current_assigned_to_id:
                send_ticket_assignment.delay(instance.id, current_assigned_to_id)
                clear_dashboard_cache()
    
    except Exception as e:
        logger.error(f"Error in ticket assignment signal for ticket {instance.id}: {str(e)}")

def clear_dashboard_cache():
    cache_keys = [
        'dashboard_summary',
        'ticket_status_stats', 
        'ticket_priority_stats'
    ]
    cache.delete_many(cache_keys)
