from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
import requests
from django.http import HttpResponse

import json

# Create your views here.

key = "7dff77adf49dbf87535842af0ca96b20"

BASE_URL = 'http://api.aviationstack.com/v1/'

# get all flights

@api_view(['GET'])
def get_flights(request):
    
    url = BASE_URL + 'flights?access_key='+ key

    resp = requests.get(url=url)
    data = resp.json()
    print(data)

    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['GET'])
def get_flight(request,flight_id):
    
    url = BASE_URL + 'flights?access_key='+ key

    resp = requests.get(url=url)
    data = resp.json()

    return Response(data)

@api_view(['GET'])
def get_flights_by_ArrivalCity(request):
    
    # ALTERAR AQUI
    arrivalCity = "Porto"
    
    with open('cities.json') as json_file:
        data = json.load(json_file)
        
    all_cities = data['data']
    
    cities = { city['city_name'] : city['iata_code'] for city in all_cities }
    
    iata_code = cities[arrivalCity]

    url = BASE_URL + 'flights?access_key='+ key +'&arr_iata='+ iata_code

    resp = requests.get(url=url)
    data = resp.json()

    return Response(data)

@api_view(['GET'])
def get_city(request):
    
    url = BASE_URL + 'cities?access_key='+ key

    resp = requests.get(url=url)
    data = resp.json()

    return Response(data)

    
