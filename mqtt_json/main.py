import json
from datetime import datetime
import xml.etree.ElementTree as xmlTree

from json2xml import json2xml
from json2xml.utils import readfromjson
from mqtt_client.mqtt_client import MQTTClient

box_number = 22


def from_date():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


topics = ["/devices/wb-msw-v3_21/controls/Current Motion",
          "/devices/wb-ms_11/controls/Air Quality (VOC)",
          "/devices/wb-msw-v3_21/controls/Humidity",
          "/devices/wb-m1w2_14/controls/External Sensor 1"]

controls = ["Current Motion",
            "Air Quality",
            "Humidity",
            "Sensor 1-wire DS18B20"]

data = [
    controls[0],
    controls[1],
    controls[2],
    controls[3],
    "Time",
    "Box number",
]


# JSON structure
def write_json(new_data, filename='../data.json'):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["data_from_sensors"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def write_xml(filename='../data.json'):
    json_data = readfromjson(filename)
    xml_data = json2xml.Json2xml(json_data, wrapper="all", pretty=True, attr_type=False).to_xml()
    with open("../data.xml", 'w') as xml_file:
        xml_file.write(xml_data)


def parse_json():
    with open("../data.json", 'r') as f:
        data_dict = json.load(f)
        for item in data_dict["data_from_sensors"]:
            for key in data:
                print(key, item[key])
            print()


def parse_xml():
    tree = xmlTree.parse('../data.xml')
    root = tree.getroot()

    for item in root[0]:
        for i, value in enumerate(item):
            print(data[i], value.text)
        print()


if __name__ == "__main__":
    commands = [write_json, write_xml, parse_json, parse_xml]
    print("What action do you want to perform? (0 - 3 for these commands: " + str(commands) + ")")
    n = int(input())
    while n != -1:
        if n == 0:
            timeout = {"minutes": 5}
            mqtt_client = MQTTClient(box_number, topics, controls, commands[n], timeout)
            mqtt_client.mqtt_work()
        else:
            commands[n]()
        n = int(input())

