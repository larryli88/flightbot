import amadeus
import re
import json
from amadeus import Client

amadeus = Client(
    client_id='3U1urnDmq0gmV8zYHPnnoF3f8xd2j0Rt',
    client_secret='C7nONTvrqiPAzTtC'
)

def checkinLinks(code):
    response = amadeus.reference_data.urls.checkin_links.get(airlineCode=code)
    if not response.data:
        return "Sorry, this is an invalid IATA airline code, please try again"
    else:
        return "the check in link is {}\n Any other airline's check in website do you want?".format(response.data[0]['href'])

def flightOffers(org, dest, departDate, flightStop, classTpye):
    response = amadeus.shopping.flight_offers.get(
                    origin=org,
                    destination=dest,
                    departureDate=departDate,
                    nonStop=flightStop,
                    travelClass=classTpye
                )
    if not response.data:
        return "Sorry, this is an invalid IATA airline code, please try again"
    else:
        return json.dumps(response.data)
