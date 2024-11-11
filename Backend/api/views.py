# views.py
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from .services import fetch_data_from_mongo, create_all_charts

@csrf_exempt
def get_data(request):
    if request.method == 'GET':
        data = fetch_data_from_mongo(collection_name="survey_respondents")  
        return JsonResponse(data, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_chart(request):
    if request.method == 'GET':
        # Get all charts
        images = create_all_charts()
        return JsonResponse(images, safe=False)

    return HttpResponse(status=405)