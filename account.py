import os
import vk


def set_online(api):
    os.system('cls')
    tmp = api.account.setOnline()
    if tmp == 1:
        print('Успешно')
    os.system('pause')


def set_offline(api):
    os.system('cls')
    tmp = api.account.setOffline()
    if tmp == 1:
        print('Успешно')
    os.system('pause')


def get_api():
        if not os.path.exists('.\\data\\token.dat') or os.stat('.\\data\\token.dat').st_size == 0:
            file = open('.\\data\\token.dat', 'w')
            file.close()
            return ''
        else:
            file = open('.\\data\\token.dat')
            token = file.read()
            file.close()
            session = vk.Session(access_token=token)
            api = vk.API(session, v='5.60')
            try:
                api.users.get()
                return api
            except vk.exceptions.VkAPIError:
                return ''
