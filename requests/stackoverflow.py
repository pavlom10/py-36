import requests
from datetime import date, timedelta
import time

fromdate = int(time.mktime((date.today() - timedelta(days=2)).timetuple()))
tagged = 'Python'

response = requests.get(
    'https://api.stackexchange.com/2.2/questions',
    params={
        'fromdate': fromdate,
        'order': 'desc',
        'sort': 'activity',
        'tagged': tagged,
        'site': 'stackoverflow'
    }
)
response.raise_for_status()

items = response.json()['items']
for item in items:
    print(item['title'])

