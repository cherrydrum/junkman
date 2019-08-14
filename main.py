import requests as r
import configparser
import utils
from tabulate import tabulate

vklink = 'https://api.vk.com/method/'

# Создадим класс соединения для хранения нужных данных.
class Connection():
    def __init__(self, filename='config.txt'):
        buf = configparser.ConfigParser()
        buf.read(filename)
        # Сюда можно добавить еще каких-либо параметров
        self.token = buf['CONFIG']['api_token']

    def _req(self, method, data):
        response = r.get(vklink + str(method),
                         params={**data, 'v':'5.0', 'access_token': self.token})
        response = response.json()
        if 'error' in response.keys():
            raise BaseException(response['error']['error_msg'])
        else:
            return response['response']

class User():
    domain = None
    id = None
    def __init__(self, master, uid, verbose=True):
        self.conn = master
        if type(uid) == str:
            self.domain = uid
        elif type(uid) == int:
            self.id = uid
        if verbose or not self.id:
            self.fetch()

    def fetch(self, fields=None):
        if self.id:
            print('Fetching ' + str(self.id))
            if fields:
                raw = self.conn._req('users.get', {'user_ids': self.id, 'fields': 'domain,'+','.join(fields)})[0]
            else:
                raw = self.conn._req('users.get', {'user_ids': self.id, 'fields': 'domain'})[0]
        elif self.domain:
            print('Fetching ' + self.domain)
            if fields:
                raw = self.conn._req('users.get', {'user_ids': self.domain, 'fields': ','.join(fields)})[0]
            else:
                raw = self.conn._req('users.get', {'user_ids': self.domain})[0]
        else: raise BaseException('WTF?')
        if raw:
            self.__dict__ = {**self.__dict__, **raw}

    def get_friends(self, verbose=True):
        raw = self.conn._req('friends.get', {'user_id': self.id})['items']
        raw = [User(self.conn, a, verbose=False) for a in raw]
        self.friends = Pack(self.conn, raw)

    def overview(self):
        data = [ [i, str(self.__dict__[i])] for i in self.__dict__.keys() if i != 'conn']
        print(tabulate(data, headers=['column', 'value']))

    def __repr__(self):
        try:
            return '<User {} {}>'.format(self.first_name, self.last_name)
        except AttributeError:
            return '<User {}>'.format(self.id)

class Pack():
    def __init__(self, master, objects):
        self.contents = objects
        self.conn = master

    def fetch(self, fields=None):
        for item in self.contents:
            print('Fetching ' + str(item.id))
            if fields:
                raw = self.conn._req('users.get', {'user_ids': self.domain, 'fields': ','.join(fields)})[0]
            else:
                raw = self.conn._req('users.get', {'user_ids': self.domain})[0]
            item.__dict__ = {**item.__dict__, **raw}

    def get(self, **kwargs):
        criteria = kwargs
        for i in criteria.keys():
            utils.currentfilter = i
            utils.questionvalue = criteria[i]
            a = filter(utils.compare, self.contents)
        if len(a) == 1:
            return a[0]
        else:
            return Pack(self.conn, a)

    def prettyprint(self, columns):
        rows = []
        for item in self.contents:
            data = []
            for column in columns:
                try:
                    data.append(item.__dict__[column])
                except AttributeError:
                    data.append('-/-')
            rows.append(data)
        print(tabulate(rows, headers=columns))

    def __repr__(self):
        return 'Humble pack of {} items'.format(len(self.contents))





