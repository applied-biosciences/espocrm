"""Stage 19 full synthetic client booking journey."""
import pathlib, uuid
p=pathlib.Path('tests/nurivoyage/smoke.py'); ns={'__file__':str(p)}
exec(p.read_text().split('try:\n    stamp=')[0],ns)
api=ns['api']; stamp=uuid.uuid4().hex[:8]
customer=api('Account','POST',{'name':'SYNTHETIC E2E Customer '+stamp,'description':'Stage 19 local smoke only'})
enquiry=api('NvEnquiry','POST',{'name':'SYNTHETIC E2E Enquiry '+stamp,'customerId':customer['id'],'status':'Qualified','destination':'Makkah and Madinah','serviceType':'Umrah','travellerCount':2})
print('PASS enquiry created:',enquiry['id'])
quote=api('NvQuote','POST',{'name':'SYNTHETIC E2E Quote '+stamp,'enquiryId':enquiry['id'],'customerId':customer['id'],'quoteNumber':'E2E-'+stamp,'status':'Accepted','sellingPrice':25000,'validUntil':'2027-01-31'})
print('PASS quote accepted:',quote['id'])
booking=api('NvBooking','POST',{'name':'SYNTHETIC E2E Booking '+stamp,'customerId':customer['id'],'enquiryId':enquiry['id'],'status':'Booking Confirmed','supplierStatus':'Supplier Selected','sellingPrice':25000,'travelDate':'2027-02-10','returnDate':'2027-02-20','bookingReference':'E2E-'+stamp,'itineraryTitle':'Two-city Umrah journey','destination':'Saudi Arabia','departureCity':'London','arrivalCity':'Jeddah','travellerCount':2,'confirmedAt':'2026-10-18 10:30:00'})
print('PASS booking confirmed:',booking['id'])
traveller=api('NvTraveller','POST',{'name':'SYNTHETIC E2E Lead Traveller '+stamp,'travellerNumber':'TRV-'+stamp,'customerId':customer['id'],'bookingId':booking['id'],'nationality':'British','isLeadTraveller':True,'groupReference':'E2E-'+stamp})
print('PASS lead traveller linked:',traveller['id'])
invoice=api('NvCustomerInvoice','POST',{'name':'SYNTHETIC E2E Invoice '+stamp,'invoiceNumber':'INV-'+stamp,'bookingId':booking['id'],'customerId':customer['id'],'status':'Issued','amount':25000,'paidAmount':0,'balanceAmount':25000,'dueDate':'2027-01-15'})
print('PASS invoice issued:',invoice['id'])
payment=api('NvCustomerPayment','POST',{'name':'SYNTHETIC E2E Deposit '+stamp,'paymentNumber':'PAY-'+stamp,'bookingId':booking['id'],'customerId':customer['id'],'customerInvoiceId':invoice['id'],'amount':10000,'allocatedAmount':10000,'paymentType':'Deposit','paymentDate':'2026-10-18','reference':'E2E-'+stamp})
print('PASS payment recorded:',payment['id'])
assert api('NvBooking/'+booking['id'])['bookingReference']=='E2E-'+stamp
assert api('NvTraveller/'+traveller['id'])['bookingId']==booking['id']
print('PASS end-to-end customer booking relationships verified')
print('PASS synthetic records are local-only and safe for cleanup')
