from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def ping(request):
    data = {
        "id": 1,
        "name": "item"
    }
    return JsonResponse(data)