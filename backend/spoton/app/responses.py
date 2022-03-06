from enum import unique
import json
from urllib import response
import request
import random
from django import views
from app import views
from app import NLP
from app import classify
from app.models import Help, Feedback

pricingdic={}
pricetuple=[]
seat_count = 50
feedback= False

with open("app/dataset.json") as file:
    data = json.load(file)

# categorize user input
def identify_intent(message):
    tag = classify.classify(message)
    
    return tag

def showflights(tag,keys):

    global pricingdic

    #find keys
    print(keys)
    #ver o caso
    if  "to" in keys and "from" in keys:
        rcv=views.get_flights_by_arr_dep(keys[keys.index("from")+1],keys[keys.index("to")+1])
    elif "from" in keys:
        rcv=views.get_flights_by_departure(keys[keys.index("from")+1])
    elif "to" in keys:
        rcv=views.get_flights_by_arrival(keys[keys.index("to")+1])
    else:  
        rcv= views.get_flights()

    # optional search filters

    ascendent_order = None
    if "price" in keys or "cost" in keys:
        price_order = keys[keys.index("to") + 1]
        ascendent_order = True if price_order == "ASC" else False if price_order == "DESC" else None

    date = None
    if "date" in keys:
        date = keys[keys.index("to") + 1]

    airline = None
    if "airline" in keys:
        airline = keys[keys.index("to") + 1]

    flights= rcv["data"]
    flightwithunique=[]

    if len(flights)>0:
        text= get_response(tag)
        for f in flights:
            
            if f["flight"]["iata"]:
                uniqueid= f["flight"]["iata"]+f["departure"]["scheduled"]
                print(uniqueid)
                if uniqueid not in pricingdic:

                    if date is not None and date not in f['departure']['scheduled']:
                        continue

                    if airline is not None and airline not in f['airline']['name']:
                        continue

                    price = random.randint(50,250)
                    pricingdic[uniqueid]= price
                    pricetuple.append((uniqueid,pricingdic[uniqueid]))
                    flightwithunique.append((uniqueid,f))

                    sorted_by_second = sorted(pricetuple, key=lambda tup: tup[1])
                    if ascendent_order == False:
                        sorted_by_second = sorted_by_second.reverse()



        for nf,p in sorted_by_second:
            for item in flightwithunique:
                if nf == item[0]:
                    getf=item[1]
                    build_response_json= {"tag":tag, "body":{"default_msg":text,"airline":getf["airline"]["name"],"flight_iata":getf["flight"]["iata"],"dep_airport":getf["departure"]["airport"],"dep_time":getf["departure"]["scheduled"], "arr_airport":getf["arrival"]["airport"],"arr_time":getf["arrival"]["scheduled"],"price":str(pricingdic[nf])}}
                    response = json.dumps(build_response_json)       

    else:
        response = {"tag":tag,"body":"Sorry there are no offers available now."}

    return response



def location():
    text="are you in brazil aakakkaka"
    return response


def book():
    return ""

    """global seat_count
    seat_count = seat_count - 1
    booking_id = str(uuid.uuid4())
    now = datetime.datetime.now()
    booking_time = now.strftime("%Y-%m-%d %H:%M:%S")
    booking_doc = {"booking_id": booking_id, "booking_time": booking_time}
    bookings_collection.insert_one(booking_doc)
    return booking_id"""


def funcionalities(tag):
    response =get_response(tag)
    return response 
def show_menu(tag):
    response = funcionalities(tag)

    return response


# sends random response after identifying the tag
def get_response(tag):
    for intent in data['intents']:
        if intent['tag'] == tag:
            responses = intent['responses']
    response = random.choice(responses)
    return response

#asd
def generate_response(message, username):


    # identify the appropriate tag and sent the correct response (type + message)

    global feedback
    tag = identify_intent(message)  # get the adequate tag from the user input
    
    if tag != "":
        if tag == "book":
            gen=0
            if gen > 0:
                response = "Your flight has been booked successfully. Please show this Booking ID at the counter: "  
            else:
                response = "Sorry we are sold out now!"


        elif tag == "greeting":
            response = get_response(tag)

        elif tag == "goodbye":#???
            
            if feedback:
                response = "Before leaving can you please rate the service by sending a number between 0-10"
            else :
                response= get_response(tag)

        elif tag == "feedback":

            for intent in data['intents']:
                if intent['tag'] == tag:
                    responses = intent['responses']
           

            rating = int(message)

            if rating >= 6 and rating <= 10:
                print("positive")
                feedback = True
                response = responses[0]

            elif rating > 0 and rating < 6:
                feedback = True
                response = responses[1]

            else:
                response = "Invalid type of feedback. Please review me from 1-10."
                feedback = False

            # save feedback to analyse the overall performance of the bot
            if feedback:
                print("saved")
                feedback_obj = Feedback(username=username,rating=rating);
                feedback_obj.save()

        elif tag == "showflights":

            #devolve um array pos 0 msg de texto pos 1 msg de 
            msg= message.split(' ')
            keys = NLP.findkeys(msg)
            if keys==404:
                response= "Please input a city after to/from "
            else:
                response = showflights(tag,keys)
            

        elif tag == "location":
            response = location()

        elif tag == "human_request":

            # save help so that humans can read who is asking for help
            help = Help(username=username);
            help.save()
            response = get_response(tag)

        elif tag == "menu":
            response = show_menu(tag)

        elif tag== "showagain":
            response = get_response(tag)

        elif tag=="funcionalities":
            response = funcionalities(tag)

        elif tag == "details":
            
            response = get_response(tag)

        elif tag == "reservations":
            
            response = get_response(tag)
                       
        # for other intents with pre-defined responses that can be pulled from dataset
        else:
            response = get_response(tag)
    else:
        response = "Sorry! I didn't get it, please try to be more precise."

    response = {'type': tag, 'message' : response }
    return response