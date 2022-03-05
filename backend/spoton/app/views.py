from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from app import responses
from app.models import Booking, Message
from app.serializers import BookingSerializer, MessageSerializer
import json

# GLOBAL VARIABLES
API_KEY = "7dff77adf49dbf87535842af0ca96b20"    # access key to API 
BASE_URL = 'http://api.aviationstack.com/v1/'
username = ''

@api_view(['GET'])
def identify_user(request):
    global username

    print("IDENTIFY USER")
    username = request.GET['username']
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def message(request):

    global username

    message = request.GET['msg']
    user_msg_obj = Message(msg=message,is_me=True,type="normal",username=username)
    user_msg_obj.save()

    bot_response = responses.generate_response(message)
    bot_msg_obj = Message(msg=bot_response, is_me=False, type="normal", username=username)
    bot_msg_obj.save()

    return Response(bot_response)


@api_view(['GET'])
def user_messages(request):
    username = request.GET['username']
    try:
        messages = Message.objects.filter(username=username)
        print(messages)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_bookings(request):
    username = request.GET['username']
    try:
        bookings = Booking.objects.get(username=username)
    except Booking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


# ################################################# OBTER TODOS OS VOOS ########################################################
@api_view(['GET'])
def get_flights(request):
    
    url = BASE_URL + 'flights?access_key='+ API_KEY

    resp = requests.get(url=url)
    data = resp.json()

    return Response(data)


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


@api_view(['GET'])
def get_flights_by_departure(request):
    
    # ALTERAR AQUI
    departureCity = "Porto"
    
    cities = get_cities()
    
    iata_code = cities[departureCity]

    # get all flights according the departure iata code given
    url = BASE_URL + 'flights?access_key='+ API_KEY +'&dep_iata='+ iata_code

    resp = requests.get(url=url)
    data = resp.json()
    
    data = [flight for flight in data['data'] if flight["flight_status"] == "scheduled" ]   # filter scheduled flights 

    return Response(data)


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


    
