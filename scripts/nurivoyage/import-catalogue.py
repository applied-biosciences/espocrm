#!/usr/bin/env python3
"""Import supplier/product catalogue rows from CSV through the local Espo API."""
import csv, json, os, sys, urllib.request, urllib.parse

BASE = os.environ.get('NURIVOYAGE_URL', 'http://localhost:8080').rstrip('/')
USER = os.environ.get('NURIVOYAGE_USER', 'admin@nuri.local')
PASSWORD = os.environ.get('NURIVOYAGE_PASSWORD', '')

def request(path, method='GET', payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(BASE + '/api/v1/' + path, data=data, method=method, headers={'Content-Type':'application/json'})
    auth = urllib.request.HTTPPasswordMgrWithDefaultRealm(); auth.add_password(None, BASE, USER, PASSWORD)
    opener = urllib.request.build_opener(urllib.request.HTTPBasicAuthHandler(auth))
    with opener.open(req) as response: return json.load(response)

def main():
    if len(sys.argv) != 2: raise SystemExit('Usage: scripts/local import-catalogue FILE.csv')
    with open(sys.argv[1], newline='') as fh: rows = list(csv.DictReader(fh))
    required = {'supplierName','supplierCategory','productName','productType','destination','supplierCost','sellingPrice'}
    if not rows: raise SystemExit('CSV contains no rows')
    missing = required - set(rows[0])
    if missing: raise SystemExit('CSV missing columns: ' + ', '.join(sorted(missing)))
    dry = os.environ.get('NURIVOYAGE_DRY_RUN') == '1'
    for row in rows:
        for key in ('supplierCost','sellingPrice'):
            if row[key]: row[key] = float(row[key])
        if dry: print('DRY-RUN', row['supplierName'], '/', row['productName']); continue
        suppliers = request('NvSupplier?textFilter=' + urllib.parse.quote(row['supplierName']))['list']
        supplier = next((x for x in suppliers if x.get('name') == row['supplierName']), None)
        if not supplier:
            supplier = request('NvSupplier', 'POST', {'name':row['supplierName'], 'category':row['supplierCategory'], 'supplierCode':row.get('supplierCode') or None, 'contactName':row.get('contactName') or None, 'website':row.get('website') or None, 'active':True})
        product = request('NvPackage', 'POST', {'name':row['productName'], 'productType':row['productType'], 'supplierId':supplier['id'], 'supplierProductCode':row.get('supplierProductCode') or None, 'destination':row['destination'], 'supplierCost':row['supplierCost'], 'supplierCostCurrency':row.get('currency') or 'ZAR', 'sellingPrice':row['sellingPrice'], 'sellingPriceCurrency':row.get('currency') or 'ZAR', 'validFrom':row.get('validFrom') or None, 'validTo':row.get('validTo') or None, 'active':True})
        print('IMPORTED', supplier['name'], '/', product['name'])

if __name__ == '__main__': main()
