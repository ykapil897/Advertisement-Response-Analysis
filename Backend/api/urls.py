from django.urls import path
from .views import get_data, get_chart, get_custom_chart, index, get_chart_names

urlpatterns = [
    path('', index, name='index'),
    path('data/', get_data, name='get_data'),
    path('chart/', get_chart, name='get_chart'),
    path('customchart/', get_custom_chart, name='get_custom_chart'),
    path('chartnames/', get_chart_names, name='get_chart_names'),
]
