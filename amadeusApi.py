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
        return "The check in link is: {}\n Do you want any other airline's check in link?".format(response.data[0]['href'])

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
        price = offers[0]['offerItems'][0]['price']['total']
        depTime = offers[0]['offerItems'][0]['services'][0]['segments'][0]['flightSegment']['departure']['at'][11:16]
        response = "<b>Flight from {} to {} - ${}</b>\n\n".format(org, dest, price)
        for segment in offers[0]['offerItems'][0]['services'][0]['segments']:
            dep = segment['flightSegment']['departure']['iataCode']
            arr = segment['flightSegment']['arrival']['iataCode']
            depTime = segment['flightSegment']['departure']['at'][11:16]
            depDate = segment['flightSegment']['departure']['at'][5:10]
            arrTime = segment['flightSegment']['arrival']['at'][11:16]
            flightNum = segment['flightSegment']['carrierCode'] + segment['flightSegment']['number']
            aircraft = segment['flightSegment']['aircraft']['code']
            duration = segment['flightSegment']['duration'][3:]
            response += "Depart from {} - {} ({})\n".format(dep, depTime, depDate)
            response += "Arrive at {} - {}\n".format(arr, arrTime)
            response += "<b>{}</b>\n".format(flightNum)
            response += "Duration: {}\n".format(duration)
            response += "Aircraft: {}\n\n".format(aircraft)
        return response
        '''
        for idx, ticket in enumerate(offers):
            response += ("ticket:" + str(idx + 1))
            for i, segment in enumerate(ticket['offerItems'][0]['services'][0]['segments']):
                response = response + "\nsegment:" + str(i + 1)
                response += ("\ndeparture: " + segment['flightSegment']['departure']['iataCode'] + " at " + segment['flightSegment']['departure']['at'])
                response += ("\narrival: " + segment['flightSegment']['arrival']['iataCode'] + " at " + segment['flightSegment']['arrival']['at'])
                response += ("\n" + segment['flightSegment']['carrierCode'] + segment['flightSegment']['number'])
                response += ("\nAircraft: " + segment['flightSegment']['aircraft']['code'])
            # price
            response += ("\nprice: " + ticket['offerItems'][0]['price']['total'])
            response += ("\n")
        return response
    '''
    except:
        return "Sorry, no available flight found..."
