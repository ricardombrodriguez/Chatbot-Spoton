from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from app import responses
from app.models import Booking, Message
from app.serializers import BookingSerializer, MessageSerializer
import json
import numpy

# GLOBAL VARIABLES
API_KEY = "723aba823e2308bdaa21430ea6efa485"    # access key to API 
BASE_URL = 'http://api.aviationstack.com/v1/'
username = ''

@api_view(['GET'])
def identify_user(request):
    global username

    print("IDENTIFY USER")
    username = request.GET['username']
    request.user.username = username
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def message(request):

    global username

    message = request.GET['msg']
    user_msg_obj = Message(body=message,is_me=True,tag="normal",username=username)
    user_msg_obj.save()

    # bot_response = responses.generate_response(message)
    # bot_msg_obj = Message(msg=bot_response, is_me=False, type="normal", username=username)
    # bot_msg_obj.save()

    bot_response = json.loads(responses.generate_response(message,username))
   
    bot_msg_obj = Message(body=bot_response['body'], is_me=False, tag=bot_response['tag'], username=username)

    bot_msg_obj.save()  

    print(bot_msg_obj, "sou o obj")
    print("sou o bot response 1", bot_response)
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


# ########################## OBTER AEROPORTO MAIS PRÓXIMO DAS COORDENADAS DO UTILIZADOR (DISTÂNCIA EUCLIDIANA) ################################

@api_view(['GET'])
def get_nearest_airport(request):

    latitude = request.GET['latitude']
    longitude = request.GET['longitude']
    user_coords = numpy.array((float(latitude),float(longitude)))
    airports_coords = get_airports()

    nearest_aiport = ''
    nearest_distance = 1000000

    for airport,coords in airports_coords.items():
        if coords[0] is None or coords[1] is None:
            continue
        airport_coords = numpy.array((float(coords[0]),float(coords[1])))

        euclidean_distance = numpy.linalg.norm(user_coords-airport_coords)
        if euclidean_distance < nearest_distance:
            nearest_aiport = airport
            nearest_distance = euclidean_distance

    return Response(nearest_aiport)

# ########################## OBTER UM DICIONÁRIO COM AS COORDENADAS GEOGRÁFICAS DOS AEROPORTOS ################################
def get_airports():
    # get all airports on only one page
    url = BASE_URL + 'airports?access_key=' + API_KEY + '&limit=100000'

    resp = requests.get(url=url)
    data = resp.json()
    airports = data['data']

    # dictionary of all airports and their respective geographic coordinates
    coords_airports = {airport['airport_name']: (airport['latitude'], airport['longitude']) for airport in airports}

    return coords_airports


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

def get_flights_by_arrival(arrivalCity):
    if not str(arrivalCity[0]).isupper():
        arrivalCity=arrivalCity.capitalize()
 
    cities = get_cities()
    
    # get iata code of our arrival city and use it to search on the url
    iata_code = cities[arrivalCity]

    # get all flights according the arrival iata code given
    url = BASE_URL + 'flights?access_key='+ API_KEY +'&arr_iata='+ iata_code+ '&flight_status=scheduled'

    resp = requests.get(url=url)
    data = resp.json()
    
    #data = [flight for flight in data['data'] if flight["flight_status"] == "scheduled" ]   # filter scheduled flights 

    return data

def get_flights_by_departure(departureCity):
    if not str(departureCity[0]).isupper():
        departureCity=departureCity.capitalize()

    
    cities = get_cities()
    
    iata_code = cities[departureCity]

    # get all flights according the departure iata code given
    url = BASE_URL + 'flights?access_key='+ API_KEY +'&dep_iata='+ iata_code+ '&flight_status=scheduled'

    resp = requests.get(url=url)
    data = resp.json()
    
    #data = [flight for flight in data['data'] if flight["flight_status"] == "scheduled" ]   # filter scheduled flights 
    #
    return data


def get_flights_by_arr_dep(departureCity,arrivalCity):
    
    if not str(arrivalCity[0]).isupper():
        arrivalCity=arrivalCity.capitalize()
 
    if not str(departureCity[0]).isupper():
        departureCity=departureCity.capitalize()
    
    cities = get_cities()
    
    iata_code_dep = cities[departureCity]
    iata_code_arr = cities[arrivalCity]
    print(iata_code_arr)
    print(iata_code_dep)

    # get all flights according the departure and arrival iata code given
    url = BASE_URL + 'flights?access_key='+ API_KEY +'&dep_iata='+ iata_code_dep + '&arr_iata='+ iata_code_arr+ '&flight_status=scheduled'
    resp = requests.get(url=url)
    data = resp.json()
    
    #data = [flight for flight in data['data'] if flight["flight_status"] == "scheduled" ]   # filter scheduled flights 

    return data


 # return a dictionary of all cities and their respective iata code
def get_cities():
     # the file 'cities.json' have all cities' data of API 
    with open('cities.json') as json_file:
        data = json.load(json_file)
        
    all_cities = data['data']
    return { city['city_name'] : city['iata_code'] for city in all_cities }



    
