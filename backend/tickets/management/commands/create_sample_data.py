# backend/fixtures/sample_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tickets.models import Ticket, TicketComment
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample users
        users = []
        user_data = [
            ('john_doe', 'John', 'Doe', 'john@example.com'),
            ('jane_smith', 'Jane', 'Smith', 'jane@example.com'),
            ('bob_wilson', 'Bob', 'Wilson', 'bob@example.com'),
            ('alice_brown', 'Alice', 'Brown', 'alice@example.com'),
        ]
        
        for username, first_name, last_name, email in user_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'is_active': True,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {username}')
            users.append(user)
        
        # Create sample tickets
        ticket_templates = [
            {
                'title': 'Fix login authentication bug',
                'description': 'Users are unable to login with special characters in their passwords. This affects approximately 15% of our user base.',
                'priority': 'high',
                'status': 'open'
            },
            {
                'title': 'Update user dashboard design',
                'description': 'The current dashboard design is outdated and needs a modern refresh. Include new charts and better mobile responsiveness.',
                'priority': 'medium',
                'status': 'in_progress'
            },
            {
                'title': 'Database performance optimization',
                'description': 'Query performance has degraded on the user reports page. Need to optimize slow queries and add proper indexing.',
                'priority': 'high',
                'status': 'open'
            },
            {
                'title': 'Add email notification preferences',
                'description': 'Allow users to customize which email notifications they receive. Should include ticket assignments, comments, and status changes.',
                'priority': 'low',
                'status': 'closed'
            },
            {
                'title': 'Mobile app API endpoints',
                'description': 'Create REST API endpoints for the upcoming mobile application. Needs to support ticket creation, viewing, and commenting.',
                'priority': 'medium',
                'status': 'in_progress'
            },
            {
                'title': 'Security audit findings',
                'description': 'Address security vulnerabilities found in recent audit: input validation, SQL injection prevention, and XSS protection.',
                'priority': 'high',
                'status': 'open'
            },
            {
                'title': 'User feedback integration',
                'description': 'Integrate user feedback system with ticket creation. Allow users to submit feedback that automatically creates tickets.',
                'priority': 'low',
                'status': 'open'
            },
            {
                'title': 'Automated testing setup',
                'description': 'Set up comprehensive automated testing pipeline including unit tests, integration tests, and end-to-end testing.',
                'priority': 'medium',
                'status': 'closed'
            }
        ]
        
        created_tickets = []
        for i, template in enumerate(ticket_templates):
            # Vary creation times over last 30 days
            created_at = timezone.now() - timedelta(days=random.randint(1, 30))
            
            ticket = Ticket.objects.create(
                title=template['title'],
                description=template['description'],
                priority=template['priority'],
                status=template['status'],
                created_by=random.choice(users),
                assigned_to=random.choice(users) if random.random() > 0.3 else None,
                created_at=created_at,
                updated_at=created_at + timedelta(hours=random.randint(1, 48))
            )
            created_tickets.append(ticket)
            self.stdout.write(f'Created ticket: {ticket.title}')
        
        # Create sample comments
        comment_templates = [
            "I've started investigating this issue and found some interesting details.",
            "This looks related to the recent deployment. Let me check the logs.",
            "I think we should prioritize this for the next sprint.",
            "The fix is ready for testing. Can someone review it?",
            "This has been resolved. Closing the ticket.",
            "We need more information from the user who reported this.",
            "I've reproduced the issue locally. Working on a solution.",
            "This might be a duplicate of ticket #123. Should we merge them?",
            "The proposed solution looks good. Let's implement it.",
            "Testing completed successfully. Ready for deployment."
        ]
        
        for ticket in created_tickets:
            # Add 1-4 comments per ticket
            num_comments = random.randint(1, 4)
            for j in range(num_comments):
                comment_time = ticket.created_at + timedelta(
                    hours=random.randint(1, 72)
                )
                TicketComment.objects.create(
                    ticket=ticket,
                    author=random.choice(users),
                    content=random.choice(comment_templates),
                    created_at=comment_time
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {len(users)} users\n'
                f'- {len(created_tickets)} tickets\n'
                f'- Multiple comments per ticket'
            )
        )