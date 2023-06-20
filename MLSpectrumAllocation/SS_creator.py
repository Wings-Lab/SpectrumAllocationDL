import random as rd
import os
from typing import List
from MLSpectrumAllocation.Sensor import Sensor
from Commons.elements import RX, Element
from Commons.Point import Point, CartesianPoint


# Create sensors from a file
def create_sensors(path: str, sensor_height) -> List[Sensor]:
    sss = []
    try:
        with open(path, 'r') as f:
            # max_gain = 0.5 * num_intruders  # len(self.transmitters)
            # index = 0
            lines = f.readlines()
            for line_idx, line in enumerate(lines):
                inputs = line.split(' ')
                x, y, std, cost = float(inputs[0]), float(inputs[1]), float(inputs[2]), float(inputs[3])
                sss.append(Sensor(ss_id=line_idx, rx=RX(Element(location=Point(CartesianPoint(x, y)),
                                                                height=sensor_height)), cost=cost, std=std))
    except FileNotFoundError:
        raise ValueError('Sensor file does not exist')
    except IndexError as e:
        raise ValueError('The file given is not in correct format of x y std cost')
    return sss

def generate_sensors(STYLE: str, grid_length: int, std: float, cost: float, num_sensors: int):
    sensor_file_path = '/'.join(['rsc', 'sensors', str(grid_length), str(number_of_sensors)])
    output_style = "{x} {y} {std} {cost}\n"
    print(sensor_file_path)
    if not os.path.exists(sensor_file_path):
        os.makedirs(sensor_file_path)
    with open(sensor_file_path + '/sensors', 'w') as f:
        if STYLE == "random":
            for i in range(number_of_sensors):
                # x = round(rd.uniform(0, grid_length),2)
                # y = round(rd.uniform(0, grid_length), 2)
                x = round(rd.randint(0, grid_length - 1), 2)
                y = round(rd.randint(0, grid_length - 1), 2)
                f.write(output_style.format(x=str(x), y=str(y), std=str(std), cost=str(cost)))
        elif STYLE == "UNIFORM":
            row_col_num = int(number_of_sensors ** 0.5)
            distance = grid_length / row_col_num
            points = [p * distance for p in range(row_col_num + 1)]
            sensor_points = [min(int((points[i] + points[i + 1]) / 2), grid_length - 1) for i in range(row_col_num)]
            sensor_locations = set([(x, y) for x in sensor_points for y in sensor_points])
            for x in sensor_points:
                for y in sensor_points:
                    f.write(output_style.format(x=str(x), y=str(y), std=str(std), cost=str(cost)))
            # REST number_of_sensors - row_col_num ** 2 would be random
            sensor_cnt = row_col_num ** 2
            while sensor_cnt < number_of_sensors:
                x = round(rd.randint(0, grid_length - 1), 2)
                y = round(rd.randint(0, grid_length - 1), 2)
                if (x, y) not in sensor_locations:
                    sensor_cnt += 1
                    sensor_locations.add((x, y))
                    f.write(output_style.format(x=str(x), y=str(y), std=str(std), cost=str(cost)))
    f.close()


if __name__ == '__main__':
    # TODO this is just for Square field
    # sensor_file_path = 'rsc/sensors/1000/1200/sensors'
    STYLE = "UNIFORM"  # {"RANDOM", "UNIFORM"}
    grid_length = 100
    std = 1
    cost = 0.388882393442197
    number_of_sensors = 225
    generate_sensors(STYLE, grid_length, std, cost, number_of_sensors)
