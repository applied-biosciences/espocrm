import pathlib, uuid
ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / 'tests/nurivoyage/smoke.py'
source = p.read_text(); ns = {'__file__': str(p)}
exec(source[:source.index('try:\n    stamp=')], ns)
api = ns['api']; stamp = uuid.uuid4().hex[:8]
meta = api('Metadata')['entityDefs']
assert {'contactName','website','supplierCode','active'}.issubset(meta['NvSupplier']['fields'])
assert {'productType','supplier','supplierProductCode','supplierCost','sellingPrice','validFrom','validTo','active'}.issubset(meta['NvPackage']['fields'])
supplier = api('NvSupplier', 'POST', {'name':'Stage 8 Synthetic Airline '+stamp,'category':'Airline','supplierCode':'AIR-'+stamp,'contactName':'Catalogue Contact','active':True}, user='operations')
product = api('NvPackage', 'POST', {'name':'Stage 8 Synthetic Flight '+stamp,'productType':'Flight','supplierId':supplier['id'],'supplierProductCode':'FL-'+stamp,'destination':'Jeddah','supplierCost':4200,'supplierCostCurrency':'ZAR','sellingPrice':5100,'sellingPriceCurrency':'ZAR','active':True}, user='operations')
detail = api('NvPackage/'+product['id'], user='operations')
assert detail.get('supplierId') == supplier['id'] and detail.get('sellingPrice') == 5100
assert detail.get('name', '').endswith(stamp)
print('PASS Stage 8 supplier and product catalogue lifecycle')
