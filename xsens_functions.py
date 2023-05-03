import os
import pandas as pd

def read_sensor_mapping(mapping_file):
    sensor_map = {}
    with open(mapping_file, 'r') as f:
        for line in f:
            if line.strip():
                sensor_id, sensor_name = line.strip().split(': ')
                sensor_map[sensor_id] = sensor_name
    return sensor_map

def import_sensor_data(directory, sensor_map, export_csv=False):
    sensor_data = {}
    for file_name in os.listdir(directory):
        if file_name.endswith('.txt') and len(file_name) == 32:
            sensor_id = file_name[-12:-4]
            if sensor_id in sensor_map:
                sensor_name = sensor_map[sensor_id]
                file_path = os.path.join(directory, file_name)
                data = pd.read_csv(file_path, delimiter='\t', skiprows=4, usecols=[0,2,3,4], index_col='PacketCounter')
                data = data.rename(columns={'Roll': f'{sensor_name}_Roll', 'Pitch': f'{sensor_name}_Pitch', 'Yaw': f'{sensor_name}_Yaw'})
                sensor_data[sensor_id] = data
    all_data = pd.concat(sensor_data.values(), axis=1)
    if export_csv:
        all_data.to_csv('sensor_data.csv')
    return all_data

