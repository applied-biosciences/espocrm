import pathlib, uuid
ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / 'tests/nurivoyage/smoke.py'
source = p.read_text(); ns = {'__file__': str(p)}
exec(source[:source.index('try:\n    stamp=')], ns)
api = ns['api']; stamp = uuid.uuid4().hex[:8]
fields = api('Metadata')['entityDefs']['NvPurchaseOrder']['fields']
assert {'purchaseOrderNumber','status','booking','supplier','amount','dueDate','requestedAt','confirmedAt','supplierReference'}.issubset(fields)
supplier = api('NvSupplier', 'POST', {'name':'Stage 9 Synthetic Supplier '+stamp,'category':'Hotel'}, user='finance')
booking = api('NvBooking', 'POST', {'name':'Stage 9 Synthetic Booking '+stamp,'status':'Quote Prepared'}, user='finance')
po = api('NvPurchaseOrder', 'POST', {'name':'Stage 9 Synthetic PO '+stamp,'bookingId':booking['id'],'supplierId':supplier['id'],'status':'Supplier Selected','amount':1800,'amountCurrency':'ZAR','dueDate':'2027-02-01','requestedAt':'2027-01-10 09:00:00','supplierReference':'SUP-'+stamp}, user='finance')
detail = api('NvPurchaseOrder/'+po['id'], user='finance')
assert detail.get('purchaseOrderNumber') and detail.get('supplierReference') == 'SUP-'+stamp
assert detail.get('status') == 'Supplier Selected'
print('PASS Stage 9 procurement and purchase-order lifecycle')
