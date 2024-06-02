import redis


class Record_Table:
    def __init__(self):
        self.server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.user = None

    def add_user(self, user, password):
        if self.server.hexists('users', user):
            print('user already registered')
        else:
            self.server.hset('user', user, password)

    def login(self, user, password):
        real_password = self.server.hget('user', user)

        if real_password and password == real_password:
            print('login OK')
            self.current_user = user
        else:
            print('Wrong login or password')


record_table = Record_Table()
while True:
    print('1. add user')
    print('2. login')

    command = int(input('enter command: '))
    if command == 1:
        pass
    elif command == 2:
        pass
