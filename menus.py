import messages
import users
import os
import account
from other import select


def get_api_menu():
    api = account.get_api()
    while api == '':
        os.system('cls')
        print('Токен отсутствует/введён неверно/не действителен\n')
        print('1. Открыть инструкцию о получении токена')
        print('2. Открыть файл для вставки токена')
        print('3. Проверить ещё раз')
        print('4. Выход')
        choice = input('Выберите: ')

        if choice == '1':
            os.system('start .\\data\\help.dat')
        elif choice == '2':
            os.system('start .\\data\\token.dat')
        elif choice == '3':
            api = account.get_api()
            if api != '':
                os.system('cls')
                print('Токен получен :)\n')
                os.system('pause')
            else:
                os.system('cls')
                print('Всё равно не работает :(\n')
                os.system('pause')
        elif choice == '4':
            exit()
    return api


def friends_menu(friends, api):
    while True:
        os.system('cls')
        print('Друзья\n')
        print('1. Мои друзья')
        print('2. Мои онлайн друзья')
        print('3. Список друзей одного из Ваших друзей')
        print('4. Назад')
        choice = input('Выберите: ')

        if choice == '1':
            os.system('cls')
            user = friends.select_friend()
            if user != '':
                users.get_information(api, user['user_id'])
                os.system('pause')
        elif choice == '2':
            os.system('cls')
            user = friends.select_friend(online=1)
            if user != '':
                users.get_information(api, user['user_id'])
                os.system('pause')
        elif choice == '3':
            os.system('cls')
            user = friends.select_friend()
            os.system('cls')
            if user != '':
                friends.get_user_friends(user['user_id'])
            os.system('pause')
        elif choice == '4':
            break


def messages_menu(api, friends, config):
    while True:
        os.system('cls')
        print('Сообщения\n')
        print('1. Диалоги')
        print('2. Отправить сообщение')
        print('3. Назад')
        choice = input('Выберите: ')

        if choice == '1':
            dialogs_menu(api, config)
        elif choice == '2':
            send_message(api, friends)
        elif choice == '3':
            break


def dialogs_menu(api, config):
    while True:
        os.system('cls')
        print('Диалоги\n')

        dialog_list = messages.get_dialogs_list(api)
        print(len(dialog_list) + 1, '. Назад', sep='')
        num = select(len(dialog_list) + 1)
        if num == len(dialog_list) + 1:
            return None
        else:
            dialog = dialog_list[num - 1]
            dialog = dialog['message']
            dialog_menu(api, config, dialog)


def dialog_menu(api, config, dialog):
    while True:
        if dialog.get('chat_id', 'none') == 'none':
            user = api.users.get(user_ids=dialog['user_id'])
            user = user[0]
            print('Выбран(а)', user['first_name'], user['last_name'],'\n')
        else:
            print('Выбран диалог "{}"\n'.format(dialog['title']))

        messages.get_message_history(api, config, dialog)

        print()
        print('1. Написать сообщение в диалог')
        print('2. Назад')
        choice = input('Выберите: ')

        if choice == '1':
            if dialog.get('chat_id', 'none') == 'none':
                messages.send_msg(api, dialog['user_id'])
                print('Отправлено!')
                os.system('pause')
            else:
                messages.send_msg(api, chat_id=dialog['chat_id'])
                print('Отправлено!')
                os.system('pause')
        elif choice == '2':
            return None


def send_message(api, friends):
    while True:
        os.system('cls')
        print('Отправить сообщение\n')
        print('1. Выбрать друга')
        print('2. Оправить конткретному пользователю (потребуется ввод id)')
        print('3. Назад')
        choice = input('Выберите: ')

        if choice == '1':  # Отправить другу
            os.system('cls')
            f = friends.select_friend()
            if f != '':
                os.system('cls')
                print('Выбран(а)', f['first_name'], f['last_name'])
                messages.send_msg(api, f['user_id'])
                print('Отправлено!')
                os.system('pause')
        elif choice == '2':  # Отправить пользователю
            uid = users.get_id()
            while users.check_id(uid, api):
                print('Аккаунт удален или не существует!')
                os.system('pause')
                uid = users.get_id()

            user = api.users.get(user_ids=uid)
            user = user[0]
            print('Выбран(а)', user['first_name'], user['last_name'])
            messages.send_msg(api, uid)
            print('Отправлено!')
            os.system('pause')
        elif choice == '3':
            return None


def account_menu(api):
    while True:
        os.system('cls')
        print('Действия с аккаунтом\n')
        print('1. Отправить онлайн статус')
        print('2. Отправить оффлайн статус')
        print('3. Назад')
        choice = input('Выберите: ')

        if choice == '1':
            account.set_online(api)
        elif choice == '2':
            account.set_offline(api)
        elif choice == '3':
            break


def settings_menu(config):
    while True:
        os.system('cls')
        print('Настройки\n')
        if config.getboolean('FRIENDS', 'show_ids'):
            print('1. Отключить отображение id в списке друзей')
        else:
            print('1. Включить отображение id в списке друзей')
        print('2. Изменить количество сообщений выводимых при просмотре')
        if config.getboolean('MESSAGES', 'reverse_messages'):
            print('3. Выводить сообщения от более ранних к более поздним')
        else:
            print('3. Выводить сообщения от более поздних к более ранним')
        if config.getboolean('FRIENDS', 'show_status'):
            print('4. Не показывать статус в списке друзей (Online/Offline)')
        else:
            print('4. Показывать статус в списке друзей (Online/Offline)')
        print('5. Сохранить и выйти')
        choice = input('Выберите: ')

        if choice == '1':
            tmp = not config.getboolean('MESSAGES', 'show_ids')
            config.set('FRIENDS', 'show_ids', str(tmp))
        elif choice == '2':
            num = int(input('Введите желаемое количество(0 < x <= 200): '))
            config.set('MESSAGES', 'num_messages', str(num))
        elif choice == '3':
            tmp = not config.getboolean('MESSAGES', 'reverse_messages')
            config.set('MESSAGES', 'reverse_messages', str(tmp))
        elif choice == '4':
            tmp = not config.getboolean('FRIENDS', 'show_status')
            config.set('FRIENDS', 'show_status', str(tmp))
        elif choice == '5':
            file = open('./data/settings.ini', 'w+')
            config.write(file)
            file.close()
            break
