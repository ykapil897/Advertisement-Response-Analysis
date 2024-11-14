# views.py
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .chart_services import fetch_data_from_mongo, create_all_charts
from .dyn_chart_services import create_custom_chart, get_chart_names_list
from django.shortcuts import render
import json
from .predict_services import predictions_cr_ctr, predictions_decision, get_dropdown_values

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')

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

@csrf_exempt
def get_chart_names(request):
    if request.method == 'GET':
        chart_names = get_chart_names_list()
        return JsonResponse(chart_names, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_custom_chart(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            chart_type = body.get('chart_type')
            # print(chart_type)
            if not chart_type:
                return JsonResponse({'error': 'No chart type provided'}, status=400)

            # Generate the chart based on the chart_type
            chart = create_custom_chart(chart_type)
            # print(chart[0]['title'])
            return JsonResponse(chart, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_predict(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            model_inputs = body.get('model_inputs')
            # print(chart_type)
            if not model_inputs:
                return JsonResponse({'error': 'No model_inputs provided'}, status=400)
            
            if model_inputs['Model'] == 'Model1':
                result = predictions_cr_ctr(model_inputs)
            else :
                result = predictions_decision(model_inputs)

            return JsonResponse(result, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
            
    elif request.method == 'GET':
        values = get_dropdown_values()
        return JsonResponse(values)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

