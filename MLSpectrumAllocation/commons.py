# from MLSpectrumAllocation.Field import Field
import math
# from random import gauss
from collections import namedtuple
# from MLSpectrumAllocation.Sensor import *
# from typing import List
# import random as rd
# from MLSpectrumAllocation.PU import *
# from MLSpectrumAllocation.SU import SU
# from MLSpectrumAllocation.SPLAT import SPLAT

TRX = namedtuple('TRX', ('loc', 'pow', 'height'))
PropagationModel = namedtuple('PropagationModel', ('name', 'var'))


def get_decimal(value: float) -> float:  # dB to decimal
    return 10 ** (value / 10)


def get_db(value: float) -> float:
    if value <= 0.0:
        return -float('inf')
    return 10 * math.log10(value)

