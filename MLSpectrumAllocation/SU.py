# from Commons.Point import Point
from Commons.elements import TX

class SU:    # secondary user
    def __init__(self, su_id: id, tx: TX):  # location: Point, height, power: float
        self.__id = "SU{0}".format(su_id)
        self.__tx = tx
        # self.__loc = location
        # self.__p = power
        # self.__height = height

    @property
    def id(self) -> str:
        return self.__id

    @property
    def tx(self) -> TX:
        return self.__tx

    @tx.setter
    def tx(self, tx: TX):
        self.__tx = tx

    # @property
    # def location(self) -> Point:
    #     return self.__loc
    #
    # @location.setter
    # def location(self, location: Point):
    #     self.__loc = location
    #
    # @property
    # def power(self) -> float:
    #     return self.__p
    #
    # @power.setter
    # def power(self, power: float):
    #     self.__p = power
    #
    # @property
    # def height(self) -> float:
    #     return self.__height
    #
    # @height.setter
    # def height(self, height: float):
    #     self.__height = height

    def __str__(self):
        return "{loc},{power}".format(loc=str(self.tx.element.location), power=round(self.tx.power, 3))


if __name__ == '__main__':
    pass

