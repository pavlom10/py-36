from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import diploma_adv.vk_user as vk_user
import diploma_adv.db_log as db_log


BOT_TOKEN = '' # input('Token: ')
USER_TOKEN = ''

vk = vk_api.VkApi(token=BOT_TOKEN)
longpoll = VkLongPoll(vk)

search_params = {}  # параметры поиска для последующих запросов
PER_PAGE = 10  # сколько анкет за раз

session = db_log.Session()


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


def ask_for_info(user_id, message):
    write_msg(user_id, message)
    request = ''
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text
            break

    return request


def prepare_self_info(user_id, self_info):

    if 'sex' not in self_info:
        sex = ask_for_info(user_id, 'Уточните пол (1-жен, 2-муж):')
    else:
        if self_info['sex'] == '1':
            sex = 2
        else:
            sex = 1

    if 'age' not in self_info:
        self_info['age'] = int(ask_for_info(user_id, 'Уточните возраст:'))

    if 'relation' not in self_info or self_info['relation'] == 0:
        self_info['relation'] = int(ask_for_info(user_id, 'Уточните статус (1-8):'))

    res = {
        'count': PER_PAGE,
        'offset': 0,
        'sex': sex,
        'age_from': self_info['age'] - 5,
        'age_to': self_info['age'] + 5,
        'city': self_info['city']['id'],
        'status': self_info['relation']
    }

    return res


def chat_bot():

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text

            if request == "Привет":
                write_msg(event.user_id, f"Привет, {event.user_id}...")

                # Получить информацию о пользователе
                user = vk_user.VkUser(USER_TOKEN, user_id=event.user_id)
                self_info = user.get_self_info()

                # Проходим по полученной инфе и спрашиваем недостающее (+увеличиваем offset)
                if event.user_id not in search_params:
                    search_params[event.user_id] = prepare_self_info(event.user_id, self_info)
                else:
                    search_params[event.user_id]['offset'] += PER_PAGE

                # Ищем пользователей учетом offset
                find_users = user.get_users(search_params[event.user_id])
                for user in find_users:
                    best_photos = user.get_best_photos(3)

                    if len(best_photos) == 0:
                        best_photos = ['Нет фотографий']

                    write_msg(event.user_id, user.get_url())
                    write_msg(event.user_id, best_photos)

                    search = db_log.Search(
                        owner_id=event.user_id,
                        user_id=user.owner_id,
                        photos="\n".join(best_photos)
                    )
                    session.add(search)

                # Сохраням результат в бд
                session.commit()

            else:
                write_msg(event.user_id, "Не понял вашего ответа... Наберите 'Привет' для начала.")


if __name__ == '__main__':
    chat_bot()