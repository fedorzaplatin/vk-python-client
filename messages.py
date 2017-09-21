import os
import sys
import time
import users
from other import action_date


def send_msg(api, uid='', chat_id=None):
    """Функция отправки сообщения"""
    msg = str(input('Введите сообщение: '))
    if uid != '':
        api.messages.send(user_id=uid, message=msg)
    else:
        api.messages.send(chat_id=chat_id, message=msg)


def get_dialogs_list(api):
    """Выводит список диалогов и созвращает список, в котором они содержаться"""
    dialog_list = api.messages.getDialogs()
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    print('Количество диалогов:', dialog_list['count'])
    dialog_list = dialog_list['items']
    i = 0
    while i < len(dialog_list):
        dialog = dialog_list[i]
        dialog = dialog['message']
        if dialog['title'] == ' ... ':
            print('{}. {}:'.format(i + 1, users.get_name_lastname(api, dialog['user_id'])))
            if dialog['body'] == '':
                print('\t[Вложение] -', action_date(dialog['date']), sep='')
            else:
                try:
                    print('\t{} - {}'.format(dialog['body'].translate(non_bmp_map), action_date(dialog['date'])))
                except UnicodeEncodeError:
                    print('\temoji :) -', action_date(dialog['date']))
        else:
            print('{}. {}. {}:'.format(i + 1, dialog['title'].translate(non_bmp_map),
                                       users.get_name_lastname(api, dialog['user_id'])))
            try:
                print('\t{} - {}'.format(dialog['body'].translate(non_bmp_map), action_date(dialog['date'])))
            except UnicodeEncodeError:
                print('\temoji :) -', action_date(dialog['date']))
        i += 1
        time.sleep(0.34)
    return dialog_list


def get_message_history(api, config, dialog):
    """Выводит историю сообщений для указаного диалога"""
    os.system('cls')
    if dialog.get('chat_id', 'none') == 'none':
        user = api.users.get(user_ids=dialog['user_id'])
        user = user[0]
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        msgs = api.messages.getHistory(user_id=dialog['user_id'], count=config.get('MESSAGES', 'num_messages'))
        msgs = msgs['items']

        if config.getboolean('MESSAGES', 'reverse_messages'):
            msgs.reverse()

        i = 0
        while i < len(msgs):
            msg = msgs[i]
            if msg['out'] == 1:
                print('Вы:', end=' ')
            else:
                print(user['first_name'], ':', sep='', end=' ')
            try:
                print(msg['body'].translate(non_bmp_map), '-', action_date(msg['date']))
            except UnicodeEncodeError as e:
                print('emoji :) -', action_date(msg['date']))
            i += 1
    else:
        print('Просмотр сообщений в диалоге находится с стадии разработки\n')
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        msgs = api.messages.getHistory(user_id=2000000000 + dialog['chat_id'],
                                       count=config.getint('MESSAGES', 'num_messages'))
        msgs = msgs['items']

        i = 0
        while i < len(msgs):
            msg = msgs[i]
            if msg['out'] == 1:
                print('Вы:', end=' ')
            else:
                print('Other user:', sep='', end=' ')
            try:
                print(msg['body'].translate(non_bmp_map), '-', action_date(msg['date']))
            except UnicodeEncodeError:
                print('emoji :) -', action_date(msg['date']))
            i += 1
    return dialog


def check_messages(api):
    dialog_list = api.messages.getDialogs(unread='1')
    return dialog_list['count']
