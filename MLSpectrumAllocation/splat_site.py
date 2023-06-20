from random import randint


class Site:
    """
    A splat site that have location(lat, lon) amd height
    """
    def __init__(self, tp, lat: float, lon: float, height: float, name: str=None):
        self.__name = '{}-N{}W{}-{}'.format(tp, abs(int(lat*1000)), abs(int(lon*1000)), randint(0, 10**5)) \
            if not name else name
        # self.type = tp # 'tx' or 'rx'
        self.__lat = lat  # latitude  is the Y axis
        self.__lon = lon  # longitude is the X axis
        self.__height = height

    @property
    def name(self) -> str:
        return self.__name

    @property
    def lat(self) -> float:
        return self.__lat

    @property
    def lon(self) -> float:
        return self.__lon

    @property
    def height(self):
        return self.__height

    def __str__(self):
        return '{}\n{}\n{}\n{}m\n'.format(self.name, abs(self.lat), abs(self.lon), self.height)


if __name__ == "__main__":
    s = Site('tx', 48.68, -65.25, 30)
    print(s)

    s = Site('rx', 48.68, -65.25, 30)
    print(s)