# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services import fetch_data_from_mongo

@csrf_exempt
def get_data(request):
    if request.method == 'GET':
        data = fetch_data_from_mongo()
        return JsonResponse(data, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)

