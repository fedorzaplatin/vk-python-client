from other import select


class Friends:

    def __init__(self, api, config):
        self.__api = api
        self.__friends_list = api.friends.get(user_id='', order='hints', fields='nickname')
        self.__friends_list = self.__friends_list['items']
        self.__config = config
        self.__friends_online_list = []

    def list(self):
        """Выводит список друзей"""
        n = 1
        for x in self.__friends_list:
            print(n, end='. ')
            print(x['first_name'], x['last_name'], end='. ')
            if x['online'] == 1 and self.__config.getboolean('FRIENDS', 'show_status'):
                print('Online', end='. ')
            elif self.__config.getboolean('FRIENDS', 'show_status'):
                print('Offline', end='. ')
            if self.__config.getboolean('FRIENDS', 'show_ids'):
                print('id:', x['user_id'])
            else:
                print()
            n += 1

    def online_list(self):
        """Выводит список друзей онлайн"""
        self.update_data()
        n = 1
        for x in self.__friends_online_list:
            print(n, end='. ')
            print(x['first_name'], x['last_name'], end='. ')
            if self.__config.getboolean('FRIENDS', 'show_ids'):
                print('id:', x['user_id'])
            else:
                print()
            n += 1

    def select_friend(self, online=0):
        """Выбор друга из списка друзей(или из списка друзей онлайн, при передаче аргумента online=1).
        Возвращает словарь с id, именем и фамилией выбранного друга.

        """
        if online == 1:
            self.online_list()
            print(len(self.__friends_online_list) + 1, '. Назад', sep='')
            num = select(len(self.__friends_online_list) + 1)
            if num == len(self.__friends_online_list) + 1:
                return ''
            user = self.__friends_online_list[num - 1]
        else:
            self.list()
            print(len(self.__friends_list) + 1, '. Назад', sep='')
            num = select(len(self.__friends_list) + 1)
            if num == len(self.__friends_list) + 1:
                return ''
            user = self.__friends_list[num - 1]

        tmp = dict(user_id=user['id'], first_name=user['first_name'], last_name=user['last_name'])
        return tmp

    def update_data(self):
        """Обновляет список друзей и список друзей онлайн"""
        self.__friends_list = self.__api.friends.get(user_id='', order='hints', fields='nickname')
        self.__friends_list = self.__friends_list['items']
        self.__friends_online_list = []
        for x in self.__friends_list:
            if x['online'] == 1:
                self.__friends_online_list.append(x)

    def get_user_friends(self, uid):
        """Выводит список друзей пользователя с указаным id"""
        f_list = self.__api.friends.get(user_id=uid, order='hints', fields='nickname')
        f_list = f_list['items']
        n = 1
        for x in f_list:
            print(n, end='. ')
            print(x['first_name'], x['last_name'], end='. ')
            if x['online'] == 1 and self.__config.getboolean('FRIENDS', 'show_status'):
                print('Online', end='. ')
            elif self.__config.getboolean('FRIENDS', 'show_status'):
                print('Offline', end='. ')
            if self.__config.getboolean('FRIENDS', 'show_ids'):
                print('id:', x['user_id'])
            else:
                print()
            n += 1
