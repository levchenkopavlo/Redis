import redis


class Record_Table:
    def __init__(self):
        self.server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.user = None

    def add_user(self, user, password):
        if self.server.hexists('users', user):
            print('user already registered')
        else:
            self.server.hset('users', user, password)
            print('user added')

    def login(self, user, password):
        real_password = self.server.hget('users', user)

        if real_password and password == real_password:
            print('login OK')
            self.current_user = user
        else:
            print('Wrong login or password')

    def show_users(self):
        users = self.server.hkeys(f'users')
        print(*users)

    def add_result(self, name, score):
        if self.current_user:
            self.server.hset('results', name, score)

    def show_results(self):
        table = self.server.hgetall('results')
        for name in table:
            print(f'{name}: {table[name]}')

    def del_result(self, name):
        if self.current_user:
            self.server.hdel('results', name)
            print('result deleted')

    def edit_result(self, name, name_new, score):
        if self.current_user:
            if name in self.server.hkeys('results'):
                self.del_result(name)
                self.add_result(name_new, score)

    def clear_results(self):
        if self.current_user:
            self.server.delete('results')
    def search_results(self, text):
        table = self.server.hgetall('results')
        for name in table:
            if text.lower() in name.lower():
                print(f'{name}: {table[name]}')
    def show_top_10(self):
        table = self.server.hgetall('results')
        sorted_table = dict(sorted(table.items(), key=lambda item: int(item[1])))
        for name in dict(list(sorted_table.items())[:10]):
            print(f'{name}: {table[name]}')

record_table = Record_Table()
while True:
    print('1. add user')
    print('2. login')
    print('3. show registered users')
    print('4. add results to table')
    print('5. show results')
    print('6. delete result from table')
    print('7. edit result')
    print('8. clear results in table')
    print('9. search results in table')
    print('0. top 10 results')

    command = input('enter command: ')
    if command == '1':
        user = input('user name: ')
        password = input('password: ')

        record_table.add_user(user, password)
    elif command == '2':
        user = input('user name: ')
        password = input('password: ')

        record_table.login(user, password)
    elif command == '3':
        record_table.show_users()
    elif command == '4':
        while True:
            name = input('input name: ')
            score = input('input score: ')
            if name and score:
                break
            else:
                print('values cannot be empty')
                continue
        record_table.add_result(name, score)
    elif command == '5':
        record_table.show_results()
    elif command == '6':
        name = input('input name: ')
        record_table.del_result(name)
    elif command == '7':
        name = input('input name: ')
        while True:
            name_new = input(f'input new name ({name}): ')
            if name_new == '':
                name_new = name
            score = input('input new score: ')
            if score:
                break
            else:
                print('score cannot be empty')
                continue
        record_table.edit_result(name, name_new, score)
    elif command == '8':
        record_table.clear_results()
    elif command == '9':
        search = input(f'input text for search: ')
        record_table.search_results(search)
    elif command == '0':
        record_table.show_top_10()