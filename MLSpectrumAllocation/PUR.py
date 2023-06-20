from Commons.Point import Point, PolarPoint
from Commons.elements import RX, Element
import warnings
from MLSpectrumAllocation.commons import get_db, get_decimal


class PUR:

    def __init__(self, pu_id: str, pur_id: int, rx: RX, threshold: float=None, beta: float=None):
        if threshold is None and beta is None:
            raise ValueError("Both threshold and beta cannot be None.")
        elif threshold is not None and beta is not None:
            raise ValueError("One of threshold and beta should be given.")
        elif threshold is None and beta == 0.0:
            raise ValueError("Beta cannot be zero.")
        self.__id = "{pu_id}_PUR{pur_id}".format(pu_id=pu_id, pur_id=pur_id)
        # self.__loc = PolarPoint(location.r, location.theta)  # relative distance defined by r and theta
        # self.__height = height  # height of PUR
        self.__rx = rx
        self.__thr = threshold  # threshold(dB)  (irp < threshold)
        self.__beta = beta  # beta (rp/irp > beta)
        # self.__rp = -float('inf')  # power(dB) received from its own pu
        self.__irp = -float('inf')  # total power(dB) received from other pus and sus ipr=total(val in irp_map)
        self.__irp_map = {}  # a maps to store key/val whey key is id of other PUs and SUs and val is their power(dB)

    @property
    def id(self):
        return self.__id

    def reset(self):
        """reset all received powers"""
        self.__irp = -float('inf')
        self.__irp_map = {}
        self.rx.received_power = -float('inf')

    # @property
    # def location(self) -> PolarPoint:
    #     """Return relative location to its PU."""
    #     return PolarPoint(self.__loc.r, self.__loc.theta)
    #
    # @location.setter
    # def location(self, location: PolarPoint):
    #     """Set its relative location to a new one."""
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
    # def received_power(self) -> float:
    #     """Return the power(dB) it receives from its PU."""
    #     return self.__rp
    #
    # @received_power.setter
    # def received_power(self, power: float):
    #     self.__rp = power

    @property
    def rx(self) -> RX:
        return self.__rx

    @rx.setter
    def rx(self, rx: RX):
        self.__rx = rx

    @property
    def threshold(self) -> float:
        return self.__thr

    @threshold.setter
    def threshold(self, threshold: float):
        self.__thr = threshold

    @property
    def beta(self) -> float:
        return self.__beta

    @beta.setter
    def beta(self, beta: float):
        self.__beta = beta

    @property
    def interference_received_power(self) -> float:
        """Return the total power(dB) it receives from other elements(PUs, SUs)."""
        return self.__irp

    def get_interference_power_from(self, key):
        """Return power(dB) received from key to PUR. If it doesn't exist, -inf would be returned"""
        if key in self.__irp_map:
            return self.__irp_map[key]
        return -float('inf')

    def add_interference(self, key: str, value: float):
        """Add power(dB) of a new element to PUR.
        If it exists, it raise a warning."""
        if key in self.__irp_map:
            warnings.warn("Power for {0} element already exists in {1}.".format(key, self.__id) +
                          " Use update_interference() if you need to update power for an element.")
            return
        self.__irp_map[key] = value
        self.__irp = get_db(get_decimal(self.__irp) + get_decimal(value))

    def update_interference(self, key: str, value: float):
        """Update power(dB) for key to PUR.
        If it does not exist, it raise a warning."""
        if key not in self.__irp_map:
            warnings.warn("Power for {0} element does not exist in {1}.".format(key, self.__id) +
                          " Use add_interference() if you need to add power for an element.")
            return
        old_power = self.__irp_map[key]
        self.__irp_map[key] = value
        self.__irp = get_db(get_decimal(self.__irp) +
                            get_decimal(value) -
                            get_decimal(old_power))

    def delete_interference_power_from(self, key):
        if key in self.__irp_map:
            value = self.__irp_map.pop(key)
            self.__irp = get_db(get_decimal(self.__irp) - get_decimal(value))

    def get_interference_capacity(self) -> float:
        """Return the maximum extra interference(dB) that PUR can stands, using threshold."""
        irp_decimal = get_decimal(self.__irp)
        if self.beta is not None:  # using beta
            rp_decimal = get_decimal(self.rx.received_power)
            return get_db(rp_decimal / self.__beta - irp_decimal)
        else:  # using threshold
            thr_decimal = get_decimal(self.threshold)
            return get_db(thr_decimal - irp_decimal)

    def __str__(self):
        r, theta = self.rx.element.location.polar.r, self.rx.element.location.polar.theta
        return "id= {pur_id}\n".format(pur_id=self.__id) + \
               "relative location= ({r},{theta})\n".format(r=round(r, 3), theta=round(theta, 3)) +\
               "height= {height}\n".format(height=self.rx.element.height) +\
               "threshold= {thr}\n".format(thr=self.__thr) +\
               "beta= {beta}\n".format(beta=self.__beta) +\
               "received power= {rp}\n".format(rp=self.rx.received_power) +\
               "received interference= {irp}".format(irp=self.__irp)


if __name__ == "__main__":
    pur = PUR('PU10', 1, RX(Element(location=Point(PolarPoint(5, 0)), height=15)), beta=1)
    print(pur)
    pur.received_power = -25
    pur.add_interference('PU110', -30)
    print(pur)
    pur.add_interference('PU110', -35)
    pur.update_interference('PU110', -35)
    print(pur)
    pur.update_interference('PU10', -30)
    pur.add_interference('PU10', -30)
    pur.delete_interference_power_from('PU110')
    print(pur)
