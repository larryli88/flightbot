# Import necessary modules
from rasa_nlu.model import Interpreter
from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config

import time

# global params
params_global = {}

def greeting(params, msg):
    return INIT, params, "Hi, this is flight bot~"

def setCheckinAir(params, msg):
    params['airline_name'] = msg
    return getCheckin(params, msg)

def getCheckin(params, msg):
    if params.get('airline_name') == None:
        return CHECKIN_AIRLINE, params, "ok, which airline are you checking in with?"
    # the search is completed, reset state and params
    return INIT, {}, "the check in link for {} is: ...".format(params['airline_name'])

# Define the INIT state
INIT = 0
# Define the CHOOSE_ORG state
CHOOSE_ORG = 1
# Define the CHOOSE_DEST state
CHOOSE_DEST = 2
CHECKIN_LINK = 3
CHECKIN_AIRLINE = 4
# Define the policy rules
policy = {
    (INIT, "greet"): greeting,
    (INIT, "checkin_link"): getCheckin,
    (CHECKIN_AIRLINE, "airline"): setCheckinAir
    #(CHOOSE_COFFEE, "specify_coffee"): (ORDERED, "perfect, the beans are on their way!"),
    #(CHOOSE_COFFEE, "none"): (CHOOSE_COFFEE, "I'm sorry - would you like Colombian or Kenyan?"),
}


def send_message(message, state, params):
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
    
    new_state, params, response = policy[(state, intent)](params, message)

    print(response)
    return new_state, params

# load the trained model
interpreter = Interpreter.load('./model/default/model_20190803-162447')


# Debug
# Define send_messages()
def send_messages(messages):
    state = INIT
    params = {}
    for msg in messages:
        state, params = send_message(msg, state, params)

# Send the messages
send_messages([
    "what can you do for me?",
    "i want to check in",
    "British Airline"
    #"i want to check in with united"
])
# Debug
