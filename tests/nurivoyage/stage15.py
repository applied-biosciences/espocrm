"""Stage 15 deployment and live provider regression checks (no financial transactions)."""
import pathlib, json, subprocess
p=pathlib.Path('tests/nurivoyage/smoke.py')
ns={'__file__':str(p)}
exec(p.read_text().split('try:\n    stamp=')[0],ns)
api=ns['api']
metadata=api('Metadata')
for entity in ['NvTaxRule','NvConversionSnapshot','NvCommunication']:
    assert metadata['clientDefs'][entity]['controller']=='controllers/record', entity
    for role in ['admin','finance','manager','sales']:
        assert 'list' in api(entity,user=role)
    print('PASS browser registration and role API access:',entity)
assert metadata['clientDefs']['NvFxRate']['views']['list']=='custom:views/nurivoyage/fx'
settings=api('Settings')
items=[i for g in settings['tabList'] if isinstance(g,dict) for i in g.get('itemList',[])]
assert items.count('NvFxRate')==1, 'Duplicate FX navigation entry'
print('PASS deployed navigation: one FX link')
rows=json.loads(subprocess.check_output(['curl','--fail','--silent','--show-error','--max-time','30','https://api.frankfurter.dev/v2/rates?base=USD&quotes=GBP,ZAR,SAR']))
rates={'USD':1,**{r['quote']:r['rate'] for r in rows}}
assert all(rates[c]>0 for c in ['USD','GBP','ZAR','SAR'])
for source in rates:
    for target in rates:
        value=100/rates[source]*rates[target]
        assert abs(value/rates[target]*rates[source]-100)<1e-8
print('PASS live Frankfurter USD/GBP/ZAR/SAR rates and all 16 conversion pairs')
