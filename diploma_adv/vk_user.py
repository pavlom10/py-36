import requests


class VkUser:
    api_url = 'https://api.vk.com/method/'
    url = 'https://vk.com/'

    def __init__(self, token, version=5.126, user_id=None, domain=None):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        if user_id is None:
            self.owner_id = requests.get(self.api_url + 'users.get', self.params).json()['response'][0]['id']
        else:
            self.owner_id = user_id
        self.domain = domain

    def get_users(self, user_params):
        url = self.api_url + 'users.search'
        search_params = {
            'has_photo': 1,
            'sort': 0,
            'fields': 'domain'
        }
        res = requests.get(url, params={**self.params, **search_params, **user_params})

        user_profiles = []
        for item in res.json()['response']['items']:
            user_profiles.append(VkUser(self.token, user_id=item['id'], domain=item['domain']))

        return user_profiles

    def get_photos(self, user_id=None, limit=None):
        if user_id is None:
            user_id = self.owner_id
        photos_url = self.api_url + 'photos.get'
        photos_params = {
            'count': limit,
            'user_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 0
        }
        response = requests.get(photos_url, params={**self.params, **photos_params})
        res = response.json()

        if 'error' in res:
            # print(res['error']['error_msg'])
            return []

        return res['response']['items']

    def get_best_photos(self, count=3):

        photos = self.get_photos()

        dump = {}
        for item in photos:
            max_size = -1
            url = ''
            for photo in item['sizes']:
                size = photo['width'] + photo['height']
                if size > max_size:
                    url = photo['url']
                    max_size = size

            dump[url] = item['likes']['count'] + item['comments']['count']

        best_photos = [k for k, v in sorted(dump.items(), key=lambda x: x[1], reverse=True)]

        return best_photos[:count]

    def get_url(self):
        if self.domain:
            return self.url + self.domain
        else:
            return self.url + 'id' + str(self.owner_id)

    def get_self_info(self):
        url = self.api_url + 'users.get'
        params = {
            'fields': 'sex,city,age,status'
        }
        response = requests.get(url, params={**self.params, **params})
        res = response.json()['response'][0]

        return res

    def get_city_id(self, name):
        url = self.api_url + 'database.getCities'
        params = {
            'country_id': 1,
            'q': name
        }

        response = requests.get(url, params={**self.params, **params})
        res = response.json()['response']

        if res['count'] == 0:
            return None

        return res['items'][0]['id']
