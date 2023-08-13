from django.http import JsonResponse
from django.core.management import call_command
from .models import Report

def trigger_report(request):
    call_command('calculations')  # Call your management command
    return JsonResponse({'message': 'Calculation command triggered successfully'})
def get_report(request, report_id):
    try:
        report = Report.objects.get(report_id=report_id)
        return JsonResponse({'report_id': report_id, 'status': report.status})
    except Report.DoesNotExist:
        return JsonResponse({'report_id': report_id, 'status': 'Report not found'})