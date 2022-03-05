from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
import requests
from django.http import HttpResponse
from app import responses

import json

# GLOBAL VARIABLES
API_KEY = "7dff77adf49dbf87535842af0ca96b20"    # access key to API 
BASE_URL = 'http://api.aviationstack.com/v1/' 



@api_view(['GET'])
def message(request):

    message = request.GET['msg']
    print(message)
    
    bot_response = responses.generate_response(message)

    print(bot_response)

    return Response(bot_response)


# ################################################# OBTER TODOS OS VOOS ########################################################

def get_flights():
    
    url = BASE_URL + 'flights?access_key='+ API_KEY

    resp = requests.get(url=url)
    data = resp.json()

    return data


# ########################################## OBTER UM DETERMINADO VOO ########################################################
@api_view(['GET'])
def get_flight(request):
    
    # ALTERAR AQUI!
    flight_iata = "AC9231"
    
    url = BASE_URL + 'flights?access_key='+ API_KEY +"&flight_iata="+ flight_iata       # get data from API to get a specific flight details

    resp = requests.get(url=url)
    data = resp.json()

    data = [ flight for flight in data['data'] if flight["flight_status"] == "scheduled" ]  # filter scheduled flights 
    
    return Response(data)


# ########################### OBTER VOOS DADAS AS CIDADES DE PARTIDA OU DE CHEGADA OU AMBAS #####################################
@api_view(['GET'])
def get_flights_by_arrival(request):
    
    # ALTERAR AQUI
    arrivalCity = "Porto"
    
    cities = get_cities()
    
    # get iata code of our arrival city and use it to search on the url
    iata_code = cities[arrivalCity]

    # get all flights according the arrival iata code given
    url = BASE_URL + 'flights?access_key='+ API_KEY +'&arr_iata='+ iata_code

    resp = requests.get(url=url)
    data = resp.json()
    
    data = [flight for flight in data['data'] if flight["flight_status"] == "scheduled" ]   # filter scheduled flights 

    return Response(data)

def get_flights_by_departure(departureCity):
    
    
    cities = get_cities()
    
    iata_code = cities[departureCity]

    # get all flights according the departure iata code given
    url = BASE_URL + 'flights?access_key='+ API_KEY +'&dep_iata='+ iata_code

    resp = requests.get(url=url)
    data = resp.json()
    
    data = [flight for flight in data['data'] if flight["flight_status"] == "scheduled" ]   # filter scheduled flights 
    
    return json.dumps(data)


@api_view(['GET'])
def get_flights_by_arr_dep(request):
    
    # ALTERAR AQUI
    departureCity = "Porto"
    arrivalCity = "Frankfurt"
    
    cities = get_cities()
    
    iata_code_dep = cities[departureCity]
    iata_code_arr = cities[arrivalCity]

    # get all flights according the departure and arrival iata code given
    url = BASE_URL + 'flights?access_key='+ API_KEY +'&dep_iata='+ iata_code_dep + '&arr_iata='+ iata_code_arr

    resp = requests.get(url=url)
    data = resp.json()
    
    data = [flight for flight in data['data'] if flight["flight_status"] == "scheduled" ]   # filter scheduled flights 

    return Response(data)


 # return a dictionary of all cities and their respective iata code
def get_cities():
     # the file 'cities.json' have all cities' data of API 
    with open('cities.json') as json_file:
        data = json.load(json_file)
        
    all_cities = data['data']
    return { city['city_name'] : city['iata_code'] for city in all_cities }


# ########################## OBTER UM DICIONÁRIO COM AS COORDENADAS GEOGRÁFICAS DOS AEROPORTOS ################################
@api_view(['GET'])
def get_airports(request):
    
    # get all airports on only one page
    url = BASE_URL + 'airports?access_key='+ API_KEY +'&limit=100000'

    resp = requests.get(url=url)
    data = resp.json()
    airports = data['data']
    
    # dictionary of all airports and their respective geographic coordinates
    coords_airports = { airport['airport_name'] : (airport['latitude'], airport['longitude']) for airport in airports }

    return Response(coords_airports)


    
