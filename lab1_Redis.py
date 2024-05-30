import redis


class ShoppingCart:
    def __init__(self):
        self.server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.current_user = None

    def _get_user_item_key(self, item_id):
        # return f'cart:{self.current_user}:{item_id}'
        return f'{self.current_user}:{item_id}'

    def add_user(self, user, password):
        if self.server.hexists('users', user):
            print('User already exists')
            return

        self.server.hset('users', user, password)

    def login(self, user, password):
        real_password = self.server.hget('users', user)

        # print(f'{real_password=}')

        if real_password and password == real_password:
            print('login Ok')
            self.current_user = user

        else:
            print('Wrong login or password')

    def add_item(self, item_id, quantity=1):
        # key = f'{self.current_user}:{item_id}'
        #
        # if self.server.exists(key):
        #     print('Item is already in cart')
        #     return
        #
        # self.server.hset(key, mapping={'id': item_id, 'quantity': quantity})

        key = self._get_user_item_key(item_id)

        if self.server.exists(key):
            print('Item is already in cart')
            self.server.hincrby(key, 'quantity', quantity)
        else:
            self.server.hset(key, mapping={'id': item_id, 'quantity': quantity})

    def show_cart(self):
        # keys = self.server.key(f'{self.current_user}:*')

        pattern = self._get_user_item_key('*')
        keys = self.server.keys(pattern)

        if keys:
            print('Cart')
            for key in keys:
                data = self.server.hgetall(key)
                print(f'Item ID {data["id"]} -- {data["quantity"]} units')
        else:
            print('Cart is empty')

    def delete_item(self, item_id):
        key = self._get_user_item_key(item_id)

        if self.server.exists(key):
            self.server.delete(key)
            print("Item is deleted")
        else:
            print('There is not item in the cart')

    def clear_cart(self):
        pattern = self._get_user_item_key('*')
        keys = self.server.keys(pattern)

        if keys:
            for key in keys:
                self.server.delete(key)
            print('Cart is cleared')
        else:
            print('Cart is already empty')

    def search_item(self, item_id):
        key = self._get_user_item_key(item_id)

        data = self.server.hgetall(key)

        if data:
            print('Item info from cart')
            print(f'Item ID {data["id"]} -- {data["quantity"]} units')
        else:
            print('Item is not found')

    def update_item(self, item_id, new_quantity):
        key = self._get_user_item_key(item_id)

        if self.server.exists(key):
            self.server.hset(key, 'quantity', new_quantity)
            print('Item quantity is updated')
        else:
            print('There is not item in the cart')


shopping_cart = ShoppingCart()

while True:
    print('Choose option')
    print('1 add user')
    print('2 login')
    print('3 add item')
    print('4 show cart')
    print('5 delete item')
    print('6 clear cart')
    print('7 search item')
    print('8 update item')

    command = int(input('enter command: '))

    if command == 1:
        user = input('user name: ')
        password = input('password: ')

        shopping_cart.add_user(user, password)

    elif command == 2:
        user = input('user name: ')
        password = input('password: ')

        shopping_cart.login(user, password)

    elif command == 3:
        item_id = int(input('enter item id: '))
        quantity = int(input('enter item quantity: '))

        shopping_cart.add_item(item_id, quantity)

    elif command == 4:
        shopping_cart.show_cart()

    elif command == 5:
        item_id = int(input('enter item id: '))

        shopping_cart.delete_item(item_id)

    elif command == 6:
        shopping_cart.clear_cart()

    elif command == 7:
        item_id = int(input('enter item id: '))

        shopping_cart.search_item(item_id)

    elif command == 8:
        item_id = int(input('enter item id: '))
        quantity = int(input('enter item quantity: '))

        shopping_cart.update_item(item_id, quantity)