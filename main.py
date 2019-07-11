import _requests as r
import configparser
import json

vklink = 'https://api.vk.com/method/'



# Создадим класс соединения для хранения нужных данных.
class Connection():
    def __init__(self, filename):
        buf = configparser.ConfigParser()
        buf.read(filename)
        self.token = buf['CONFIG']['api_token']

    def _req(self, method, data):
        if
        response = r.get(vklink + str(method),
                         params={**data, 'v':'5.0', 'access_token': self.token})
        response = response.json()
        if 'error' in response.keys():
            raise BaseException(response['error']['error_msg'])
        else:
            return response['response']

    def newuser(self, id):
        if type(id) == str:
            print('detected domain id')
            response = _req('users.get', {'user_ids': id})[0]
            return User(response['id'], data=response)

    # MAKE !!COUNTER MORE THAN OFFSET!!

class User(Connection):
    def __init__(self, id, lazy=False, data=None):
        self.id = id
        if not lazy:
            if data:
                self.fname = data['first_name']
                self.sname = data['last_name']
                self.closed = data['is_closed']

        else:
            self.fname = 'Not'
            self.closed = False
            self.sname = 'Obtained'
            self.friends = []

    def __repr__(self):
        return('User %i: %s %s' % (self.id, self.fname, self.sname))

class Group(Connection):
    def __init__(self, id, lazy=False):
        self.id = id
        self.name =
        self.members = []

    def __repr__(self):
        return('User %i: %s %s' % (self.id, self.fname, self.sname))
