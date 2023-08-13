from django.http import JsonResponse
from django.shortcuts import render

import random
import string

def trigger_report(request):
    # Generate a random report ID and store it in the session
    report_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    request.session['report_id'] = report_id

    return JsonResponse({'report_id': report_id})

def get_report(request):
    report_id = request.GET.get('report_id')
    
    if report_id:
        stored_report_id = request.session.get('report_id')
        if stored_report_id and report_id == stored_report_id:
            # If the report ID matches, return status as "Complete"
            return JsonResponse({'status': 'Complete'})
    # If no report ID or mismatch, return status as "Running"
    return JsonResponse({'status': 'Running'})
