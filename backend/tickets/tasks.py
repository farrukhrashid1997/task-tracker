from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import logging
from .models import Ticket

logger = logging.getLogger(__name__)
@shared_task(bind=True, retry_kwargs={'max_retries': 3, 'countdown': 60})
def send_ticket_assignment(self, ticket_id, assigned_user_id):
    try:
        ticket = Ticket.objects.select_related('created_by', 'assigned_to').get(id=ticket_id)
        assigned_user = User.objects.get(id=assigned_user_id)

        if not assigned_user.email:
            return "User has no email address"
        
        subject = f'New Ticket Assigned: {ticket.title}'
        message = f"""
            Hi {assigned_user.first_name or assigned_user.username},

            You have been assigned a new ticket:

            Title: {ticket.title}
            Priority: {ticket.get_priority_display()}
            Status: {ticket.get_status_display()}
            Created by: {ticket.created_by.get_full_name() or ticket.created_by.username}

            Description:
            {ticket.description}

            Please log in to the ticket system to view full details and start working on it.

            Best regards,
            Ticket System Team
                    """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[assigned_user.email],
            fail_silently=False,  # Raise exception if email fails
        )
        
    except Exception as exc:
        # Log the error for debugging
        logger.error(f"Failed to send assignment email for ticket {ticket_id}: {str(exc)}")
        # Retry the task (Celery will retry up to 3 times with 60 second delays)
        raise self.retry(exc=exc)



@shared_task(bind=True, retry_kwargs={'max_retries': 3, 'countdown': 60})
def send_ticket_comment_notification(self, ticket_id, comment_id, commenter_id):
    try:
        from .models import Ticket, TicketComment
        
        ticket = Ticket.objects.select_related('created_by', 'assigned_to').get(id=ticket_id)
        comment = TicketComment.objects.select_related('author').get(id=comment_id)
        commenter = User.objects.get(id=commenter_id)
        recipients = []
        if ticket.assigned_to and ticket.assigned_to.email and ticket.assigned_to != commenter:
            recipients.append(ticket.assigned_to)
        
        if (ticket.created_by and 
            ticket.created_by.email and 
            ticket.created_by != commenter and 
            ticket.created_by != ticket.assigned_to):
            recipients.append(ticket.created_by)
        
        if not recipients:
            logger.info(f"No recipients for comment notification on ticket {ticket_id}")
            return "No recipients found"
        
        subject = f'New Comment on Ticket: {ticket.title}'
        
        emails_sent = 0
        for recipient in recipients:
            message = f"""
Hi {recipient.first_name or recipient.username},

{commenter.get_full_name() or commenter.username} has added a comment to ticket "{ticket.title}":

"{comment.content}"

Ticket Details:
- Priority: {ticket.get_priority_display()}
- Status: {ticket.get_status_display()}
- Assigned to: {ticket.assigned_to.get_full_name() if ticket.assigned_to else 'Unassigned'}

Please log in to the ticket system to view the full conversation and respond if needed.

Best regards,
Ticket System Team
            """
            
            # Send email to this recipient
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            emails_sent += 1
        
        logger.info(f"Comment notification emails sent for ticket {ticket_id} to {emails_sent} recipients")
        return f"Email sent to {emails_sent} recipients"
        
    except Exception as exc:
        logger.error(f"Failed to send comment notification for ticket {ticket_id}: {str(exc)}")
        raise self.retry(exc=exc)