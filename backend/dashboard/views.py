from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from django.core.cache import cache
from tickets.models import Ticket

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ticket_status_stats(request):
    cache_key = 'ticket_status_stats'
    data = cache.get(cache_key)
    if data:
        return Response(data)
    status_stats = Ticket.objects.values('status').annotate(count=Count('status'))
    data = {}
    for stat in status_stats:
        data[stat['status']] = stat['count']

    all_status = [choice[0] for choice in Ticket.STATUS_CHOICES]
    result = {}
    for status in all_status:
        result[status] = data.get(status, 0)
    
    final_result = {
        'status_distribution': result, 
        'total_tickets': sum(result.values())
    }
    cache.set(cache_key, final_result, timeout=180)
    return Response({
        'status_distribution': result, 
        'total_tickets': sum(result.values())
    })
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ticket_priority_stats(request):
    cache_key = 'ticket_priority_stats'
    data = cache.get(cache_key)
    if data:
        return Response(data)
    priority_stats = Ticket.objects.values('priority').annotate(count=Count('priority'))
    data = {}
    for stat in priority_stats:
        data[stat['priority']] = stat['count']

    all_priorities = [choice[0] for choice in Ticket.PRIORITY_CHOICES]
    result = {}
    for priority in all_priorities:
        result[priority] = data.get(priority, 0)
    final_result = {
        'priority_distribution': result, 
        'total_tickets': sum(result.values())
    }
    cache.set(cache_key, final_result, timeout=180)
    return Response(final_result)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):    
    cache_key = 'dashboard_summary'
    data = cache.get(cache_key)
    if data:
        return Response(data)
    total_tickets = Ticket.objects.count()
    open_tickets = Ticket.objects.filter(status='open').count()
    in_progress_tickets = Ticket.objects.filter(status='in_progress').count()
    closed_tickets = Ticket.objects.filter(status='closed').count()
    
    high_priority = Ticket.objects.filter(priority='high').count()
    

    unassigned = Ticket.objects.filter(assigned_to__isnull=True).count()

    final_result = {
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'in_progress_tickets': in_progress_tickets,
        'closed_tickets': closed_tickets,
        'high_priority_tickets': high_priority,
        'unassigned_tickets': unassigned
    }
    cache.set(cache_key, final_result, timeout=180)


    return Response(final_result)