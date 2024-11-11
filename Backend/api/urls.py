from django.urls import path
from .views import get_data, get_chart

urlpatterns = [
    path('data/', get_data, name='get_data'),
    path('chart/', get_chart, name='get_chart'),
]
