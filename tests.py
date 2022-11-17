from main import *
import random

store = Store((0, 0))

users = []
for i in range(5):
    x = random.randint(-100, 100)
    y = random.randint(-100, 100)
    new_user = User((x, y))
    users.append(new_user)

provider1 = Provider(0)
provider2 = Provider(1)

item1 = Item('Aibek', 0, 0, 100)
item2 = Item('Mark', 1, 1, 200)
item3 = Item('Vlad', 2, 2, 300)

order_1 = Order({0: [item1, 1], 1: [item2, 3]})

worker1 = Courier(0)
worker2 = Courier(1)
worker3 = Storekeeper(2)
print('-' * 40)

store.get_worker(worker1)
store.get_worker(worker2)
store.get_worker(worker3)
print('-' * 40)

provider1.make_item(item1, 20)
provider1.make_item(item2, 20)
print('-' * 40)

store.send_request(provider1, {0: [item1, 1], 1: [item2, 3]})
print('-' * 40)


print('провайдеры магазина', store.providers)
print('Курьеры маганиза', store.couriers)
print('Кладовщики магазина', store.storekeepers)
print('Заказы магазина', store.orders)
print()
print('Итемы у провайдера', provider1.items)
print('Итемы у магазина', store.items)
print('-' * 40)

users[0].make_order(store, order_1)
print('-' * 40)

print('-' * 40)

print('-' * 40)

print('-' * 40)


