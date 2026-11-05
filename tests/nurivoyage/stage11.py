import pathlib, uuid
ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / 'tests/nurivoyage/smoke.py'
source = p.read_text(); ns = {'__file__': str(p)}
exec(source[:source.index('try:\n    stamp=')], ns)
api = ns['api']; stamp = uuid.uuid4().hex[:8]
fields = api('Metadata')['entityDefs']['NvCommission']['fields']
assert {'commissionNumber','basisAmount','amount','status','ruleSnapshot','frozen','approvedAt','paidAt','settlementReference'}.issubset(fields)
agentFields = api('Metadata')['entityDefs']['NvAgent']['fields']
assert {'user','login','lastLoginAt','loginAuditTrail','completedSales','openSales','commissionType','commissionPaid','commissionOwed'}.issubset(agentFields)
booking = api('NvBooking', 'POST', {'name':'Stage 11 Synthetic Booking '+stamp,'status':'Booking Confirmed'}, user='finance')
commission = api('NvCommission', 'POST', {'name':'Stage 11 Synthetic Commission '+stamp,'bookingId':booking['id'],'method':'Percent of Sale','basisAmount':10000,'amount':1000,'amountCurrency':'ZAR','status':'Draft','frozen':False,'ruleSnapshot':'10% synthetic rule'}, user='manager')
api('NvCommission/'+commission['id'], 'PUT', {'status':'Approved','frozen':True,'approvedAt':'2027-02-01 10:00:00'}, user='finance')
updated = api('NvCommission/'+commission['id'], 'PUT', {'status':'Paid','paidAt':'2027-02-10 10:00:00','settlementReference':'SET-'+stamp}, user='finance')
assert updated.get('commissionNumber') and updated.get('frozen') is True and updated.get('status') == 'Paid'
print('PASS Stage 11 commission approval, freeze and settlement lifecycle')
