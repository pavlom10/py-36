import diploma_adv.vk_user as vk_user

TEST_TOKEN = ''

def test_vk_user():
    user = vk_user.VkUser(TEST_TOKEN)
    assert isinstance(user, vk_user.VkUser)

def test_vk_get_users():
    user = vk_user.VkUser(TEST_TOKEN)
    users = user.get_users({'count': 10, 'offset': 0})
    assert isinstance(users[0], vk_user.VkUser)
