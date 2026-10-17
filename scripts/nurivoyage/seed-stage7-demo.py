#!/usr/bin/env python3
"""Create one stable, synthetic family and a four-stop Stage 7 itinerary."""
import base64
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
env = dict(line.split('=', 1) for line in (ROOT / '.env').read_text().splitlines()
           if line and not line.startswith('#'))
base = 'http://localhost:8080/api/v1/'
auth = base64.b64encode((env['ESPO_ADMIN_USERNAME'] + ':' + env['ESPO_ADMIN_PASSWORD']).encode()).decode()

def api(path, method='GET', data=None):
    req = urllib.request.Request(base + path, method=method,
        data=json.dumps(data).encode() if data is not None else None,
        headers={'Authorization': 'Basic ' + auth, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

def ensure(scope, name, values):
    rows = api(scope + '?maxSize=200')['list']
    found = next((row for row in rows if row['name'] == name), None)
    if found:
        return api(scope + '/' + found['id'], 'PUT', values)
    return api(scope, 'POST', {'name': name, **values})

customer = ensure('Account', 'DEMO Al Noor Family (synthetic)',
                  {'type': 'Customer', 'description': 'Synthetic Stage 7 group UAT record.'})
booking = ensure('NvBooking', 'DEMO Al Noor Four-City Itinerary (synthetic)', {
    'customerId': customer['id'], 'bookingReference': 'DEMO-S7-4CITY',
    'itineraryTitle': 'Four-city family itinerary', 'destination': 'Saudi Arabia',
    'departureCity': 'Cape Town', 'arrivalCity': 'Jeddah', 'travellerCount': 4,
    'travelDate': '2027-02-10', 'returnDate': '2027-02-24',
    'status': 'Quote Prepared',
    'itineraryNotes': 'Synthetic demonstration. Add or remove group members before confirmation.'
})
travellers = []
for index, name in enumerate(['Amina Noor', 'Yusuf Noor', 'Mariam Noor', 'Idris Noor']):
    travellers.append(ensure('NvTraveller', 'DEMO ' + name + ' (synthetic)', {
        'customerId': customer['id'], 'bookingId': booking['id'],
        'groupReference': 'DEMO-S7-FAMILY', 'isLeadTraveller': index == 0
    }))
api('NvBooking/' + booking['id'], 'PUT', {'leadTravellerId': travellers[0]['id']})

stops = [
    (1, 'Jeddah', '2027-02-10', '2027-02-11', 'Cape Town', 'Plane', 4200),
    (2, 'Makkah', '2027-02-11', '2027-02-16', 'Jeddah', 'Car', 350),
    (3, 'Madinah', '2027-02-16', '2027-02-21', 'Makkah', 'Bus', 850),
    (4, 'Riyadh', '2027-02-21', '2027-02-24', 'Madinah', 'Train', 1100),
]
segment_ids = {}
for seq, city, arrival, departure, origin, mode, cost in stops:
    segment = ensure('NvItinerarySegment', f'DEMO stop {seq}: {city} (synthetic)', {
        'bookingId': booking['id'], 'sequence': seq, 'city': city,
        'arrivalDate': arrival, 'departureDate': departure,
        'transferFromCity': origin, 'transferMode': mode,
        'transferCost': cost, 'transferCostCurrency': 'ZAR'
    })
    segment_ids[city] = segment['id']
for seq, city, hotel, check_in, check_out, cost in [
    (1, 'Jeddah', 'Arrival Hotel', '2027-02-10', '2027-02-11', 700),
    (2, 'Makkah', 'Hotel One', '2027-02-11', '2027-02-13', 1800),
    (3, 'Makkah', 'Hotel Two', '2027-02-13', '2027-02-16', 2400),
    (4, 'Madinah', 'Hotel Three', '2027-02-16', '2027-02-21', 3000),
    (5, 'Riyadh', 'Departure Hotel', '2027-02-21', '2027-02-24', 2100),
]:
    ensure('NvHotel', f'DEMO {city} {hotel} (synthetic)', {
        'bookingId': booking['id'], 'itinerarySegmentId': segment_ids[city],
        'city': city, 'staySequence': seq, 'checkIn': check_in, 'checkOut': check_out,
        'cost': cost, 'costCurrency': 'ZAR'
    })
for city, activity, date, cost in [('Makkah', 'Historic Sites', '2027-02-13', 300),
                                    ('Madinah', 'City Tour', '2027-02-18', 450)]:
    ensure('NvSightseeing', f'DEMO {city} {activity} (synthetic)', {
        'bookingId': booking['id'], 'city': city, 'activityDate': date,
        'cost': cost, 'costCurrency': 'ZAR', 'status': 'Planned'
    })
for origin, destination, cost in [('Jeddah', 'Makkah', 350),
                                   ('Makkah', 'Madinah', 850),
                                   ('Madinah', 'Riyadh', 1100)]:
    ensure('NvTransfer', f'DEMO {origin} to {destination} (synthetic)', {
        'bookingId': booking['id'], 'transferType': 'Inter-city',
        'originCity': origin, 'destinationCity': destination,
        'cost': cost, 'costCurrency': 'ZAR'
    })

print('Customer number:', customer['customerNumber'])
print('Traveller numbers:', ', '.join(str(item['travellerNumber']) for item in travellers))
print('Customer: http://localhost:8080/#Account/view/' + customer['id'])
print('Itinerary: http://localhost:8080/#NvBooking/view/' + booking['id'])
print('Travellers: 4; city stops: 4; hotels: 5; transfers: 3; sightseeing: 2')
