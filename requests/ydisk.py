import requests
import os

token = ''

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        """Метод загруджает файл file_path на яндекс диск"""
        remote_path = os.path.basename(file_path)
        response = requests.get(
            'https://cloud-api.yandex.net/v1/disk/resources/upload',
            params={
                'path': remote_path
            },
            headers={
                'Authorization': f'OAuth {self.token}'
            }
        )
        response.raise_for_status()

        href = response.json()['href']
        with open(file_path, 'rb') as f:
            upload_response = requests.put(
                href,
                files={'file': f}
            )
            upload_response.raise_for_status()

        return True


if __name__ == '__main__':
    uploader = YaUploader(token)
    result = uploader.upload('file.txt')