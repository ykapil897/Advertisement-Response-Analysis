from django.shortcuts import render
from django.http import JsonResponse

def test_view(request):
    data = {
        'message': 'Hello from Django backend!'
    }
    return JsonResponse(data)

# Create your views here.
