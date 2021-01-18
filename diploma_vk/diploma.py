import requests
import json
import os
from urllib.parse import urlparse

vk_token = ''

class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version=5.126):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']

    def get_photos(self, user_id=None, limit=5):
        if user_id is None:
            user_id = self.owner_id
        photos_url = self.url + 'photos.get'
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
            print(res['error']['error_msg'])
            return []

        return res['response']['items']

    def prepare_photos_to_dump(self, photos):
        dump = {}
        for item in photos:
            max_size = -1
            url = ''
            for photo in item['sizes']:
                size = photo['width'] + photo['height']
                if size > max_size:
                    url = photo['url']
                    max_size = size

            name = str(item['likes']['count'])
            if name in dump:
                name += '_' + str(item['date'])

            path = urlparse(url).path
            ext = os.path.splitext(path)[1]
            name += ext
            dump[name] = url

        return dump


class YaDisk:

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'OAuth {self.token}'
        }

    def make_new_dir(self, path):
        response = requests.put(
            'https://cloud-api.yandex.net/v1/disk/resources',
            params={
                'path': path
            },
            headers=self.headers
        )
        res = response.status_code # == 409
        return res

    def upload_from_url(self, url, path):
        response = requests.post(
            'https://cloud-api.yandex.net/v1/disk/resources/upload',
            params={
                'url': url,
                'path': path,
            },
            headers=self.headers
        )
        response.raise_for_status()
        res = response.json()
        return res

    def wait_for_upload(self, res):
        is_ok = False
        response_counter = 0
        response_counter_limit = 30
        print('Uploading.', end='')

        while not is_ok:
            response_counter += 1
            if (response_counter > response_counter_limit):
                print('Too long request or something wrong')
                break
            response = requests.get(
                res['href'],
                headers=self.headers
            )
            status = response.json()['status']
            if status == 'success':
                print('Ok')
                is_ok = True
            elif status == 'failed':
                print('Failed')
                break
            else:
                print('.', end='')

        return is_ok

    def get_file_info(self, path):
        response = requests.get(
            'https://cloud-api.yandex.net/v1/disk/resources',
            params={
                'path': path,
                'fields': 'size'
            },
            headers=self.headers
        )
        response.raise_for_status()
        res = response.json()
        return res


def dump_photos_from_vk_to_yadisk(vk_id, ya_token, limit=5, dir_name='Diploma'):
    user = VkUser(vk_token)
    photos = user.get_photos(vk_id, limit)
    if len(photos):
        dump = user.prepare_photos_to_dump(photos)
        uploader = YaDisk(ya_token)
        uploader.make_new_dir(dir_name)
        json_log = []

        for name, url in dump.items():
            print('File: ' + name)
            path = dir_name + '/' + name
            result = uploader.upload_from_url(url=url, path=path)
            is_uploaded = uploader.wait_for_upload(result)
            if is_uploaded:
                res = uploader.get_file_info(path)
                json_log.append({'file_name': name, 'size': res['size']})

        with open('log.json', 'w') as outfile:
            json.dump(json_log, outfile)
        print('Done')

if __name__ == '__main__':
    vk_id = int(input('Vk id: '))
    ya_token = input('Polygon token: ')
    dump_photos_from_vk_to_yadisk(vk_id, ya_token)