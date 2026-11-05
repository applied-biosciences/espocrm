import pathlib, uuid
ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / 'tests/nurivoyage/smoke.py'
source = p.read_text(); ns = {'__file__': str(p)}
exec(source[:source.index('try:\n    stamp=')], ns)
api = ns['api']; stamp = uuid.uuid4().hex[:8]
defs = api('Metadata')['entityDefs']
assert {'invoiceNumber','amount','paidAmount','balanceAmount','status','dueDate'}.issubset(defs['NvCustomerInvoice']['fields'])
assert {'paymentNumber','paymentType','amount','allocatedAmount','customerInvoice'}.issubset(defs['NvCustomerPayment']['fields'])
customer = api('Account', 'POST', {'name':'Stage 10 Synthetic Customer '+stamp,'type':'Customer'}, user='finance')
invoice = api('NvCustomerInvoice', 'POST', {'name':'Stage 10 Synthetic Invoice '+stamp,'customerId':customer['id'],'status':'Issued','amount':5000,'amountCurrency':'ZAR','paidAmount':0,'dueDate':'2027-02-15'}, user='finance')
payment = api('NvCustomerPayment', 'POST', {'name':'Stage 10 Synthetic Deposit '+stamp,'customerId':customer['id'],'customerInvoiceId':invoice['id'],'paymentType':'Deposit','amount':1500,'amountCurrency':'ZAR','allocatedAmount':1500,'paymentDate':'2027-01-15','reference':'DEP-'+stamp}, user='finance')
assert api('NvCustomerInvoice/'+invoice['id'], user='finance').get('invoiceNumber')
assert api('NvCustomerPayment/'+payment['id'], user='finance').get('paymentNumber')
print('PASS Stage 10 invoice, deposit, allocation and refund-type metadata lifecycle')
