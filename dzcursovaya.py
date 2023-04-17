import requests
import json
from pprint import pprint
import time


with open('tokenvk.txt') as f1:
    token = f1.read().strip()

with open('yatoken.txt') as f2:
    yatoken = f2.read().strip()


class VK:
    url = 'https://api.vk.com/method/'

    def __init__(self, token=token, version=5.131):
        self.params = {
            'access_token': token,
            'v': version
        }

    @classmethod
    def get_photos(cls, owner_id):
        all_photos_url = {}

        photos_get_url = 'https://api.vk.com/method/photos.get'
        photos_get_params = {
            'album_id': 'profile',
            'owner_id': owner_id,
            'rev': 1,
            'extended': 1,
            'access_token': token,
            'v': 5.131
        }
        req = requests.get(photos_get_url, params={**photos_get_params}).json()

        for photo in req['response']['items']:
            if photo['likes']['count'] in all_photos_url.keys():
                all_photos_url[photo['likes']['count'], time.gmtime(photo['date'])] = photo['sizes'][-1]['url']
            else:
                all_photos_url[photo['likes']['count']] = photo['sizes'][-1]['url']
            time.sleep(0.3)
        return all_photos_url


class YandexDisk:
    def __init__(self, token):
        self.token = token
        self.yandex_url = 'https://cloud-api.yandex.net/'

    def get_headers(self):
         return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def upload_file_to_disk(self, owner_id):
        headers = self.get_headers()
        upload_url = f'{self.yandex_url}v1/disk/resources/upload'
        a = VK.get_photos(owner_id=owner_id)
        for k, v in a.items():
            params = {
                'url': v,
                'path': k
            }
            response = requests.post(upload_url, headers=headers, params=params)
            response.raise_for_status()
            if response.status_code == 202:
                print("Success")


if __name__ == '__main__':
    # vk_user = VK(token)

    yandex_disk = YandexDisk(token=yatoken  )
    yandex_disk.upload_file_to_disk()
