from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket, TicketComment


def ticket_to_dict(ticket):
    return {
        'id': ticket.id,
        'title': ticket.title,
        'description': ticket.description,
        'priority': ticket.priority,
        'status': ticket.status,
        'assigned_to': {
            'id': ticket.assigned_to.id,
            'username': ticket.assigned_to.username,
            'first_name': ticket.assigned_to.first_name,
            'last_name': ticket.assigned_to.last_name,
        } if ticket.assigned_to else None,
        'created_by': {
            'id': ticket.created_by.id,
            'username': ticket.created_by.username,
            'first_name': ticket.created_by.first_name,
            'last_name': ticket.created_by.last_name,
        },
        'created_at': ticket.created_at.isoformat(),
        'updated_at': ticket.updated_at.isoformat(),
    }


def comment_to_dict(comment):
    return {
        'id': comment.id,
        'content': comment.content,
        'author': {
            'id': comment.author.id,
            'username': comment.author.username,
            'first_name': comment.author.first_name,
            'last_name': comment.author.last_name,
        },
        'created_at': comment.created_at.isoformat(),
    }

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tickets(request):
    tickets = Ticket.objects.all().order_by('-created_at')
    ticket_data = [ticket_to_dict(ticket) for ticket in tickets]
    return Response({'results': ticket_data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ticket(request):
    data = request.data
    ticket = Ticket.objects.create(
        title=data.get('title'), 
        description=data.get("description"),
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'open'),
        created_by=request.user
    )

    assigned_to_id = data.get('assigned_to_id')
    if assigned_to_id:
        try:
            assigned_user = User.objects.get(id=assigned_to_id)
            ticket.assigned_to = assigned_user
            ticket.save()
        except User.DoesNotExist:
            pass
    
    return Response(ticket_to_dict(ticket), status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

    ticket_data = ticket_to_dict(ticket)
    comments = ticket.comments.all().order_by('created_at')
    ticket_data['comments'] = [comment_to_dict(comment) for comment in comments]
    return Response(ticket_data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data
    ticket.title = data['title']
    ticket.description = data['description']
    ticket.priority = data['priority']
    ticket.status = data['status']
    
    assigned_to_id = data["assigned_to_id"]
    if assigned_to_id:
        try:
            assigned_user = User.objects.get(id=assigned_to_id)
            ticket.assigned_to = assigned_user
        except User.DoesNotExist:
            pass
    else:
        ticket.assigned_to = None
    
    ticket.save()
    return Response(ticket_to_dict(ticket))


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
    
    ticket.delete()
    return Response({'message': 'Ticket deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = User.objects.all().order_by('username')
    user_data = [{
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    } for user in users]
    return Response({'results': user_data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data
    comment = TicketComment.objects.create(
        ticket=ticket,
        author=request.user,
        content=data.get('content')
    )
    
    return Response(comment_to_dict(comment), status=status.HTTP_201_CREATED)