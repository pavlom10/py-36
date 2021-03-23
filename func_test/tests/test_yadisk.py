import requests

token = ''
headers = {'Authorization': f'OAuth {token}'}
url = 'https://cloud-api.yandex.net/v1/disk/resources'
path = 'test'
wrong_path = 'test_no_such_dir'

class TestYadisk:

    def test_make_new_dir(self):
        response = requests.put(
            url,
            params={
                'path': path
            },
            headers=headers
        )
        assert response.status_code == 201

    def test_check_dir_exist(self):
        response = requests.get(
            url,
            params={
                'path': path
            },
            headers=headers
        )
        assert response.status_code == 200

    def test_check_wrong_dir(self):
        response = requests.get(
            url,
            params={
                'path': wrong_path
            },
            headers=headers
        )
        assert response.status_code == 404

    def test_delete_dir(self):
        response = requests.delete(
            url,
            params={
                'path': path,
                'permanently': True
            },
            headers=headers
        )
        assert response.status_code == 204
