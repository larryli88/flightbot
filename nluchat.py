# Import necessary modules
from rasa_nlu.model import Interpreter
from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config

import time
import re

from amadeusApi import checkinLinks

# define states
INIT = 0
CHOOSE_ORG = 1
CHOOSE_DEST = 2
CHECKIN_LINK = 3
CHECKIN_LINK_CHOOSE = 4

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
        return CHECKIN_LINK_CHOOSE, {}, "Sorry, this is an invalid IATA airline code"
    else:
        params['airline_code'] = matchObj.group()
    return getCheckin(params, msg, state)

def getCheckin(params, msg, state):
    if params.get('airline_code') == None:
        response = "Ok, which airline are you checknig in with? Tell me its IATA code"
        return CHECKIN_LINK_CHOOSE, {}, response
    
    response = "the check in link is {}\n Any other airline's check in website do you want?".format(checkinLinks(params['airline_code']))
    # the search is completed, reset state and params
    return CHECKIN_LINK_CHOOSE, {}, response

def backToInit(params, msg, state):
    return INIT, {}, "Thanks for using Flight Bot~"

# Define the policy rules
policy = {
    (INIT, "greet"): greeting,
    (INIT, "default"): confusing,
    (INIT, "checkin_link"): getCheckin,
    (CHECKIN_LINK, "default"): getCheckin,
    (CHECKIN_LINK_CHOOSE, "decline"): backToInit,
    (CHECKIN_LINK_CHOOSE, "default"): setCheckinAir
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
interpreter = Interpreter.load('./model/default/model_20190804-003240')

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
