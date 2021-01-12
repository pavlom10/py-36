import requests

token = ''

class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version=5.126, user_id=None):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        if user_id is None:
            self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']
        else:
            self.owner_id = user_id

    def get_mutual_friends(self, target_id):
        friends_url = self.url + 'friends.getMutual'
        friends_params = {
            'source_uid': self.owner_id,
            'target_uid': target_id
        }
        res = requests.get(friends_url, params={**self.params, **friends_params})
        user_profiles = []
        for user_id in res.json()['response']:
            user_profiles.append(VkUser(self.token, user_id=user_id))

        return user_profiles

    def __and__(self, other):
        return self.get_mutual_friends(other.owner_id)

    def __str__(self):
        return 'http://vk.com/id' + str(self.owner_id)


if __name__ == '__main__':
    user_1 = VkUser(token, user_id=6492)
    user_2 = VkUser(token, user_id=2745)
    mutual_friends = user_1 & user_2
    for user in mutual_friends:
        print(user)