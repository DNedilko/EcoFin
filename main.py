from datetime import date
from abc import ABC, abstractmethod, ABCMeta
import random


class IStationsPage(ABC):
    @abstractmethod
    def show_stations(self):
        pass

    @abstractmethod
    def set_station_as_favourite(self):
        pass

    @abstractmethod
    def set_station_as_default(self):
        pass


class Station(IStationsPage):

    def __init__(self, city='none', material='none', address='none', favourite=False, station_id=0):
        self.city = city
        self.material = material
        self.address = address
        self.favourite_station = favourite
        self.station_id = station_id

    def set_station_as_favourite(self):
        self.favourite_station = True

    def set_station_as_default(self):
        self.favourite_station = False

    def add_station(self):
        fh = open('stations.csv', 'a')
        station = [self.city, self.material, self.address, '_', str(self.station_id)]
        fh.write('\n')
        fh.write(','.join(station))
        fh.close()

    @staticmethod
    def show_stations():
        fh = open('stations.csv', 'r', encoding="utf-8")
        stations_data = fh.readlines()
        stations_list = []
        for string in stations_data:
            city, material, address, favourite_station, station_id = string.split(',')
            stations_list.append(Station(city, material, address, False, int(station_id)))
        return stations_list

    def __str__(self):
        return f'\nStation {self.station_id:03}   (material: {str(self.material)}, city: {str(self.city)}, ' \
               f'address: {str(self.address)} favourite: {bool(self.favourite_station)})'


class Garbage:
    def __init__(self, record_date, material='none', amount=0.0):
        self._record_date = record_date
        self._material = material
        self._amount = amount

        self._station = Station()

    @property
    def record_date(self):
        return self._record_date

    @property
    def material(self):
        return self._material

    @property
    def amount(self):
        return self._amount

    @property
    def station(self):
        return self._station

    @record_date.getter
    def record_date(self):
        return self._record_date

    @station.getter
    def station_id(self):
        return self._station

    @amount.getter
    def amount(self):
        return self._amount

    @material.setter
    def material(self, value):
        self._material = value

    @station.setter
    def station(self, new_station: Station):
        self._station = new_station

    @record_date.setter
    def record_date(self, value):
        self._record_date = value

    @amount.setter
    def amount(self, new_amount):
        if isinstance(new_amount, int):
            self._amount = new_amount
        else:
            raise ValueError('Please, enter amount number correctly')

    def __str__(self):
        return f'\nSorted   (station: {self._station.station_id}, material: {str(self._material)}, amount: {str(self._amount)}, ' \
               f'record date: {self._record_date})'


class IBuy(ABC):
    @abstractmethod
    def subtract_coins(self, coins_subtracted: int):
        pass


class IUserInfo(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def change_password(self, new_password):
        pass

    @abstractmethod
    def email(self):
        pass


class IRegistration(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def email(self):
        pass

    @abstractmethod
    def city(self):
        pass

    @abstractmethod
    def password(self):
        pass


class NotInRange(Exception):
    def __init__(self, var, frm, to):
        self.var = var
        self.frm = frm
        self.to = to
        super().__init__()

    def __str__(self):
        return f'The variable \'{self.var}\' can only take value from {self.frm} to {self.to}'


class InvalidLength(Exception):
    def __init__(self, var, frm):
        self.var = var
        self.frm = frm
        super().__init__()

    def __str__(self):
        return f'The \'{self.var}\' length can only be greater than {self.frm} characters'


class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, message: str) -> None:
        pass


class Observable(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.observers = []

    def register(self, observer: Observer) -> None:
        self.observers.append(observer)

    def notify_observers(self, message: str) -> None:
        for observer in self.observers:
            observer.update(message)


class NoticeBoard(Observable):
    def add_facts(self, facts: str) -> None:
        self.notify_observers(facts)


class Account(IBuy):
    sort_history = []

    def __init__(self, user_id, password='1111', coins=0, register=str(date.today())):
        self.__user_id = f'{user_id:06}'
        self.__password = password
        self._balance = coins
        self._registration_date = register

    @property
    def password(self):
        return self.__password

    @property
    def id(self):
        return self.__user_id

    @property
    def registration_date(self):
        return self._registration_date

    @property
    def balance(self):
        return self._balance

    @password.setter
    def password(self, pw):
        try:
            if not len(pw) > 7:
                raise InvalidLength('password', 7)
            else:
                self.__password = pw
        except InvalidLength as e:
            print(f'Error:\n     {e}')

    @password.getter
    def password(self):
        return self.__password

    @id.getter
    def id(self):
        return self.__user_id

    @registration_date.getter
    def registration_date(self):
        return self._registration_date

    @balance.getter
    def balance(self):
        return self._balance

    def add_coins(self, coins_added: int):
        self._balance = int(self._balance) + coins_added

    def subtract_coins(self, coins_subtracted: int):
        try:
            if (int(self._balance) - coins_subtracted) < 0:
                raise ValueError('     Not enough coins for the operation')
            else:
                self._balance = int(self._balance) - coins_subtracted
        except ValueError as e:
            print('Error:\n', e)

    def add_sorted(self, garbage: Garbage):
        self.sort_history.append(garbage)

    def __str__(self):
        return f'registration date: {self._registration_date}, password: {self.__password}, ' \
               f'id: {self.__user_id}, balance: {self._balance}'


class User(Observer, IUserInfo, IRegistration, ABC):
    __user_count = 0

    def __init__(self, name='none', city='none', email='none'):
        self._name = name
        self._city = city
        self._email = email

        User.__user_count += 1
        self.account = Account(self.__user_count)

    @property
    def name(self):
        return self._name

    @property
    def city(self):
        return self._city

    @property
    def email(self):
        return self._email

    @name.setter
    def name(self, new_name):
        try:
            if not isinstance(new_name, str):
                raise TypeError('    Wrong type of name')
            elif not len(new_name) >= 2:
                raise InvalidLength('name', 2)
            else:
                self._name = new_name
        except InvalidLength as e:
            print(e)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)

    @city.setter
    def city(self, new_city):
        if isinstance(new_city, str) and len(new_city) >= 2:
            self._city = new_city
        else:
            raise ValueError('Please, enter your city name correctly')

    @email.setter
    def email(self, new_email):
        if not isinstance(new_email, str):
            raise ValueError('Please, enter your email correctly')
        self._email = new_email

    @name.getter
    def name(self):
        return self._name

    @city.getter
    def city(self):
        return self._city

    @email.getter
    def email(self):
        return self._email

    def change_password(self, new_password):
        try:
            if not len(new_password) > 7:
                raise InvalidLength('password', 7)
            else:
                self.account._Account__password = new_password
        except InvalidLength as e:
            print(f'Error:\n     {e}')

    def password(self):
        print('Password IRegistration')

    def update(self, message: str) -> None:
        print(f'{self._name} received a new fact: {message}')

    def __str__(self):
        return f'\nUser {self.account.id}   (name: {str(self._name)}, city: {str(self._city)}, ' \
               f'email: {str(self._email)}) \nAccount info ({self.account})'


class ItemNotFound(Exception):
    def __init__(self, item, message="There is no such item"):
        self.item = item
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: \'{self.item}\''


class Item(ABC):
    items = [[]]

    def __init__(self, type_of_item='none', amount=0):
        self._type = type_of_item
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    @property
    def type(self):
        return self._type

    @amount.setter
    def amount(self, entered_amount):
        try:
            if not isinstance(float(entered_amount), float):
                raise ValueError
            elif not 0 < entered_amount < 50:
                raise NotInRange('amount', 0, 50)
            else:
                self._amount = entered_amount
        except NotInRange as e:
            print(f'Out of range:\n     {e}')
        except ValueError as e:
            print(f'Value Error:\n     {e}')

    @type.setter
    def type(self, entered_type):
        try:
            if entered_type in self.items:
                self._type = entered_type
            else:
                raise ItemNotFound(entered_type)
        except ItemNotFound as e:
            print(f'Error:\n    {e}')
        except TypeError as e:
            print(f'Type Error:\n    {e}')
        except Exception as e:
            print(f'Unknown Error:\n    {e}')

    @staticmethod
    def get_count_of_coins(user: Account):
        return user.balance

    def count_value(self):
        for i in range(len(self.items)):
            if self._type in self.items:
                return int(self.items[self._type] * self._amount)
            else:
                return 0

    def value_of_item(self):
        return self.count_value()


class Merch(Item):
    items = {
        "Shopper": 100,
        "Shirt": 150
    }


class Material(Item):
    items = {
        "Plastic": 10,
        "Glass": 15,
        "Metal": 20,
        "Paper": 10
    }


def random_line(file):
    lines = open(file).read().splitlines()
    one_line = random.choice(lines)
    return one_line


user_1 = User('katya', 'kyiv', '@dooole.com')
user_1.account.add_coins(500)
user_2 = User('lola')

board = NoticeBoard()
board.register(user_1)
board.register(user_2)
board.add_facts(random_line('facts.txt'))

merch = Merch()
merch.type = 'Shopper'
merch.amount = 2

# Add sorted garbage, show recycling history
g_1 = Garbage('2020-11-25', 'Glass', 0.5)
g_2 = Garbage('2020-12-14', 'plastic', 2)
st_1 = Station('lviv', 'glass', 'foo 3', False, 41)
g_1.station = st_1
user_1.account.add_sorted(g_1)
user_1.account.add_sorted(g_2)
print(user_1)
print(*user_1.account.sort_history)

user_1.account.subtract_coins(merch.value_of_item())

# Change password
user_1.change_password('56561111')
print(user_1)


# a = Station('Lviv', 'Plastic', 'Prospect 66', False)
# Station.add_station(a)
# print(a)
# a.set_station_as_favourite()
#
# print(a)
# print(*Station.show_stations())
