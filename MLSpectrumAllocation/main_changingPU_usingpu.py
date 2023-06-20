import sys
sys.path.append('../')
from MLSpectrumAllocation.Field import *
from random import *
import datetime
import numpy as np
import math
from MLSpectrumAllocation.commons import *


if __name__ == "__main__":
    alpha = 3 # 2.0, 4.9
    max_x = 4000  # in meter
    max_y = 4000  # in meter
    corners = [Point(0, 0), Point(max_x, 0), Point(0, max_y), Point(max_x, max_y)]
    pus_number = 15  # number of pus all over the field
    pur_number = 10  # number of purs each pu can have
    pur_threshold = 0
    pur_beta = 1
    pur_dist = 3  # distance from each pur to its pu
    min_power = -30  # in dB
    max_power = 0    # in dB
    min_pur_dist = 1
    max_pur_dist = 3
    noise_floor = -90
    noise, std = False, 30  # std in dB, real std=10^(std/10)
    MAX_POWER = True   # make it true if you want to achieve the highest power su can have without interference.
                        # calculation for conservative model would also be done
    sensors_path = 'rsc/50/sensors'

    n_samples = 500

    ss = create_sensors(sensors_path)

    date =  datetime.datetime.now().strftime('_%Y%m_%d%H_%M')
    f = open("ML/data/dynamic_pus_using_pus" + str(n_samples) + "_" + str(pus_number)+ "PUs" +
             ("_noisy_" if noise else "") + ("std" + str(std) if noise else "") +
             date + ".txt", "w")
    if MAX_POWER:
        f_max = open("ML/data/dynamic_pus_max_power" + str(n_samples) + "_" + str(pus_number) + "PUs" +
                     ("_noisy_" if noise else "") + ("std" + str(std) if noise else "") + date + ".txt", "w")
        f_conserve = open("ML/data/dynamic_pus_conservative_power" + str(n_samples) + "_" + str(pus_number) + "PUs" +
                     ("_noisy_" if noise else "") + ("std" + str(std) if noise else "") + date + ".txt", "w")
        conserve_error = 0
        inter_error = 0
        inter_ignor, conserve_ignore = 0, 0
        # lowest, highest = 0, math.sqrt(max_x**2 + max_y**2) * pow(10, max_power/10) / pur_beta
    # PUs_loc = [Point(x, y) for x in range(500, 3501, 1000) for y in range(500, 3501, 1000)]
    # PUs_loc.pop()
    # f.write("?Nodes:")
    pus = []
    for i in range(pus_number):
        pus.append(PU(location=Point(uniform(0, max_x), uniform(0, max_y)), n=pur_number, pur_threshod=pur_threshold,
                      pur_beta=pur_beta, pur_dist=(min_pur_dist, max_pur_dist), power=uniform(min_power, max_power)))
        # pus.append(PU(location=PUs_loc[i], n=pur_number, pur_threshod=pur_threshold,
        #               pur_beta=pur_beta, pur_dist=(min_pur_dist, max_pur_dist), power=uniform(min_power, max_power)))
    su = SU(Point(uniform(0, max_x), uniform(0, max_y)), uniform(min_power, max_power))

    if ss is not None:
        f_sensor = open("ML/data/dynamic_pus_sensors_" + str(n_samples) + "_" + str(pus_number) + "PUs_" + str(len(ss)) +
                        "sensors" + ("_noisy_" if noise else "") + ("std" + str(std) if noise else "") + date + ".txt", "w")

    field = Field(pus=pus, su=su, ss=ss, corners=corners, propagation_model='log', alpha=alpha, noise=noise, std=std)

    if False:   # make it True if you need to find out distribution of location with maximum allowed power
        power_width = max_power - min_power
        # max_allowed_power = [0] * (power_width + 1)
        power_range = np.arange(0, 20, 0.3)
        max_allowed_power = [0] * len(power_range)
        for y in range(max_x):
            for x in range(max_y):
                su.loc = Point(x, y)
                # low = min_power
                # high = max_power
                # mid = (high + low) // 2
                # # while mid - low > 1 and high - mid > 1:
                # while low <= high:
                #     su.p = mid
                #     if field.su_request_accept():
                #         low = mid + 1
                #     else:
                #         high = mid - 1
                #     mid = (high + low) // 2
                # max_allowed_power[mid + power_width] += 1
                for ipow, power in enumerate(power_range):
                    su.p = power
                    if not field.su_request_accept():
                        break
                if ipow != 0 and ipow != len(power_range) - 1:
                    ipow -= 1
                max_allowed_power[ipow] += 1
        print(max_allowed_power)

    if False:  #used for heatmap of the field
        f_heat = open("ML/data/su_only" + str(n_samples) + "_" + str(pus_number) + "PUs" + "_heatmap_" +
                 datetime.datetime.now().strftime('_%Y%m_%d%H_%M') + ".txt", "w")
        received_power = field.compute_field_power()
        for lrp in received_power:  # received power for a specific x=c (all )
            for prp in lrp:         # received pwer for a a specifi (x, y)
                f_heat.write(str(round(prp, 3)) + " ")
            f_heat.write('\n')
        f_heat.close()

    num_one = 0
    for i in range(n_samples):
        su.loc = Point(uniform(0, max_x), uniform(0, max_y))
        su.p = uniform(max_power - 5, max_power + 55)
        res = 0
        if field.su_request_accept(randint(0, 1)):
            res = 1
            num_one += 1
        for pu in pus:
            f.write(str(pu.loc.get_cartesian[0]) + "," + str(pu.loc.get_cartesian[1]) + "," + str(round(pu.p, 3)) + ",")
        f.write(str(su.loc.get_cartesian[0]) + "," + str(su.loc.get_cartesian[1]) + "," + str(round(su.p, 3)) + "," + str(res))
        f.write("\n")

        if ss is not None:
            for sensor in ss:
                f_sensor.write(str(round(sensor.rp, 3)) + ",")
            f_sensor.write(str(su.loc.get_cartesian[0]) + "," + str(su.loc.get_cartesian[1]) + "," +
                           str(round(su.p, 3)) + "," + str(res))
            f_sensor.write("\n")

        if MAX_POWER:  # used when you want to calculate maximum power of su it can send without any interference
            highest_pow = calculate_max_power(field.pus, field.su, field.propagation_model)
            conserve_pow = conservative_model_power(pus=field.pus, su=field.su, min_power=min_power,
                                                    propagation_model=field.propagation_model, noise_floor=noise_floor,
                                                    noise=noise)
            inter_pow = interpolation_max_power(pus=field.pus, su=field.su, sss=field.ss,
                                                inter_sm_param=InterSMParam(0, 0, 'sort', 2),
                                                propagation_model=field.propagation_model, noise=noise)
            if conserve_pow > highest_pow:
                print('Warning: Conservative power higher than max!!!, MAX:', str(highest_pow), ', Conservative: ',
                      str(conserve_pow))
            if inter_pow > highest_pow:
                print('Warning: Interpolation power higher than max!!! , MAX:', str(highest_pow), ', Interpolation: ',
                      str(inter_pow))
            if highest_pow != -float('inf'):
                conserve_error += abs(highest_pow - conserve_pow)
                if inter_pow != -float('inf') and inter_pow != float('inf'):
                    inter_error += abs(highest_pow - inter_pow)
                else:
                    inter_ignor +=1
            else:
                inter_ignor += 1
                conserve_ignore += 1

            f_max.write(str(su.loc.get_cartesian[0]) + "," + str(su.loc.get_cartesian[1]) + "," +
                        (str(round(highest_pow, 3)) if highest_pow != -float('inf') else '-inf'))
            f_max.write("\n")
            f_conserve.write(str(su.loc.get_cartesian[0]) + "," + str(su.loc.get_cartesian[1]) + "," +
                             (str(round(highest_pow, 3)) if highest_pow != -float('inf') else '-inf') + "," +
                             (str(round(conserve_pow, 3)) if conserve_pow != -float('inf') else '-inf') + "," +
                             (str(round(inter_pow, 3)) if conserve_pow != -float('inf') else '-inf'))
            f_conserve.write("\n")

        for pu in pus:
            pu.loc, pu.p = Point(uniform(0, max_x), uniform(0, max_y)), uniform(min_power, max_power)
        field.compute_purs_powers()
        field.compute_sss_received_power()

    f.close()
    if MAX_POWER:
        f_max.close()
        f_conserve.close()
    if ss is not None:
        f_sensor.close()
    print('Number of samples of class 1(accepted):', num_one)
    if MAX_POWER:
        print('Mean Error for Conservative Model:', conserve_error/(n_samples - conserve_ignore))
        print('Mean Error for Interpolation Model:', inter_error / (n_samples - inter_ignor))
    print('Number of ignore conservative: ', str(conserve_ignore))
    print('Number of ignore interpolation: ', str(inter_ignor))