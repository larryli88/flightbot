import amadeus
import re
from amadeus import Client

amadeus = Client(
    client_id='3U1urnDmq0gmV8zYHPnnoF3f8xd2j0Rt',
    client_secret='C7nONTvrqiPAzTtC'
)

def checkinLinks(code):
    response = amadeus.reference_data.urls.checkin_links.get(airlineCode=code)
    return response.data[0]['href']
