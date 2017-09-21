import os
from other import action_date


def check_id(uid, api):
    """Проверяет правильность введенного id"""
    tmp = api.users.get(user_id=uid)
    tmp2 = tmp[0]
    if tmp2.get('deactivated', 'none') == 'none':
        return False
    else:
        return True


def get_id():
    os.system('cls')
    uid = input('Введите id пользователя: ')
    return uid


def get_name_lastname(api, uid):
    """Возвращает сроку содержащую имя и фамилию пользователя с указаным id"""
    user = api.users.get(user_ids=uid)
    user = user[0]
    tmp = user['first_name'] + ' ' + user['last_name']
    return tmp


def get_information(api, uid):
    """Выводит основную информацию страницы пользователя с указанным id"""
    user = api.users.get(user_ids=uid,
                         fields='bdate,city,home_town,online,domain,status,contacts,site,last_seen,relation,'
                                'activities,interests,music,movies,tv,books,games,about,quotes,connections')
    user = user[0]
    os.system('cls')

    print(user['first_name'], user['last_name'], end='. ')
    if user['online'] == 1:
        print('Online', end='. ')
    else:
        print('Offline', end='. ')
    print(action_date(user['last_seen']['time']), end=' ')
    if user['last_seen']['platform'] == 1:
        print('c m.vk.com')
    elif user['last_seen']['platform'] == 2:
        print('с iPhone')
    elif user['last_seen']['platform'] == 3:
        print('с iPad')
    elif user['last_seen']['platform'] == 4:
        print('с Android')
    elif user['last_seen']['platform'] == 5:
        print('с Windows Phone')
    elif user['last_seen']['platform'] == 6:
        print('с Windows Desktop')
    elif user['last_seen']['platform'] == 7:
        print('с vk.com')

    print('vk.com/{}. id: {}.'.format(user['domain'], user['id']))
    print('Статус:', user['status'])
    if user.get('bdate', False):
        print('Дата рождения: ', user['bdate'])

    if user.get('relation', False):
        print('Семейное положение:', end=' ')
        if user['relation'] == 0:
            print('не указано')
        elif user['relation'] == 1:
            print('не женат/не замужем')
        elif user['relation'] == 2:
            print('есть друг/есть подруга')
        elif user['relation'] == 3:
            print('помолвлен/помолвлена')
        elif user['relation'] == 4:
            print('женат/замужем')
        elif user['relation'] == 5:
            print('всё сложно')
        elif user['relation'] == 6:
            print('в активном поиске')
        elif user['relation'] == 7:
            print('влюблён/влюблена')

    if user.get('site', False):
        print('Веб-сайт:', user['site'])
    if user.get('home_town', False):
        print('Родной город:', user['home_town'])
    if user.get('mobile_phone', False):
        print('Моб. телефон:', user['mobile_phone'])
    if user.get('home_phone', False):
        print('Доп. телефон:', user['home_phone'])
    if user.get('skype', False):
        print('Skype:', user['skype'])
    if user.get('facebook', False):
        print('Facebook:', user['facebook'])
    if user.get('twitter', False):
        print('Twitter:', user['twitter'])
    if user.get('livejournal', False):
        print('Livejournal:', user['livejournal'])
    if user.get('instagram', False):
        print('Instasgram:', user['instagram'])

    if user.get('activities', False):
        print('Деятельность:', user['activities'])
    if user.get('interests', False):
        print('Интересы:', user['interests'])
    if user.get('music', False):
        print('Любимая музыка:', user['music'])
    if user.get('movies', False):
        print('Любимые фильмы: ', user['movies'])
    if user.get('tv', False):
        print('Любимые телешоу:', user['tv'])
    if user.get('books', False):
        print('Любимые книги:', user['books'])
    if user.get('games', False):
        print('Любимые игры:', user['games'])
    if user.get('quotes', False):
        print('Любимые цитаты:', user['quotes'])
    if user.get('about', False):
        print('О себе:', user['about'])
