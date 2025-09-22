# backend/tickets/tests/test_models.py
import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from tickets.models import Ticket, TicketComment
from django.utils import timezone


@pytest.mark.django_db
class TestTicketModel:
    """Test cases for the Ticket model"""
    

    def test_create_ticket_with_all_fields(self):
        """Test creating a ticket with all fields populated"""
        creator = User.objects.create_user(username='creator', email='creator@example.com')
        assignee = User.objects.create_user(username='assignee', email='assignee@example.com')
        
        ticket = Ticket.objects.create(
            title='Complete Ticket',
            description='Full description',
            priority='high',
            status='in_progress',
            assigned_to=assignee,
            created_by=creator
        )
        
        assert ticket.title == 'Complete Ticket'
        assert ticket.priority == 'high'
        assert ticket.status == 'in_progress'
        assert ticket.assigned_to == assignee
        assert ticket.created_by == creator

    def test_ticket_priority_choices(self):
        user = User.objects.create_user(username='testuser', email='test@example.com')
        
        # Valid priorities
        for priority in ['low', 'medium', 'high']:
            ticket = Ticket.objects.create(
                title=f'Ticket {priority}',
                description='Test',
                priority=priority,
                created_by=user
            )
            assert ticket.priority == priority

    def test_ticket_status_choices(self):
        user = User.objects.create_user(username='testuser', email='test@example.com')
        
        # Valid statuses
        for status in ['open', 'in_progress', 'closed']:
            ticket = Ticket.objects.create(
                title=f'Ticket {status}',
                description='Test',
                status=status,
                created_by=user
            )
            assert ticket.status == status

   

@pytest.mark.django_db
class TestTicketCommentModel:
    def test_create_comment(self):
        user = User.objects.create_user(username='testuser', email='test@example.com')
        ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test description',
            created_by=user
        )
        
        comment = TicketComment.objects.create(
            ticket=ticket,
            author=user,
            content='This is a test comment'
        )
        
        assert comment.ticket == ticket
        assert comment.author == user
        assert comment.content == 'This is a test comment'
        assert comment.created_at is not None
