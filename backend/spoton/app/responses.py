import json
import random
import datetime
from urllib import response
import uuid
from django import views
from app import views
from httplib2 import Response
from app import NLP
from app import classify

seat_count = 50
feedback= False
with open("app/dataset.json") as file:
    data = json.load(file)

# categorize user input
def identify_intent(message):
    tag = classify.classify(message)
    
    return tag

def showflights(tag,keys):
    #find keys
    print(keys)
    #ver o caso
    rcv= views.get_flights()
    if "to" in keys:
        rcv=views.get_flights_by_departure(keys[keys.index("to")+1]
)    
    flights= rcv["data"]
    if len(flights)>0:
        response= get_response(tag)
        for f in flights:
            
            response = response+"\n"+f["flight"]["iata"]+"\n departure" +" "+  f["departure"]["scheduled"]+" "+ f["departure"]["airport"] +"\n arrival" + f["arrival"]["airport"] +" "+ f["arrival"]["scheduled"]+"\n\n"       
    else:
        response = "Sorry there are no offers available now."
    return response



def location():
    response="are you in brazil aakakkaka"
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


#this fucntion show create a request that connects user to an agent
def request_human():
    return "blhis"
    
def funcionalities(tag):
    response =get_response(tag)
    return response 
def show_menu():
    response = funcionalities()

    return response






#def record_feedback(message, type):
#    feedback_doc = {"feedback_string": message, "type": type}
#    feedback_collection.insert_one(feedback_doc)


# sends random response after identifying the tag
def get_response(tag):
    for intent in data['intents']:
        if intent['tag'] == tag:
            responses = intent['responses']
    response = random.choice(responses)
    return response

#asd
def generate_response(message):
    global feedback
    tag = identify_intent(message)  # get the adequate tag from the user input
    response = ""
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
           
            try:
                rating= int(message)
                if rating<5:
                    response= responses[1]
                    
                else:
                    response= responses[0]
                
                feedback=True
            except:
                response=random.choice(responses)
                feedback=True

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
            response =get_response(tag)
            response += request_human()

        elif tag == "menu":
            response = show_menu()
        elif tag== "showagain":
            response =get_response(tag)
        elif tag=="funcionalities":
            response = funcionalities(tag)
        elif tag == "details":
            
            response = get_response(tag)

        elif tag == "reservations":
            
            response = get_response(tag)
                       
        # for other intents with pre-defined responses that can be pulled from dataset
        else:
            print("foi aqui")
            response = get_response(tag)
    else:
        response = "Sorry! I didn't get it, please try to be more precise."
    return response