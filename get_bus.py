from collections import namedtuple
from datetime import datetime

import requests
import csv
import json

BusPoint = namedtuple('BusPoint', [
    'id',
    'name',
    'type', # Uses IconPrefix
    'route_id',
    'pattern_id',
    'provider',
    'longitude',
    'latitude',
    'orientation',
    'speed',
    'has_apc',
    'apc_percentage',
    'door_status',
    'last_updated',
    'request_time',
])

bus_info_mock = json.loads('[{"ID":39,"APCPercentage":0,"RouteId":2092,"PatternId":2092,"Name":"2164","HasAPC":true,"IconPrefix":"bus_","DoorStatus":1,"Latitude":32.876946,"Longitude":-117.235021,"Coordinate":{"Latitude":32.876946,"Longitude":-117.235021},"Speed":1,"Heading":"E","Updated":"5:12:47P","UpdatedAgo":"ago"},{"ID":21,"APCPercentage":10,"RouteId":2092,"PatternId":2092,"Name":"0724","HasAPC":true,"IconPrefix":"bus_","DoorStatus":0,"Latitude":32.865112,"Longitude":-117.225048,"Coordinate":{"Latitude":32.865112,"Longitude":-117.225048},"Speed":2,"Heading":"NE","Updated":"5:12:43P","UpdatedAgo":"4s ago"},{"ID":31,"APCPercentage":18,"RouteId":2092,"PatternId":2092,"Name":"0726","HasAPC":true,"IconPrefix":"bus_","DoorStatus":0,"Latitude":32.743619,"Longitude":-117.181114,"Coordinate":{"Latitude":32.743619,"Longitude":-117.181114},"Speed":7,"Heading":"S","Updated":"5:12:27P","UpdatedAgo":"20s ago"}]')

heading_to_orientation = {
    'N': 0,
    'NE': 45,
    'E': 90,
    'SE': 135,
    'S': 180,
    'SW': 225,
    'W': 270,
    'NW': 315,
}

# route_id (string)
# returns object
def request_route_vehicle_info(route_id):
    request_url = 'https://ucsdbus.com/Route/' + route_id + '/Vehicles'
    bus_info_req = requests.get(request_url)
    return bus_info_req.json()

def bus_info_to_bus_points(bus_info_obj):
    return [bus_obj_to_bus_point(bus) for bus in bus_info_obj]

# bus (dict)
def bus_obj_to_bus_point(bus):
    updated_time_str = bus['Updated']
    updated_time = datetime.strptime(updated_time_str + "M", "%I:%M:%S%p")
    last_updated = datetime.combine(
            datetime.now(),
            updated_time.timetz(),
        ).strftime('%s')
    orientation = heading_to_orientation.get(bus['Heading'], None)
    request_time = datetime.now().strftime('%s')

    return BusPoint(
        id=bus['ID'],
        name=bus['Name'],
        type=bus['IconPrefix'].replace('_', ''),
        route_id=bus['RouteId'],
        pattern_id=bus['PatternId'],
        provider='UCSD',
        longitude=bus['Longitude'],
        latitude=bus['Latitude'],
        orientation=orientation,
        speed=bus['Speed'],
        has_apc=bus['HasAPC'],
        apc_percentage=bus['APCPercentage'],
        door_status=bus['DoorStatus'],
        last_updated=last_updated,
        request_time=request_time,
    )

# bus_point (BusPoint)
# csv_dict_writer (DictWriter)
def append_bus_point_to_csv(bus_point, csv_dict_writer):
    csv_dict_writer.writerow(bus_point._asdict())
    
def get_dict_writer(out_file):
    return csv.DictWriter(out_file, BusPoint._fields)

# route_id (string)
def get_live_bus_info(route_id):
    return bus_info_to_bus_points(request_route_vehicle_info(route_id))

def get_mock_bus_info(route_id):
    return bus_info_to_bus_points(bus_info_mock)
    

