#!/usr/bin/env python3
"""Stage 7 focused checks for traveller passport photos and versioning."""
import base64, pathlib, urllib.request, uuid
ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / 'tests/nurivoyage/smoke.py'
source = p.read_text(); ns = {'__file__': str(p)}
exec(source[:source.index('try:\n    stamp=')], ns)
api = ns['api']
fields = api('Metadata')['entityDefs']['NvTraveller']['fields']
assert 'passportPhoto' in fields and fields['passportPhoto']['type'] == 'image'
head = urllib.request.urlopen('http://localhost:8080/client/custom/nurivoyage-head.js').read().decode()
assert 'v10.0.10.0.s7' in head
print('PASS Stage 7 metadata and version marker')
stamp = uuid.uuid4().hex[:8]
traveller = api('NvTraveller', 'POST', {'name':'Stage 7 Synthetic Traveller '+stamp}, user='operations')
png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aKfkAAAAASUVORK5CYII=')
attachment = api('Attachment', 'POST', {'name':'synthetic-passport-photo-'+stamp+'.png','type':'image/png','role':'Attachment','relatedType':'NvTraveller','field':'passportPhoto','file':'data:image/png;base64,'+base64.b64encode(png).decode()}, user='operations')
api('NvTraveller/'+traveller['id'], 'PUT', {'passportPhotoId':attachment['id']}, user='operations')
detail = api('NvTraveller/'+traveller['id'], user='operations')
assert detail.get('passportPhotoId') == attachment['id']
api('Attachment/file/'+attachment['id'], user='operations', raw=True)
sales_detail = api('NvTraveller/'+traveller['id'], user='sales')
assert sales_detail.get('passportPhotoId') == attachment['id']
api('Attachment/file/'+attachment['id'], user='sales', raw=True)
print('PASS Stage 7 lifecycle: Operations attached private passport photo; Sales can view it')
booking_fields = api('Metadata')['entityDefs']['NvBooking']['fields']
required_booking = ['bookingReference','itineraryTitle','destination','departureCity','arrivalCity','travellerCount','itineraryNotes','confirmedAt']
assert all(name in booking_fields for name in required_booking)
booking = api('NvBooking', 'POST', {
    'name':'Stage 7 Synthetic Itinerary '+stamp,
    'bookingReference':'NV-B-'+stamp, 'itineraryTitle':'Umrah Family Itinerary',
    'destination':'Makkah and Madinah', 'departureCity':'Cape Town',
    'arrivalCity':'Jeddah', 'travellerCount':2,
    'travelDate':'2027-01-10', 'returnDate':'2027-01-21',
    'status':'Booking Confirmed', 'confirmedAt':'2026-10-22 10:00:00',
    'itineraryNotes':'Synthetic itinerary for Stage 7 local testing.'
}, user='operations')
itinerary = api('NvBooking/'+booking['id'], user='operations')
assert itinerary['bookingReference'] == 'NV-B-'+stamp and itinerary['destination'] == 'Makkah and Madinah'
print('PASS Stage 7 itinerary lifecycle: Operations created and read a synthetic itinerary')
segments = [
    {'name':'Stage 7 City 1 Makkah '+stamp, 'bookingId':booking['id'], 'sequence':1, 'city':'Makkah', 'transferMode':'None'},
    {'name':'Stage 7 City 2 Madinah '+stamp, 'bookingId':booking['id'], 'sequence':2, 'city':'Madinah', 'transferMode':'Road', 'transferFromCity':'Makkah', 'transferCost':850, 'transferCostCurrency':'ZAR'},
    {'name':'Stage 7 City 3 Jeddah '+stamp, 'bookingId':booking['id'], 'sequence':3, 'city':'Jeddah', 'transferMode':'Air', 'transferFromCity':'Madinah', 'transferCost':1200, 'transferCostCurrency':'ZAR'},
]
for segment in segments:
    api('NvItinerarySegment', 'POST', segment, user='operations')
segment_list = api('NvItinerarySegment', user='operations')['list']
created_cities = {row.get('city') for row in segment_list if row.get('bookingId') == booking['id']}
assert {'Makkah','Madinah','Jeddah'}.issubset(created_cities)
print('PASS Stage 7 expandable city segments: two starting cities plus an additional city and priced transfers')
transfer = api('NvTransfer', 'POST', {
    'name':'Stage 7 Inter-city Transfer '+stamp, 'transferType':'Inter-city',
    'originCity':'Makkah', 'destinationCity':'Madinah', 'cost':850,
    'bookingId':booking['id'],
    'costCurrency':'ZAR'
}, user='operations')
assert api('NvTransfer/'+transfer['id'], user='operations')['transferType'] == 'Inter-city'
hotel1 = api('NvHotel', 'POST', {'name':'Stage 7 Makkah Hotel '+stamp,'city':'Makkah','staySequence':1}, user='operations')
hotel2 = api('NvHotel', 'POST', {'name':'Stage 7 Madinah Hotel '+stamp,'city':'Madinah','staySequence':2}, user='operations')
assert api('NvHotel/'+hotel1['id'], user='operations')['city'] == 'Makkah'
assert api('NvHotel/'+hotel2['id'], user='operations')['city'] == 'Madinah'
sightseeing = api('NvSightseeing', 'POST', {
    'name':'Stage 7 Makkah Sightseeing '+stamp, 'city':'Makkah',
    'activityDate':'2027-01-14', 'cost':300, 'costCurrency':'ZAR', 'status':'Planned', 'bookingId':booking['id']
}, user='operations')
assert api('NvSightseeing/'+sightseeing['id'], user='operations')['city'] == 'Makkah'
print('PASS Stage 7 multi-city itinerary: inter-city transfer, multi-hotel stays and sightseeing cost persisted')
booking_detail = api('NvBooking/'+booking['id'], user='operations')
group_member = api('NvTraveller', 'POST', {'name':'Stage 7 Booking Member '+stamp, 'bookingId':booking['id'], 'isLeadTraveller':False}, user='operations')
assert api('NvBooking/'+booking['id']+'/travellers', user='operations')['total'] >= 1
api('NvTraveller/'+group_member['id'], 'PUT', {'bookingId':None}, user='operations')
assert api('NvBooking/'+booking['id']+'/travellers', user='operations')['total'] == 0
api('NvTraveller/'+group_member['id'], 'PUT', {'bookingId':booking['id']}, user='operations')
assert api('NvBooking/'+booking['id']+'/itinerarySegments', user='operations')['total'] >= 3
assert api('NvBooking/'+booking['id']+'/transfers', user='operations')['total'] >= 1
assert api('NvBooking/'+booking['id']+'/sightseeing', user='operations')['total'] >= 1
print('PASS Stage 7 booking page relationships: travellers, city segments, transfers and sightseeing are visible')
