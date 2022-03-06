from enum import unique
import json
from urllib import response
# 6import request
import random
from django import views
from app import views
from app import NLP
from app import classify
from app.models import Help, Feedback


seat_count = 50
feedback= False

with open("app/dataset.json") as file:
    data = json.load(file)

# categorize user input
def identify_intent(message):
    tag = classify.classify(message)
    
    return tag

def showflights(tag,keys):

    global pricingdic, flightwithunique, sorted_by_second

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

    date = None
    if "date" in keys:
        date = keys[keys.index("date") + 1]

    airline = None
    if "airline" in keys:
        airline = keys[keys.index("airline") + 1]

    print(rcv)
    flights= rcv["data"]
    all_flights=[]
    sorted_by_second = []
    flightwithunique = []
    pricingdic={}
    pricetuple=[]
    if len(flights)>0:
        text= get_response(tag)
        for f in flights:
            
            if f["flight"]["iata"]:
                uniqueid= f["flight"]["iata"]+f["departure"]["scheduled"]
                print(uniqueid)
                pricingdic[uniqueid]= random.randint(50,250)
                pricetuple.append((uniqueid,pricingdic[uniqueid]))
                flightwithunique.append((uniqueid,f))
                    

            sorted_by_second = sorted(pricetuple, key=lambda tup: tup[1])

        for nf,p in sorted_by_second:
            for item in flightwithunique:
                if nf == item[0]:
                    getf=item[1]

                    if date is not None and date not in getf['departure']['scheduled']:
                        print("date")
                        continue

                    if airline is not None and airline not in getf['airline']['name']:
                        print(getf['airline']['name'])
                        print("airline::: "+ airline)
                        continue

                    all_flights.append( json.dumps({
                                                    "airline" :     getf["airline"]["name"],
                                                    "flight_iata" : getf["flight"]["iata"],
                                                    "dep_airport" : getf["departure"]["airport"],
                                                    "dep_time" :    getf["departure"]["scheduled"],
                                                    "arr_airport" : getf["arrival"]["airport"],
                                                    "arr_time" :    getf["arrival"]["scheduled"],
                                                    "price" :       str(pricingdic[nf])
                                                })
                    )

        response = {"tag":tag, "body": {"flights":all_flights, "default_msg":  text} }

      
    else:
        response = {"tag":tag,"body": {"flights":[], "default_msg":  "There are no current offers for the selected destinations :("} }

    return response



def location(tag):
    response="are you in brazil aakakkaka"
    return response


def book():
    return "Flight was booked! Please pay at counter!"

    """global seat_count
    seat_count = seat_count - 1
    booking_id = str(uuid.uuid4())
    now = datetime.datetime.now()
    booking_time = now.strftime("%Y-%m-%d %H:%M:%S")
    booking_doc = {"booking_id": booking_id, "booking_time": booking_time}
    bookings_collection.insert_one(booking_doc)
    return booking_id"""


#this fucntion show create a request that connects user to an agent
def default_message_builder(tag, resp):
    build_json={"tag":tag, "body":resp}
    return build_json
    
def funcionalities(tag):
    response =get_response(tag)
    return default_message_builder(tag,response)
def show_menu(tag):
    
    return funcionalities(tag)


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
            response= book()


        elif tag == "greeting":
            response = get_response(tag)

        elif tag == "goodbye":#???
            
            if feedback:
                response = "Before leaving can you please rate the service by sending a number between 0-5"
            else :
                response= get_response(tag)

        elif tag == "feedback":

            for intent in data['intents']:
                if intent['tag'] == tag:
                    responses = intent['responses']
           

            rating = int(message)

            if rating >= 3 and rating <= 5:
                print("positive")
                feedback = True
                response = responses[0]

            elif rating > 0 and rating < 3:
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
                return json.dumps(response)

        elif tag == "ratings":
            response = funcionalities(tag)
        elif tag == "location":
            response = location(tag)

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

    response = {'tag': tag, 'body' : response }
    return json.dumps(response)