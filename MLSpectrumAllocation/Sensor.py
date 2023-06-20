import sys
sys.path.append('../')
from Commons.Point import Point
from Commons.elements import RX, Element


class Sensor:
    def __init__(self, ss_id: int, rx: RX, cost: float, std: float):
        self.__id = "SS{0}".format(ss_id)
        self.__rx = rx
        # self.__loc = loc
        # self.__rp = -float('inf')
        self.__cost = cost
        self.__std = std

    def reset(self):
        self.rx.received_power = -float('inf')

    @property
    def id(self) -> str:
        return self.__id

    @property
    def rx(self) -> RX:
        return self.__rx

    @rx.setter
    def rx(self, rx: RX):
        self.__rx = rx

    @property
    def cost(self):
        return self.__cost

    @cost.setter
    def cost(self, cost: float):
        self.__cost = cost

    @property
    def std(self):
        return self.__std

    @std.setter
    def std(self, std: float):
        self.__std = std

    def __str__(self):
        return "id= {0}\n".format(self.id) + \
               "{0}\n".format(self.rx) + \
               "cost= {0}\n".format(self.cost) + \
               "std= {0}\n".format(self.std)


if __name__ == "__main__":
    ss = Sensor(ss_id=15, rx=RX(Element(location=Point((1, 5)), height=15)), cost=15, std=1)
    print(ss)
