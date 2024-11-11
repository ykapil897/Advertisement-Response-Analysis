# views.py
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services import fetch_data_from_mongo, create_ad_topic_percentage_plot

@csrf_exempt
def get_data(request):
    if request.method == 'GET':
        data = fetch_data_from_mongo(collection_name="survey_respondents")  
        return JsonResponse(data, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_chart(request):
    if request.method == 'GET':
        buf = create_ad_topic_percentage_plot()
        return HttpResponse(buf, content_type='image/png')

    return HttpResponse(status=405)