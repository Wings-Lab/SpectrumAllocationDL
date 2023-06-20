from Commons.Point import Point, PolarPoint, CartesianPoint
from Commons.elements import TX, Element, RX
from typing import List
import math
from random import uniform
from MLSpectrumAllocation.PUR import PUR


class PU:
    def __init__(self, pu_id: int, tx: TX,
                 purs: List[PUR]=None, pur_num: int=None, pur_threshold: float=None, pur_beta: float=None,
                 pur_dist=None, pur_height: float= None):
        """PU class where a list of PURs or number of PUR is given. When both are given, list would be taken."""
        if not purs and not (pur_num and (pur_threshold or pur_beta) and pur_dist and pur_height):
            raise ValueError("One of purs or (pur_num and pur_threshold and pur_beta and pur_dist and pur_height) set "
                             "should be given")
        self.__id = "PU{0}".format(pu_id)
        self.__ON = False  # indicates if this PU exists or not(usable for different samples)
        # self.__loc = location
        # self.__height = height
        # self.__p = power
        self.__tx = tx
        if purs:
            self.__purs = purs
        else:
            if len(pur_dist) == 2:
                pur_min_dist, pur_max_dist = pur_dist[0], pur_dist[1]
            else:
                pur_min_dist = pur_max_dist = pur_dist
            self.__purs = self.create_purs(pu_id=self.id, pur_number=pur_num, pur_min_dist=pur_min_dist,
                                           pur_max_dist=pur_max_dist, pur_threshold=pur_threshold,
                                           pur_beta=pur_beta, pur_height=pur_height)

    def reset_purs(self):
        """reset all the power received to PURS"""
        for pur in self.purs:
            pur.reset()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def ON(self) -> bool:
        return self.__ON

    @ON.setter
    def ON(self, ON: bool):
        self.__ON = ON

    @property
    def purs(self) -> List[PUR]:
        return self.__purs

    # @property
    # def location(self) -> Point:
    #     return self.__loc
    #
    # @location.setter
    # def location(self, location: Point):
    #     self.__loc = location
    #
    # @property
    # def height(self) -> float:
    #     return self.__height
    #
    # @height.setter
    # def height(self, height: float):
    #     self.__height = height
    #
    # @property
    # def power(self) -> float:
    #     return self.__p
    #
    # @power.setter
    # def power(self, p: float):
    #     self.__p = p

    @property
    def tx(self) -> TX:
        return self.__tx

    @tx.setter
    def tx(self, tx: TX):
        self.__tx = tx

    @staticmethod
    def create_purs(pu_id: str, pur_number: int, pur_min_dist: float, pur_max_dist: float, pur_threshold: float,
                    pur_beta: float, pur_height: float) -> List[PUR]:
        purs = []
        angle = float(360/pur_number)
        for i in range(pur_number):
            purs.append(PUR(pu_id=pu_id, pur_id=i,
                            rx=RX(element=Element(location=Point(PolarPoint(uniform(pur_min_dist, pur_max_dist),
                                                                            i * math.radians(angle))),
                                                  height=pur_height)),
                            threshold=pur_threshold, beta=pur_beta))
        return purs

    def __str__(self):
        return "{loc},{power}".format(loc=str(self.tx.element.location), power=round(self.tx.power, 3))


if __name__ == "__main__":
<<<<<<< HEAD
    pu1 = PU(Point(5,5), 10, 13, 2, 10)
    for i in range(pu1.n):
        print(str(i+1), "(", pu1.purs[i].loc.get_cartesian[0], ",", pu1.purs[i].loc.get_cartesian[1],")", pu1.loc.distance(pu1.purs[i].loc))
=======
    pu1 = PU(pu_id=10, tx=TX(element=Element(location=Point(CartesianPoint(5, 5)), height=15), power=-5),
             pur_num=16, pur_beta=1.0, pur_dist=[1, 3], pur_height=15)
    print(pu1)
    for idx, pur in enumerate(pu1.purs):
        pur_location = pu1.tx.element.location + pur.rx.element.location
        print("{0}. ({1}), {2}".format(idx+1, str(pur_location), pu1.tx.element.location.distance(pur_location)))
>>>>>>> 2f6fbc9e82c377be81183e276e9e45d79365b964
