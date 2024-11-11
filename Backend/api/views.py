# views.py
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from .services import fetch_data_from_mongo, create_ad_topic_percentage_plot

@csrf_exempt
def get_data(request):
    if request.method == 'GET':
        data = fetch_data_from_mongo(collection_name="survey_respondents")  
        return JsonResponse(data, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_chart(request):
    if request.method == 'GET':
        # Create the plot
        buf = create_ad_topic_percentage_plot()
        image_data = buf.getvalue()

        # Create a list of images with titles
        images = []
        for i in range(10):
            images.append({
                "title": f"Chart {i+1}",
                "image": base64.b64encode(image_data).decode('utf-8')
            })

        return JsonResponse(images, safe=False)

    return HttpResponse(status=405)