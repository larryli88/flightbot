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
    try:
        response = amadeus.shopping.flight_offers.get(
                        origin=org,
                        destination=dest,
                        departureDate=departDate,
                        nonStop=flightStop,
                        travelClass=classTpye,
                        max=2
                    )
        offers = response.data
        response = ""
        for idx, ticket in enumerate(offers):
            response += ("ticket:" + str(idx + 1))
            for i, segment in enumerate(ticket['offerItems'][0]['services'][0]['segments']):
                response = response + "segment:" + str(i + 1)
                response += ("departure: " + segment['flightSegment']['departure']['iataCode'] + " at " + segment['flightSegment']['departure']['at'])
                response += ("arrival: " + segment['flightSegment']['arrival']['iataCode'] + " at " + segment['flightSegment']['arrival']['at'])
                response += (segment['flightSegment']['carrierCode'] + segment['flightSegment']['number'])
                response += ("Aircraft: " + segment['flightSegment']['aircraft']['code'])
            # price
            response += ("price: " + ticket['offerItems'][0]['price']['total'])
            response += ("\n")
        return response
    except:
        return "Sorry, no available flight found..."
