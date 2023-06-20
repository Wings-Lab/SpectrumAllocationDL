# from typing import List
from MLSpectrumAllocation.PU import PU
from MLSpectrumAllocation.SU import SU
from Commons.Point import Point
from MLSpectrumAllocation.Sensor import Sensor
from Commons.elements import TX, RX, Element
from typing import List
from MLSpectrumAllocation.propgation_model import PropagationModel, LogDistancePM
from Commons.shapes import Shape
from MLSpectrumAllocation.commons import get_decimal, get_db
from collections import namedtuple
from random import sample
# import multiprocessing
# import sys
# import random as rd

# INTERPOLATION
InterSMParam = namedtuple('InterSMParam', ('pu_size', 'ss_size', 'selection_algo', 'gamma'))


class Field:
    def __init__(self, pus: List[PU], sus: List[SU], sss: List[Sensor], propagation_model: PropagationModel,
                 shape: Shape, cell_size: int=1):
        # corners: List[Point], propagation_model: str, alpha: float, noise: bool=False,
        # std: float = -float('inf'), splat_upper_left=None,
        self.__pus = pus  # Primary Users
        self.__sus = sus  # Secondary Users
        # self.corners = corners
        self.__propagation_model = propagation_model
        self.__cell_size = cell_size
        self.__sss = sss  # Spectrum Sensors
        self.__shape = shape
        # self.alpha = alpha
        # if propagation_model.lower() == 'log':
        #     self.propagation_model = PropagationModel('log', [alpha])
        # elif propagation_model.lower() == 'splat':
        #     self.propagation_model = PropagationModel('splat', [splat_upper_left])

        # self.noise = noise

        # self.std = std

        # self.compute_purs_powers()
        # self.compute_sss_received_power() if ss else None

    @property
    def pus(self) -> List[PU]:
        return self.__pus

    @property
    def sss(self) -> List[Sensor]:
        return self.__sss

    @property
    def field_shape(self) -> Shape:
        return self.__shape

    @property
    def propagation_model(self) -> PropagationModel:
        return self.__propagation_model

    @property
    def cell_size(self) -> int:
        return self.__cell_size

    @property
    def sus(self) -> List[SU]:
        return self.__sus

    @sus.setter
    def sus(self, sus: List[SU]):
        self.__sus = sus

    def compute_field_power(self) -> List[List[float]]:  # calculate received power at specific locations all over the
                                                            # field to create a heatmap
        # TODO fix this part before using
        received_power = []

        [min_x, min_y] = [0, 0]  # self.corners[0].get_cartesian
        [max_x, max_y] = [1, 2]  # self.corners[-1].get_cartesian
        for y in range(min_y, max_y, min(1, max(1, (max_y - min_y) // 400))):
            tmp = []
            for x in range(min_x, max_x, min(1, max(1, (max_x - min_x) // 400))):
                pwr_tmp = -float('inf')
                for pu in self.pus:
                    pwr_tmp = self.power_with_path_loss(tx=pu.tx, rx=RX(Element(Point((x, y)), 15)))
                tmp.append(pwr_tmp)
            received_power.append(tmp)
        return received_power

    def compute_purs_powers(self):  # calculate received powers at PURs
        tmp_pus = [tmp_pu for tmp_pu in self.pus if tmp_pu.ON]
        for pu in tmp_pus:
            pu.reset_purs()
            for pur in pu.purs:
                pur_element = RX(Element(pu.tx.element.location + pur.rx.element.location, pur.rx.element.height))
                # pur location is relational and it should be updated first
                pur.rx.received_power = self.power_with_path_loss(tx=pu.tx, rx=pur_element)
                for npu in tmp_pus:  # power received from other PUs
                    if pu != npu:
                        npu_pur_loss = self.propagation_model.path_loss(tx=npu.tx.element * self.cell_size,
                                                                        rx=pur_element.element * self.cell_size)
                        pur.add_interference(npu.id, npu.tx.power - npu_pur_loss)

        # compute max power power for SUs except the last one, O(#su * #pus * #sus)
        for i in range(len(self.sus) - 1):
            # get max_power for su
            su = self.sus[i]
            su.tx.power = self.calculate_max_power(su)
            if su.tx.power == -float('inf'):
                continue
            # update irp for purs
            for pu in tmp_pus:
                for pur in pu.purs:
                    pur_element = RX(Element(pu.tx.element.location + pur.rx.element.location, pur.rx.element.height))
                    su_pur_loss = self.propagation_model.path_loss(tx=su.tx.element * self.cell_size,
                                                                   rx=pur_element.element * self.cell_size)
                    pur.add_interference(su.id, su.tx.power - su_pur_loss)

    def compute_sss_received_power(self):  # compute received power at sensors from PUs and SUs
        for sensor in self.sss:
            sensor.rx.received_power = -float('inf')
            for pu in [tmp_pu for tmp_pu in self.pus if tmp_pu.ON]:  # calculate power of PUs
                sensor.rx.received_power = self.power_with_path_loss(tx=pu.tx, rx=sensor.rx)

            # calculate power of sus(except the last one)
            for i in range(len(self.sus) - 1):
                su = self.sus[i]
                sensor.rx.received_power = self.power_with_path_loss(tx=su.tx, rx=sensor.rx)

    def su_request_accept(self) -> bool:
        # sign: bool=True sign here is temporary and just for create an unreal situation in which learning would fail
        # option = 0  # 0 means using BETA, 1 means using threshold
        su = self.sus[-1]
        for pu in [tmp_pu for tmp_pu in self.pus if tmp_pu.ON]:
            for pur in pu.purs:
                if pur.get_interference_capacity() == -float('inf'):
                    continue
                    # TODO reconsider this case(False should be returned). No interference should be allowed
                pur_element = RX(Element(pu.tx.element.location + pur.rx.element.location, pur.rx.element.height))
                su_pur_loss = self.propagation_model.path_loss(tx=su.tx.element * self.cell_size,
                                                               rx=pur_element.element * self.cell_size)
                pur.add_interference(su.id, su.tx.power - su_pur_loss)
                if pur.get_interference_capacity() == -float('inf'):
                    pur.delete_interference_power_from(su.id)
                    return False
                pur.delete_interference_power_from(su.id)
        return True

    def power_with_path_loss(self, tx: TX, rx: RX):  # False for sign means negative otherwise positive
        """Return received power after applying tx power. rx_power = tx_power + rx_power"""
        tx_power = tx.power
        if tx_power == -float('inf'):
            return rx.received_power
        loss = self.propagation_model.path_loss(tx.element * self.cell_size, rx.element * self.cell_size)
        return get_db(get_decimal(rx.received_power) + get_decimal(tx_power - loss))

    def calculate_max_power(self, su: SU) -> float:
        """Calculate the maximum power(dB) SU can send."""
        pus = [tmp_pu for tmp_pu in self.pus if tmp_pu.ON]
        max_pow = float('inf')  # find the minimum possible without bringing any interference
        for pu in pus:
            for pur in pu.purs:
                pur_element = RX(Element(pu.tx.element.location + pur.rx.element.location, pur.rx.element.height))
                # pur location is relational and it should be updated first
                su_power_at_pur = pur.get_interference_capacity()
                loss = self.propagation_model.path_loss(tx=su.tx.element * self.cell_size,
                                                        rx=pur_element.element * self.cell_size)
                su_power_at_su = su_power_at_pur + loss
                max_pow = min(max_pow, su_power_at_su)
        return max_pow

    # compute power SU can send based on conservative model: if existing power at su location is higher than
    # noise floor, it cannot send otherwise it can send a power based on propagation model and minimum power
    #  a PU can have
    def conservative_model_power(self, min_power: float,  noise_floor=-90):
        send_power = float('inf')
        su = self.sus[-1]  # TODO this code has written for only one SU. Fix for multiple before using it
        # upper bound should be calculated based on purs not pus. Assume there is minimum power at a PU;
        # should calculate min(pur_pow/beta)
        pus = [pu for pu in self.pus if pu.ON]
        for pu in pus:
            for pur in pu.purs:
                pur_element = RX(Element(pu.tx.element.location + pur.rx.element.location, pur.rx.element.height))
                pow_tmp = self.power_with_path_loss(tx=TX(pu.tx.element, min_power), rx=pur_element)
                send_power = min(send_power, pow_tmp/pur.beta)
        for pu in pus:
            su_rx = RX(su.tx.element)
            power_at_su_from_pus = self.power_with_path_loss(tx=pu.tx, rx=su_rx)
            if power_at_su_from_pus > noise_floor:
                return noise_floor  # there is already a signal, su cannot send anything.
        return send_power  # all powers from pus is still less than threshold, su can send power

    # INTERPOLATION
    @staticmethod
    def num_select(select_size, elements_size):
        if select_size == 0 or select_size > elements_size:
            return elements_size
        return select_size

    def interpolation_max_power(self, inter_sm_param: InterSMParam):
        k_pu = self.num_select(inter_sm_param.pu_size, len(self.pus))
        k_ss = self.num_select(inter_sm_param.ss_size, len(self.sss))
        su = self.sus[-1]  # TODO this code has written for only one SU. Fix for multiple before using it
        if type(self.propagation_model) == LogDistancePM:  # TODO only written for LogNormal Propagation Model
            pl_alpha = self.propagation_model.alpha
        else:
            raise ValueError("Only Log-Distance has been implemented")

        pu_inds, sss_inds, sss_dists = [], [], []
        if not inter_sm_param.selection_algo:
            pu_inds = list(range(k_pu))
            sss_inds = list(range(k_ss))
            sss_dists = [self.cell_size * su.tx.element.location.distance(self.sss[i].rx.element.location)
                         for i in range(k_ss)]
        elif inter_sm_param.selection_algo.lower() == 'sort':
            pu_dists = []
            for i, pu in enumerate(self.pus):
                dist, ind = self.cell_size * su.tx.element.location.distance(pu.tx.element.location), i
                if i < k_pu:
                    pu_inds.append(i)
                    pu_dists.append(dist)
                else:
                    for j in range(len(pu_inds)):
                        if dist < pu_dists[j]:
                            pu_dists[j], dist = dist, pu_dists[j]
                            ind, pu_inds[j] = pu_inds[j], ind

            for i, ss in enumerate(self.sss):
                dist, ind = self.cell_size * su.tx.element.location.distance(ss.rx.element.location), i
                if i < k_ss:
                    sss_inds.append(i)
                    sss_dists.append(dist)
                else:
                    for j in range(len(sss_inds)):
                        if dist < sss_dists[j]:
                            sss_dists[j], dist = dist, sss_dists[j]
                            ind, sss_inds[j] = sss_inds[j], ind
        elif inter_sm_param.selection_algo.lower() == 'random':
            pu_inds = sample(range(len(self.pus)), k_pu)
            pu_dists = [self.cell_size * su.tx.element.location.distance(self.pus[i].tx.element.location)
                        for i in pu_inds]
            sss_inds = sample(range(len(self.sss)), k_ss)
            sss_dists = [self.cell_size * su.tx.element.location.distance(self.sss[i].rx.element.location)
                         for i in sss_inds]
        else:
            print('Unsupported selection algorithm!')
            return None
        # end selection

        # compute weights
        weights, tmp_sum_weight = [], 0.0
        for ss_dist in sss_dists:
            d = ss_dist
            d = max(d, 0.0001)  # TODO why 0.0001?

            # Weight of this SS with respect to this SU
            w = (1.0/d) ** pl_alpha
            weights.append(w)
            tmp_sum_weight += w

        # BY ME
        received_powers = []
        pl_pu_ss = []
        for i, ss_idx in enumerate(sss_inds):
            tmp_ss, all_power, tmp_pl_pu_ss = [], 0, []
            for j, pu_idx in enumerate(pu_inds):
                tmp = get_decimal(self.pus[pu_idx].tx.power) / \
                      (self.cell_size *
                       self.pus[pu_idx].tx.element.location.distance(self.sss[ss_idx].rx.element.location)) ** pl_alpha
                tmp_ss.append(tmp)
                all_power += tmp
                tmp_pl_pu_ss.append(get_decimal(self.pus[pu_idx].tx.power))
                # tmp_pow = power_with_path_loss(TRX(pus[pu_idx].loc, pus[pu_idx].p), TRX(sss[ss_
                # idx].loc, -float('inf')),
                #                                propagation_model=propagation_model, noise=noise)
                # # tmp_pow = max(tmp_pow, noise_floor)
                # tmp_ss.append(tmp_pow)
            received_powers.append([get_decimal(self.sss[ss_idx].rx.received_power) / all_power * x for x in tmp_ss])
            pl_pu_ss.append([x/y for x in tmp_pl_pu_ss for y in received_powers[-1]])
        # Compute SU transmit power
        # tp = thresh * sum(w(SS)) / sum(r(SS) / t(PU) * w(SS))
        max_transmit_power, estimated_path_loss = float('inf'), []
        for y, j in enumerate(pu_inds):
            sum_weight = 0.0
            sum_weighted_ratio = 0.0
            for x, i in enumerate(sss_inds):
                sum_weight += weights[x]
                # only DB is implemented here
                sum_weighted_ratio += weights[x] * (received_powers[i][j] / get_decimal(self.pus[j].tx.power))
            this_pu_path_loss = sum_weighted_ratio / sum_weight
            # estimated_path_loss_tmp = []
            for x, pur in enumerate(self.pus[j].purs):
                pur_element = Element(self.pus[j].tx.element.location + pur.rx.element.location, pur.rx.element.height)
                this_pr_path_loss = this_pu_path_loss - inter_sm_param.gamma * \
                                    get_db(self.cell_size * su.tx.element.location.distance(pur_element.location) /
                                           su.tx.element.location.distance(self.pus[j].tx.element.location))
                # this_pr_path_loss = this_pu_path_loss - 10.0 * inter_sm_param.gamma * \
                #                     math.log10(cell_size * su.loc.distance(pur_location) /
                #  (cell_size * su.loc.distance(pus[j].loc)))
                # estimated_path_loss_tmp.append(this_pr_path_loss)
                # this_transmit_power = pur.thr - this_pr_path_loss
                this_transmit_power = pur.rx.received_power/pur.beta - pur.interference_received_power + \
                                      this_pr_path_loss
                max_transmit_power = min(max_transmit_power, this_transmit_power)
            # estimated_path_loss.append(estimated_path_loss_tmp)
        return max_transmit_power


if __name__ == "__main__":
    pass