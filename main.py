from datetime import datetime, timedelta

import requests

print("Enter start and end dates in format: 'Year-month-day', for example: 2015-9-7 or 2015-09-07")
start_date = str(input("Start date:"))
end_date = str(input("End date:"))
limit_str = int(input("Limit strings (integer - 3 or 5, etc.):"))
try:
    d1 = datetime.strptime(start_date, '%Y-%m-%d')
    d2 = datetime.strptime(end_date, '%Y-%m-%d')
except ValueError:
    print("Incorrect format")

# for test
# d1 = date(2015, 9, 7)
# d2 = date(2015, 9, 8)
# limit_str = 3

payload = {'start_date': d1, 'end_date': d2, 'api_key': 'DEMO_KEY'}
response = requests.get('https://api.nasa.gov/neo/rest/v1/feed?', params=payload)
r_content = response.json()


def daterange(d1, d2):
    for n in range(int((d2 - d1).days + 1)):
        yield d1 + timedelta(n)


all_result = []
for single_date in daterange(d1, d2):
    all_result.clear()
    current_date = single_date.strftime("%Y-%m-%d")

    near_objects = r_content['near_earth_objects']
    dates = near_objects[current_date]
    count = 0
    for keys in dates:
        id = keys['neo_reference_id']
        name = keys['name']
        magnitude = keys['absolute_magnitude_h']
        haz = keys['is_potentially_hazardous_asteroid']
        obj = {'date': current_date, 'neo_reference_id': id, 'name': name, 'absolute_magnitude_h': magnitude,
               'is_potentially_hazardous_asteroid': haz}
        all_result.append(obj)
        count += 1

    all_result = sorted(all_result, key=lambda result: (result['date'], -result['absolute_magnitude_h']))
    del all_result[limit_str:count]
    print(all_result)
