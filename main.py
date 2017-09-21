import os
import configparser

import menus
from messages import check_messages
import class_friends


def main():
    api = menus.get_api_menu()
    config = configparser.ConfigParser()
    config.read('./data/settings.ini')
    friends = class_friends.Friends(api, config)

    while True:
        new_msgs = check_messages(api)
        os.system('cls')

        print('Главное меню\n')
        print('1. Друзья')
        if new_msgs == 0:
            print('2. Сообщения')
        else:
            print('2. Сообщения. Имеются новые сообщения ({})'.format(new_msgs))
        print('3. Действия с аккаунтом')
        print('4. Настройки')
        print('5. Выход')
        choice = input('Выберите действие: ')

        if choice == '1':
            menus.friends_menu(friends, api)
        elif choice == '2':
            menus.messages_menu(api, friends, config)
        elif choice == '3':
            menus.account_menu(api)
        elif choice == '4':
            menus.settings_menu(config)
        elif choice == '5':
            exit(0)

if __name__ == '__main__':
    main()
