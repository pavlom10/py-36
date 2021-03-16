import json
from urllib.parse import quote

class CountryStreamer:

    def __init__(self, file_name):
        self.file_name = file_name

        country_names = []
        with open(file_name) as json_file:
            data = json.load(json_file)
            for item in data:
                country_names.append(item['name']['official'])

        self.country_names = iter(country_names)

    def __iter__(self):
         return self

    def __next__(self):
        return next(self.country_names)


if __name__ == '__main__':
    countries = CountryStreamer('countries.json')
    with open('countries.txt', 'w') as file:
        for name in countries:
             file.write(f"{name} + https://en.wikipedia.org/wiki/{quote(name)}")
             file.write('\n')

