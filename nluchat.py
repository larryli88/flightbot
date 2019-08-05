# Import necessary modules
from rasa_nlu.model import Interpreter
from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config

import time
import re

from amadeusApi import checkinLinks
from amadeusApi import flightOffers

# define states
INIT = 0
CHOOSE_ORG = 1
CHOOSE_DEST = 2
CHECKIN_LINK = 3
CHECKIN_LINK_CHOOSE = 4
FLIGHT_OFFER = 5
FLIGHT_OFFER_ORG = 6
FLIGHT_OFFER_DEST = 7
FLIGHT_OFFER_DEP_DATE = 8

# global params
params_global = {}
state_global = INIT

def greeting(params, msg, state):
    return INIT, params, "Hi, this is flight bot~"

def confusing(params, msg, state):
    return state, params, "Sorry, I don't get what you said...:("

def setCheckinAir(params, msg, state):
    matchObj = re.search(r'\b[A-Za-z0-9]{2}\b', msg)
    if not matchObj:
        return CHECKIN_LINK_CHOOSE, {}, "Sorry, this is an invalid IATA airline code, please try again"
    else:
        params['airline_code'] = matchObj.group()
    return getCheckin(params, msg, state)

def getCheckin(params, msg, state):
    if params.get('airline_code') == None:
        response = "Ok, which airline are you checknig in with? Tell me its IATA code"
        return CHECKIN_LINK_CHOOSE, {}, response
    
    response = checkinLinks(params['airline_code'])
    # the search is completed, reset state and params
    return CHECKIN_LINK_CHOOSE, {}, response

def setFlightOrg(params, msg, state):
    matchObj = re.search(r'\b[A-Z]{3}\b', msg)
    if not matchObj:
        return FLIGHT_OFFER_ORG, params, "Sorry, this is an invalid IATA airport code, please try again"
    else:
        params['fromloc.iata'] = matchObj.group()
    return getFlight(params, msg, state)

def setFlightDest(params, msg, state):
    matchObj = re.search(r'\b[A-Z]{3}\b', msg)
    if not matchObj:
        return FLIGHT_OFFER_DEST, params, "Sorry, this is an invalid IATA airport code, please try again"
    else:
        params['toloc.iata'] = matchObj.group()
    return getFlight(params, msg, state)

def setFlightDep(params, msg, state):
    params['depart_date'] = params['time'][:10]
    return getFlight(params, msg, state)

def getFlight(params, msg, state):
    # set the class type
    if "premium economy" in msg:
        params['class_type'] = "PREMIUM_ECONOMY"
    elif "business" in msg:
        params['class_type'] = "BUSINESS"
    elif "first class" in msg:
        params['class_type'] = "FIRST"
    else:
        params['class_type'] = "ECONOMY"
    # get org iata
    if params.get('fromloc.iata') == None:
        response = "Ok, where are you flying from?"
        return FLIGHT_OFFER_ORG, params, response
    # get dest iata
    if params.get('toloc.iata') == None:
        response = "Where are you flying to?"
        return FLIGHT_OFFER_DEST, params, response
    # non stop?
    if params.get('flight_stop') == None or params['flight_stop'] != "nonstop":
        params['flight_stop'] = False
    else:
        params['flight_stop'] = True
    # time?
    if params.get('depart_date') == None and params.get('time') == None:
        response = "Ok, when are you flying?"
        return FLIGHT_OFFER_DEP_DATE, params, response
    else:
        params['depart_date'] = params['time'][:10]
    print(params)
    return FLIGHT_OFFER, {}, flightOffers(params['fromloc.iata'], params['toloc.iata'], params['depart_date'], params['flight_stop'], params['class_type'])
    # default is no return flight

    

def backToInit(params, msg, state):
    return INIT, {}, "Thanks for using Flight Bot~"

# Define the policy rules
policy = {
    (INIT, "greet"): greeting,
    (INIT, "default"): confusing,
    (INIT, "checkin_link"): getCheckin,
    (INIT, "flight"): getFlight,
    (CHECKIN_LINK, "default"): getCheckin,
    (CHECKIN_LINK_CHOOSE, "decline"): backToInit,
    (CHECKIN_LINK_CHOOSE, "default"): setCheckinAir,
    (FLIGHT_OFFER, "default"): getFlight,
    (FLIGHT_OFFER_ORG, "default"): setFlightOrg,
    (FLIGHT_OFFER_DEST, "default"): setFlightDest,
    (FLIGHT_OFFER_DEP_DATE, "default"): setFlightDep,
    (FLIGHT_OFFER, "decline"): backToInit
}


def send_message(message, state, params):
    print("USER : {}".format(message))
    # Interpret the message
    parse_data = interpreter.parse(message)
    #print(parse_data)
    # Extract the intent
    intent = parse_data["intent"]["name"]

    # Extract the entities
    entities = parse_data["entities"]
    # Fill the dictionary with entities
    for ent in entities:
        params[ent["entity"]] = str(ent["value"])
    if policy.get((state, intent)) == None:
        intent = 'default'
    new_state, params, response = policy[(state, intent)](params, message, state)
    
    print("BOT : {}".format(response))
    return new_state, params, response

# load the trained model
interpreter = Interpreter.load('./model/default/model_20190805-111626')

"""
# Debug
# Define send_messages()
def send_messages(messages):
    state = INIT
    params = {}
    for msg in messages:
        state, params, response = send_message(msg, state, params)
        print(response)

# Send the messages
send_messages([
    "what can you do for me?",
    "i want to check in",
    "British Airline"
    #"i want to check in with united"
])
# Debug
"""
