import redis
from _datetime import datetime


class SocialNetwork:
    def __init__(self):
        self.server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.user = None
        self.current_user = None

    def add_user(self, user, password, mail, full_name):
        if self.server.hexists(f'users:{user}', user):
            print('user already registered')
        else:
            self.server.hset(f'users:{user}', mapping={user: password, 'mail': mail, 'full_name': full_name})

            print('user added')

    def edit_user(self, password, mail, full_name):
        if self.current_user:
            self.server.hset(f'users:{self.current_user}',
                             mapping={self.current_user: password, 'mail': mail, 'full_name': full_name})

    def del_user(self):
        if self.current_user:
            self.server.delete(f'users:{self.current_user}')
            if not self.server.exists(f'users:{self.current_user}', self.current_user):
                print('account deleted')

    def login(self, user, password):
        real_password = self.server.hget(f'users:{user}', user)

        if real_password and password == real_password:
            print('login OK')
            self.current_user = user
        else:
            print('Wrong login or password')

    def show_user_info(self, name):
        if self.server.exists(f'users:{name}', name):
            user_info = self.server.hgetall(f'users:{name}')
            print(f'user_id: {name}')
            print(f'e-mail: ', user_info['mail'])
            print(f'full name: ', user_info['full_name'])

    def search_users(self, text):
        cursor = '0'
        all_users = []

        while cursor != 0:
            cursor, keys = social_network.server.scan(cursor=cursor, match='users:*', _type='hash')
            all_users.extend(keys)

        print(f'{all_users = }')
        for user in all_users:
            if text.lower() in (social_network.server.hget(user, "full_name")).lower():
                print(f'user id: {user[6:]}; full name: {social_network.server.hget(user, "full_name")}')

    def add_publication(self, text):
        if self.current_user:
            self.server.hset(f'posts:{self.current_user}', datetime.timestamp(datetime.now()), text)
        else:
            print('please login first')

    def show_publications(self, name):
        if self.server.exists(f'posts:{name}'):
            posts = self.server.hgetall(f'posts:{name}')
            for time, post in posts.items():
                print('-----------------------------------')
                print(datetime.fromtimestamp(float(time)))
                print(post)
            print('-----------------------------------')
    def add_friend(self, name):
        if self.current_user:
            if self.server.exists(f'users:{name}'):
                print('---adding')
                self.server.lpush(f'friends:{self.current_user}', name)
                self.server.lpush(f'friends:{name}', self.current_user)
                print('friend added')
            else:
                print('id not found')
        else:
            print('please login first')
    def show_friends(self):
        if self.current_user:
            if self.server.exists(f'friends:{self.current_user}'):
                friends = self.server.lrange(f'friends:{self.current_user}', 0, -1)
                print('your friends:')
                for friend in friends:
                    print('-----------------------')
                    social_network.show_user_info(friend)
                print('-----------------------')
        else:
            print('please login first')

social_network = SocialNetwork()
while True:
    print('1. register new user')
    print('2. login')
    print('3. search users')
    print('4. delete account')
    print('5. edit account')
    print('6. user info')
    print('7. add friend')
    print('8. show friends')
    print('9. new publication')
    print('0. show publications')

    command = input('enter command: ')
    if command == '1':
        user = input('user name: ')
        password = input('password: ')
        mail = input('e-mail: ')
        full_name = input('full name: ')
        social_network.add_user(user, password, mail, full_name)

    elif command == '2':
        user = input('user name: ')
        password = input('password: ')

        social_network.login(user, password)
    elif command == '3':
        text = input('input text for search user by name: ')
        social_network.search_users('cv')
    elif command == '4':
        confirm = input('input "Y" for delete account: ')
        if confirm.lower() == 'y':
            social_network.del_user()
    elif command == '5':
        password = input('new password: ')
        mail = input('new e-mail: ')
        full_name = input('full name: ')
        social_network.edit_user(password, mail, full_name)
    elif command == '6':
        name = input('input user login: ')
        social_network.show_user_info(name)
    elif command == '7':
        name = input('input friend id: ')
        social_network.add_friend(name)
    elif command == '8':
        social_network.show_friends()
    elif command == '9':
        text = input('input new publication: ')
        social_network.add_publication(text)
    elif command == '0':
        name = input('input user login: ')
        social_network.show_publications(name)
