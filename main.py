import requests as r
import configparser
import json

vklink = 'https://api.vk.com/method/'

# Создадим класс соединения для хранения нужных данных.
class Connection():
    def __init__(self, filename):
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
    uid = None
    def __init__(self, master, uid, verbose=True):
        self.conn = master
        if type(uid) == str:
            self.domain = uid
        elif type(uid) == int:
            self.uid = uid
        if verbose:
            self._obtain()

    def _obtain(self):
        if self.uid:
            raw = self.conn._req('users.get', {'user_ids': self.uid})[0]
        elif self.domain:
            raw = self.conn._req('users.get', {'user_ids': self.domain})[0]
        else: raise BaseException('WTF?')
        if raw:
            self.__dict__ = {**self.__dict__, **self.raw}
    @property
    def friends(self):


    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.last_name)
