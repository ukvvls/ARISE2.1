#!/usr/bin/env python3
"""Update ARISE's static data cache. Uses only Python standard library."""
import json, os, urllib.parse, urllib.request, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'data.json'
CURRENCIES = 'USD,EGP,GBP,JPY,CAD,AUD,CHF,CNY,AED,SAR,KWD,TRY,INR,ZAR,SEK,NOK,DKK,NZD,BRL,MXN,HKD,SGD,PLN,CZK,HUF,RON,BGN,ISK,KRW'
TODAY = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')

def fetch_json(url, timeout=25):
    req = urllib.request.Request(url, headers={'User-Agent': 'ARISE-Financial-Intelligence/2.1 data-cache'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))

old = {}
if OUT.exists():
    try: old = json.loads(OUT.read_text(encoding='utf-8'))
    except Exception: old = {}
new = {'generatedAt': TODAY, 'fx': old.get('fx'), 'news': old.get('news'), 'status': {'fx': 'cached' if old.get('fx') else 'unavailable', 'news': 'cached' if old.get('news') else 'unavailable'}}
# FX: daily reference rates, not intraday trading quotes.
try:
    url = 'https://api.frankfurter.dev/v1/latest?base=EUR&symbols=' + urllib.parse.quote(CURRENCIES, safe=',')
    payload = fetch_json(url)
    if payload.get('rates') and payload.get('date'):
        new['fx'] = {'date': payload['date'], 'base': payload.get('base', 'EUR'), 'rates': payload['rates'], 'source': 'Frankfurter'}
        new['status']['fx'] = 'updated'
except Exception as err:
    new['status']['fx'] = 'stale' if old.get('fx') else 'unavailable'
    new['errors'] = new.get('errors', []) + ['FX fetch: ' + str(err)[:180]]
# GDELT news snapshot. Retain old cache if the feed is temporarily unreachable.
try:
    params = urllib.parse.urlencode({'query':'finance sourcelang:english', 'mode':'ArtList', 'format':'json', 'maxrecords':'12', 'sort':'HybridRel'})
    payload = fetch_json('https://api.gdeltproject.org/api/v2/doc/doc?' + params)
    articles = payload.get('articles', [])
    if articles:
        new['news'] = {'generatedAt': TODAY, 'source':'GDELT', 'articles':articles[:12]}
        new['status']['news'] = 'updated'
except Exception as err:
    new['status']['news'] = 'stale' if old.get('news') else 'unavailable'
    new['errors'] = new.get('errors', []) + ['News fetch: ' + str(err)[:180]]
OUT.write_text(json.dumps(new, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Updated data.json; statuses:', new['status'])
