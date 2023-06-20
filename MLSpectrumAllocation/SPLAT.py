from MLSpectrumAllocation.propgation_model import PropagationModel
from Commons.Point import GeographicPoint, to_geographic, Point
from Commons.elements import Element
import os
import subprocess
from random import uniform
import re
import time
from MLSpectrumAllocation.splat_site import Site


class SPLAT(PropagationModel):
    SDF_DIR = 'rsc/splat/sdf'
    OFFSET = GeographicPoint(-1/111111, -1/111111)  # offset for one meter that should be added to upper_left_loc
    TIMEOUT = 0.4
    APPROX = 10  # SPLAT! will not be used if there is a previous saved path loss in vicinity of APPROX meter
    SPLAT_COMMAND = 'splat'  # 'splat' or 'splat-hd'

    def __init__(self, upper_left_loc, pl_dict: dict=None):  # field_width: int, field_length: int
        if type(upper_left_loc) == GeographicPoint:
            self.__upper_left_ref = upper_left_loc  # (lat, lon) of upper left corner
        elif len(upper_left_loc) == 2:
            self.__upper_left_ref = GeographicPoint(upper_left_loc[0], upper_left_loc[1])
        else:
            raise ValueError("Upper left corner point is not given")
        if not pl_dict:
            self.__pl_dict = {}
        self.__FETCH_TIME = 0
        self.__FETCH_NUM = 0
        self.__EXEC_TIME = 0
        self.__EXEC_NUM = 0
        PropagationModel.__init__(self, 'splat')
        # self.field_width = field_width
        # self.field_length = field_length
        # self.create_lrp_file()

    @property
    def upper_left_ref(self) -> GeographicPoint:
        return self.__upper_left_ref

    @property
    def pl_dict(self) -> dict:
        return self.__pl_dict

    @pl_dict.setter
    def pl_dict(self, pl_dict: dict):
        self.__pl_dict = pl_dict

    @property
    def FETCH_TIME(self) -> int:
        return self.__FETCH_TIME

    @property
    def FETCH_NUM(self) -> int:
        return self.__FETCH_NUM

    @property
    def EXEC_TIME(self) -> int:
        return self.__EXEC_TIME

    @property
    def EXEC_NUM(self) -> int:
        return self.__EXEC_NUM

    @staticmethod
    def create_qth_files(site: Site):
        qthfile = site.name
        with open(qthfile + '.qth', 'w') as fq:
            fq.write(str(site))
        return qthfile

    def path_loss(self, tx: Element, rx: Element, iteration: int=0):
        if iteration == 20:
            raise Exception("Sample skipped")
        tmp_fetch_time = time.time()
        approx_tx = (int(tx.location.cartesian.x//SPLAT.APPROX) * SPLAT.APPROX,
                     int(tx.location.cartesian.y//SPLAT.APPROX) * SPLAT.APPROX)
        approx_rx = (int(rx.location.cartesian.x//SPLAT.APPROX) * SPLAT.APPROX,
                     int(rx.location.cartesian.y//SPLAT.APPROX) * SPLAT.APPROX)
        tx_dict_key = '{:04d}{:04d}'.format(approx_tx[0], approx_tx[1])
        rx_dict_key = '{:04d}{:04d}'.format(approx_rx[0], approx_rx[1])
        if tx_dict_key in self.pl_dict:
            if rx_dict_key in self.pl_dict[tx_dict_key]:
                # free, itm = self.pl_dict[tx_dict_key][rx_dict_key]  # old format which the map has both values
                pl_value = self.pl_dict[tx_dict_key][rx_dict_key]
                self.__FETCH_TIME += time.time() - tmp_fetch_time
                self.__FETCH_NUM += 1
                # return itm if itm != 0.0 else free  # old version
                return pl_value
        tmp_exec_time = time.time()
        pwd = os.getcwd()
        file_dir = os.path.dirname(__file__)
        os.chdir(file_dir + "/" + SPLAT.SDF_DIR)
        # terr_dir = os.getcwd()
        # os.chdir('out')

        tx_loc = to_geographic(self.upper_left_ref, tx.location)
        rx_loc = to_geographic(self.upper_left_ref, rx.location)
        # print(haversine_distance(tx_loc, rx_loc)*1000)
        tx_site = Site('tx', tx_loc.lat, tx_loc.lon, tx.height)
        rx_site = Site('rx', rx_loc.lat, rx_loc.lon, rx.height)
        tx_name = SPLAT.create_qth_files(tx_site)
        rx_name = SPLAT.create_qth_files(rx_site)

        # running splat command
        path_loss_command = [SPLAT.SPLAT_COMMAND, '-t', tx_name + '.qth', '-r', rx_name + '.qth']

        count = 1
        # subprocess.call(path_loss_command, stdout=open(os.devnull, 'wb'))
        try:
            p = subprocess.Popen(path_loss_command, stdout=open(os.devnull, 'wb'))
        except (OSError or ValueError or TimeoutError) as e:
            print("Error happened executing SPLAT! command.\n" + e)
            count += 1
            pass
        start_time = time.time()
        while True:
            if p.poll() is not None:
                # count = 1
                break
            else:
                if time.time() - start_time > SPLAT.TIMEOUT:
                    if count > 50:
                        # print('Error: Too many repetition for a location')
                        raise Exception("Error: Too many SPLAT! repetition for a location")
                    # print('SPLAT! does not produce result for', ' '.join(path_loss_command), 'for ', count, 'times.')
                    count += 1
                    p.kill()
                    # splat! does not respond
                    # os.remove(tx_name + '.qth')
                    # os.remove(rx_name + '.qth')
                    offset = count
                    # tx_loc = SPLAT.get_loc(upper_left_ref, tx[0] + uniform(-(SPLAT.APPROX/2)**2 - offset,
                    # (SPLAT.APPROX/2)**2),
                    #                        tx[1] + uniform(-(SPLAT.APPROX / 2) ** 2 - offset,
                    # (SPLAT.APPROX / 2) ** 2 +
                    #                                        offset))
                    tx_loc = to_geographic(self.upper_left_ref, tx.location + Point((uniform(-offset, offset),
                                                                                    uniform(-offset, offset))))
                    rx_loc = to_geographic(self.upper_left_ref, rx.location + Point((uniform(-offset, offset),
                                                                                    uniform(-offset, offset))))

                    tx_site = Site('tx', tx_loc.lat, tx_loc.lon, tx.height, tx_name)
                    rx_site = Site('rx', rx_loc.lat, rx_loc.lon, rx.height, rx_name)
                    tx_name = SPLAT.create_qth_files(tx_site)
                    rx_name = SPLAT.create_qth_files(rx_site)

                    try:
                        path_loss_command = [SPLAT.SPLAT_COMMAND, '-t', tx_name + '.qth', '-r', rx_name + '.qth']
                        p = subprocess.Popen(path_loss_command, stdout=open(os.devnull, 'wb'))
                    except (OSError or ValueError or TimeoutError) as e:
                        print("Error happened executing SPLAT! command.\n" + e)
                        # pass
                    start_time = time.time()  # reset time
                else:
                    time.sleep(SPLAT.TIMEOUT/5)

        output_name = "{tx_name}-to-{rx_name}.txt".format(tx_name=tx_name, rx_name=rx_name)
        # output_name = tx_name + '-to-' + rx_name + '.txt'  # the file where the result will be created
        try:
            free_pl, itm_pl = self.process_output(output_name)
        except FileNotFoundError:
            print('Warning: Recalling is happening')
            os.chdir(pwd)
            return self.path_loss(tx, rx, iteration + 1)

        # removing created files
        try:
            os.remove(output_name)
            os.remove(tx_name + '.qth')
            os.remove(rx_name + '.qth')
            os.remove(tx_name + '-site_report.txt')
        except (FileNotFoundError, Exception) as e:
            pass

        os.chdir(pwd)
        pl_value = float(itm_pl) if float(itm_pl) != 0.0 else float(free_pl)
        if tx_dict_key not in self.pl_dict:
            # self.__pl_dict[tx_dict_key] = {rx_dict_key: (float(free_pl), float(itm_pl))}  # old version
            self.__pl_dict[tx_dict_key] = {rx_dict_key: pl_value}
        else:
            # self.__pl_dict[tx_dict_key][rx_dict_key] = (float(free_pl), float(itm_pl))  # old version
            self.__pl_dict[tx_dict_key][rx_dict_key] = pl_value
        self.__EXEC_TIME += time.time() - tmp_exec_time
        self.__EXEC_NUM += 1
        # return float(itm_pl) if float(itm_pl) != 0.0 else float(free_pl)  # old version
        return pl_value

    @staticmethod
    def process_output(file_name):
        positive_float = r'(\d+\.\d+)'
        free_space_pattern = r'Free space.*\D{}.*'.format(positive_float)
        itm_pattern = r'ITWOM Version 3.0.*\D{}.*'.format(positive_float)
        free_p = re.compile(free_space_pattern)
        itm_p = re.compile(itm_pattern)
        with open(file_name, encoding="ISO-8859-1", mode='r') as f:
            content = f.read()
            free_m = free_p.search(content)
            free_pl = free_m.group(1) if free_m else 0

            itm_m = itm_p.search(content)
            itm_pl = itm_m.group(1) if itm_m else 0
        return free_pl, itm_pl

    def __str__(self):
        "SPLAT! PM:\nUpper-left corner:{}".format(self.upper_left_ref)


if __name__ == "__main__":
    # 40.800595, -73.107507
    top_left_ref = GeographicPoint(40.800595, 73.107507)
    splat = SPLAT(top_left_ref)
    # splat.generate_sdf_files()
    free_pl, itm_pl = splat.path_loss(Element(Point((180, 170)), 300), Element(Point((100, 100)), 15))
    print('free path loss:', free_pl, ', itm path loss:', itm_pl)