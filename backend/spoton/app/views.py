from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
import requests
from django.http import HttpResponse


# Create your views here.

BASE_URL = 'http://api.aviationstack.com/v1/'

# get all flights

@api_view(['GET'])
def get_flights(request):
    
    url = BASE_URL + 'flights?access_key=614368392936bf785327dd2d8157fb5a'

    resp = requests.get(url=url)
    data = resp.json()
    print(data)

    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['GET'])
def get_flight(request,flight_id):
    
    url = BASE_URL + 'flights?access_key=614368392936bf785327dd2d8157fb5a'

    resp = requests.get(url=url)
    data = resp.json()
    print(data)

    return Response(data)

@api_view(['GET'])
def get_flights_by_ArrivalCity(request, arrivalCity):
    
    url = BASE_URL + 'flights?access_key=614368392936bf785327dd2d8157fb5a'

    resp = requests.get(url=url)
    data = resp.json()
    print(data)

    return Response(data)

@api_view(['GET'])
def get_city(request):
    
    url = BASE_URL + 'cities?access_key=614368392936bf785327dd2d8157fb5a'

    resp = requests.get(url=url)
    data = resp.json()

    return Response(data)

    
