from dataclasses import dataclass
import time
from abc import ABC, abstractmethod
from enum import Enum

PREPARE_TIME = 0.75  # 45s
EXIT_TIME = 1  # 60s
GO_TIME = 0.5  # 30s


@dataclass
class Item:
    __name: str
    __id_in_provider_system: int
    __id_in_store_system: int
    __cost_price: int

    @property
    def provider_id(self):
        return self.__id_in_provider_system

    @provider_id.setter
    def provider_id(self, id_):
        if isinstance(id_, int):
            self.__id_in_provider_system = id_

    @property
    def store_id(self):
        return self.__id_in_store_system

    @store_id.setter
    def store_id(self, id_):
        if isinstance(id_, int):
            self.__id_in_store_system = id_

    @property
    def price(self):
        return self.price

    @price.setter
    def price(self, new_price):
        if isinstance(new_price, int):
            self.__cost_price = new_price


class Provider:
    def __init__(self, id_):
        self.__items = dict()
        self.__id = id_

    @property
    def items(self):
        return self.__items

    @property
    def get_id(self):
        return self.__id

    def make_item(self, item, count):
        print('провайдер делает итемы из воздуха')
        if item.provider_id in self.__items:
            self.__items[item.provider_id][2] += count
        else:
            self.__items[item.provider_id] = [item, count]

    def send_order(self, items_in_provider_system):
        print('Провайдер отправляет итемы в магазин')
        store_ids = {}
        for item_id_in_provider_system in items_in_provider_system:
            number = items_in_provider_system[item_id_in_provider_system]
            if self.__items[item_id_in_provider_system][1] >= number:
                self.__items[item_id_in_provider_system][1] -= number
                store_ids[self.__items[item_id_in_provider_system][0].store_id] = number
        return store_ids


class WorkerStatus(Enum):
    Relax = 0
    Free = 1
    Busy = 2


class Worker(ABC):

    def __init__(self):
        super().__init__()
        self._status = WorkerStatus.Relax
        self._shift_start = None
        self._shift_finish = None
        self._finish_time = None
        self._id = None
        self._store_id = None
        self._order = None

    @abstractmethod
    def get_order(self, order):
        pass

    @property
    def shift(self):
        return self._shift_start, self._shift_finishFree

    @shift.setter
    def shift(self, start_time, finish_time):
        if (isinstance(start_time, int) or isinstance(start_time, float)) and \
                (isinstance(finish_time, int) or isinstance(finish_time, float)):
            self._shift_finish = start_time
            self._finish_time = finish_time

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        if isinstance(new_status, WorkerStatus):
            self._status = new_status

    @property
    def get_id(self):
        return self._id

    @property
    def store(self):
        return self._store_id

    @store.setter
    def store(self, store_id):
        if isinstance(store_id, int):
            self._store_id = store_id

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, order_id):
        if isinstance(order_id, int):
            self._order = order_id

    @property
    def finish_time(self):
        return self._finish_time

    @finish_time.setter
    def finish_time(self, ft):
        if isinstance(ft, int) or isinstance(ft, float):
            self._finish_time = ft

    @property
    def shift_finish(self):
        return self._shift_finish

    @shift_finish.setter
    def shift_finish(self, sf):
        if isinstance(sf, int) or isinstance(sf, float):
            self._shift_finish = sf


class Courier(Worker):
    def __init__(self, id_):
        super().__init__()
        self._id = id_

    def get_order(self, order):
        print('Курьер принимает заказ')
        self.order = order

        # start_coords = order.store.coords
        # finish_coords = order.user.coords

        # forward_time = round(2 * EXIT_TIME + ((start_coords[0] - finish_coords[0]) ** 2 + (
        #         start_coords[1] - finish_coords[1]) ** 2) ** 0.5 * GO_TIME)
        # self.order.deliver_datetime = time.time() + forward_time
        # full_time = 2 * forward_time
        # self._finish_time = time.time() + full_time
        self.status = WorkerStatus.Busy

    def hand_over_order(self):
        print('Курьер передаёт заказ юзеру')
        self.order.status = DeliveryStatus.Delivered
        order = self.order
        self.order = None
        return order


class Storekeeper(Worker):
    def __init__(self, id_):
        super().__init__()
        self.id = id_
        self.order = None

    def get_order(self, order):
        print('Заказ начинает собираться кладовщиком')
        self.status = WorkerStatus.Busy
        order.status = DeliveryStatus.IsPreparing
        order.storekeeper_id = self.id
        self.order = order

    def finish_preparation(self):
        print('Заказ собран')
        self.order.status = DeliveryStatus.Ready
        self.status = WorkerStatus.Free
        self.order = None


class Store:
    def __init__(self, coords: tuple[float, float]):
        self.__items = dict()
        self.__providers = []
        self.__orders = []
        self.__couriers = []
        self.__storekeepers = []
        self.__coords = coords

    # def __get_new_provider(self, new_provider):
    #     print('Добавляем провайдера к магазину')
    #     if not isinstance(new_provider, Provider):
    #         return
    #     self.__providers[new_provider.get_id] = new_provider

    def __add_new_item(self, new_item, count):
        print('Добавляем итем к магазину')
        if not isinstance(new_item, Item) or not isinstance(count, int):
            return
        if new_item.store_id in self.__items:
            self.__items[new_item.store_id][1] += count
        else:
            self.__items[new_item.store_id] = [new_item, count]

    def send_request(self, provider, item_store_ids: dict[int, list[Item, int]]):
        if provider not in self.__providers:
            self.__providers.append(provider)
        print('Отправляем запрос поставщику')
        provider_ids = {}
        for item_id_in_store_system in item_store_ids:
            item, number = item_store_ids[item_id_in_store_system]
            if item_id_in_store_system not in self.__items:
                self.__items[item_id_in_store_system] = [item, 0]
            provider_ids[item.provider_id] = number
        available = provider.send_order(provider_ids)
        for item_store_id in available:
            number = available[item_store_id]
            self.__items[item_store_id][1] += number

    def update_stocks(self, items_in_store_system):
        print('Обновляем склад')
        for [item_id_in_store_system, number] in items_in_store_system:
            self.__items[item_id_in_store_system][1] += number

    def is_available(self, order):
        print('Идёт проверка на доступность заказа')
        for item_id in order.items:
            number = order.items[item_id][1]
            if item_id not in self.__items or self.__items[item_id][1] < number:
                print('Заказ не доступен')
                return False
        print('Заказ доступен')
        return True

    def take_order(self, order):
        print('Магазин принимает заказ от юзера')
        if self.is_available(order):
            order.status = DeliveryStatus.Created
            order.store = self
            order.creation_datetime = time.time()
            order.full_delivery_time = 2 * round(
                2 * EXIT_TIME + ((order.store.coords[0] - order.user.coords[0]) ** 2 + (
                        order.store.coords[1] - order.user.coords[1]) ** 2) ** 0.5 * GO_TIME)
            order.preparation_time = len(order.items) * PREPARE_TIME
            self.set_storekeeper(order)
            self.set_courier(order)
            self.__orders.append(order)
        else:
            order.status = DeliveryStatus.Rejected
            order.store = self
            order.creation_datetime = time.time()
            self.__orders.append(order)

    def get_waiting_courier(self, order):
        print('Ищем свободного курьера')
        for i in range(len(self.__couriers)):
            if self.__couriers[i].status == WorkerStatus.Free or (
                    self.__couriers[i].status == WorkerStatus.Busy and self.__couriers[i].finish_time < time.time()):
                if order.delivery_time + time.time() <= self.__couriers[i].shift_finish:
                    return i

    def set_courier(self, order):
        print('Для заказа устанавливается курьер')
        available_courier_number = self.get_waiting_courier(order)
        if available_courier_number is None:
            print('Свободный курьер не найден')
            return False
        print('Для заказа установлен курьер')
        self.__couriers[available_courier_number].get_order(order)
        return True

    def get_waiting_storekeeper(self, order):
        print('Ищем свободного кладовщика')
        for i in range(len(self.__storekeepers)):
            if self.__storekeepers[i].status == WorkerStatus.Free or (
                    self.__storekeepers[i].status == WorkerStatus.Busy
                    and self.__storekeepers[i].finish_time < time.time()):
                if order.preparation_time + time.time() <= self.__storekeepers[i].shift_finish:
                    return i

    def set_storekeeper(self, order):
        print('Для заказа устанавливается кладовщик')
        available_storekeeper_number = self.get_waiting_storekeeper(order)
        if available_storekeeper_number is None:
            print('Свободный кладовщик не найден')
            return False
        self.__couriers[available_storekeeper_number].get_order(order)
        print('Заказу установлен кладовщик')
        return True

    def get_worker(self, worker):
        if isinstance(worker, Courier):
            print('На работу принимается новый курьер')
            self.__couriers.append(worker)
        elif isinstance(worker, Storekeeper):
            print('На работу принимается новый кладовщик')
            self.__storekeepers.append(worker)
        else:
            print('На работу принималась обезьяна')

    @property
    def items(self):
        return self.__items

    @property
    def couriers(self):
        return self.__couriers

    @property
    def storekeepers(self):
        return self.__storekeepers

    @property
    def orders(self):
        return self.__orders

    @property
    def providers(self):
        return self.__providers

    @property
    def coords(self):
        return self.__coords


class DeliveryStatus(Enum):
    Created = 0
    IsPreparing = 1
    Ready = 2
    WithCourier = 3
    Delivered = 4
    Canceled = 5
    Rejected = 6


@dataclass
class Order:
    __status = None
    __items: dict[int:list[Item, int]]
    __creation_datetime = None
    __deliver_datetime = None
    __full_delivery_time = None
    __preparation_time = None
    __storekeeper_id = None
    __courier_id = None
    __store = None
    __user = None

    @property
    def creation_datetime(self):
        return self.__creation_datetime

    @creation_datetime.setter
    def creation_datetime(self, t):
        if isinstance(t, int) or isinstance(t, float):
            self.__creation_datetime = t

    @property
    def full_delivery_time(self):
        return self.__full_delivery_time

    @full_delivery_time.setter
    def full_delivery_time(self, t):
        if isinstance(t, int) or isinstance(t, float):
            self.__full_delivery_time = t

    @property
    def preparation_time(self):
        return self.__preparation_time

    @preparation_time.setter
    def preparation_time(self, t):
        if isinstance(t, float) or isinstance(t, int):
            self.__preparation_time = t

    @property
    def items(self):
        return self.__items

    @property
    def deliver_datetime(self):
        return self.__deliver_datetime

    @deliver_datetime.setter
    def deliver_datetime(self, t: int):
        if isinstance(t, float) or isinstance(t, int):
            self.__deliver_datetime = t

    @property
    def storekeeper_id(self):
        return self.__storekeeper_id

    @storekeeper_id.setter
    def storekeeper_id(self, storekeeper_id_):
        if isinstance(storekeeper_id_, int):
            self.__storekeeper_id = storekeeper_id_

    @property
    def courier_id(self):
        return self.__courier_id

    @courier_id.setter
    def courier_id(self, courier_id_):
        if isinstance(courier_id_, int):
            self.__courier_id = courier_id_

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, new_status):
        if isinstance(new_status, DeliveryStatus):
            self.__status = new_status

    @property
    def store(self):
        return self.__store

    @store.setter
    def store(self, store_):
        if isinstance(store_, Store):
            self.__store = store_

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user_):
        if isinstance(user_, User):
            self.__user = user_


class User:
    __slots__ = ('__coords', '__orders')

    def __init__(self, coords):
        self.__coords = coords

    def make_order(self, store, order):
        print('Создаётся заказ от юзера')
        order.user = self
        order.store = store
        store.take_order(order)

    def take_order(self, courier):
        print('Юзер забирает заказ у курьера')
        self.__orders.append(courier.hand_over_order())

    @property
    def coords(self):
        return self.__coords

    @coords.setter
    def coords(self, new_coords):
        if isinstance(new_coords, list) and len(new_coords) == 2 and isinstance(new_coords[0], int) and \
                isinstance(new_coords[1], int) and abs(new_coords[0]) <= 100 and abs(new_coords[1]) <= 100:
            self.__coords = new_coords
