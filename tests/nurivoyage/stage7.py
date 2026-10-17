#!/usr/bin/env python3
"""Stage 7 focused checks for traveller passport photos and versioning."""
import base64, pathlib, urllib.request, uuid
ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / 'tests/nurivoyage/smoke.py'
source = p.read_text(); ns = {'__file__': str(p)}
exec(source[:source.index('try:\n    stamp=')], ns)
api = ns['api']
fields = api('Metadata')['entityDefs']['NvTraveller']['fields']
assert 'passportPhoto' in fields and fields['passportPhoto']['type'] == 'file'
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
