from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
import requests
from django.http import HttpResponse
from app import responses

import json

# GLOBAL VARIABLES
API_KEY = "7dff77adf49dbf87535842af0ca96b20"
BASE_URL = 'http://api.aviationstack.com/v1/'



@api_view(['GET'])
def message(request):

    message = request.GET['msg']
    print(message)
    
    bot_response = responses.generate_response(message)

    print(bot_response)

    return Response(bot_response)


# ################################################# OBTER TODOS OS VOOS ########################################################
@api_view(['GET'])
def get_flights(request):
    
    url = BASE_URL + 'flights?access_key='+ API_KEY

    resp = requests.get(url=url)
    data = resp.json()
    print(data)

    return HttpResponse("Hello, world. You're at the polls index.")


# ########################################## OBTER UM DETERMINADO VOO ########################################################
@api_view(['GET'])
def get_flight(request):
    
    # ALTERAR AQUI!
    flight_iata = "AC9231"
    
    url = BASE_URL + 'flights?access_key='+ API_KEY +"&flight_iata="+ flight_iata

    resp = requests.get(url=url)
    data = resp.json()

    data = [ fligth for fligth in data['data'] if fligth["flight_status"] == "scheduled" ]
    
    return Response(data)


# ########################### OBTER VOOS DADAS AS CIDADES DE PARTIDA OU DE CHEGADA OU AMBAS #####################################
@api_view(['GET'])
def get_flights_by_arrival(request):
    
    # ALTERAR AQUI
    arrivalCity = "Porto"
    
    with open('cities.json') as json_file:
        data = json.load(json_file)
        
    all_cities = data['data']
    
    cities = { city['city_name'] : city['iata_code'] for city in all_cities }
    
    iata_code = cities[arrivalCity]

    url = BASE_URL + 'flights?access_key='+ API_KEY +'&arr_iata='+ iata_code

    resp = requests.get(url=url)
    data = resp.json()
    
    data = [fligth for fligth in data['data'] if fligth["flight_status"] == "scheduled" ]

    return Response(data)


@api_view(['GET'])
def get_flights_by_departure(request):
    
    # ALTERAR AQUI
    departureCity = "Porto"
    
    with open('cities.json') as json_file:
        data = json.load(json_file)
        
    all_cities = data['data']
    
    cities = { city['city_name'] : city['iata_code'] for city in all_cities }
    
    iata_code = cities[departureCity]

    url = BASE_URL + 'flights?access_key='+ API_KEY +'&dep_iata='+ iata_code

    resp = requests.get(url=url)
    data = resp.json()
    
    data = [fligth for fligth in data['data'] if fligth["flight_status"] == "scheduled" ]

    return Response(data)


@api_view(['GET'])
def get_flights_by_arr_dep(request):
    
    # ALTERAR AQUI
    departureCity = "Porto"
    arrivalCity = "Frankfurt"
    
    with open('cities.json') as json_file:
        data = json.load(json_file)
        
    all_cities = data['data']
    
    cities = { city['city_name'] : city['iata_code'] for city in all_cities }
    
    iata_code_dep = cities[departureCity]
    iata_code_arr = cities[arrivalCity]

    url = BASE_URL + 'flights?access_key='+ API_KEY +'&dep_iata='+ iata_code_dep + '&arr_iata='+ iata_code_arr

    resp = requests.get(url=url)
    data = resp.json()
    
    data = [fligth for fligth in data['data'] if fligth["flight_status"] == "scheduled" ]

    return Response(data)



# ########################## OBTER UM DICIONÁRIO COM AS COORDENADAS GEOGRÁFICAS DOS AEROPORTOS ################################
@api_view(['GET'])
def get_airports(request):
    
    url = BASE_URL + 'airports?access_key='+ API_KEY +'&limit=100000'

    resp = requests.get(url=url)
    data = resp.json()
    
    airports = data['data']
    coords_airports = { airport['airport_name'] : (airport['latitude'], airport['longitude']) for airport in airports }

    return Response(coords_airports)


# #########################################################################################################################
@api_view(['GET'])
def get_city(request):
    
    url = BASE_URL + 'cities?access_key='+ API_KEY

    resp = requests.get(url=url)
    data = resp.json()

    return Response(data)

    
