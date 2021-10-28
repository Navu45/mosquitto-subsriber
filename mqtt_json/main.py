import json
from datetime import datetime, timedelta

from mqtt_client.mqtt_client import MQTTClient

box_number = 22


def from_date():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


topics = ["/devices/wb-msw-v3_21/controls/Current Motion",
          "/devices/wb-ms_11/controls/Air Quality (VOC)",
          "/devices/wb-msw-v3_21/controls/Humidity",
          "/devices/wb-m1w2_14/controls/External Sensor 1"]

controls = ["Current Motion:",
            "Air Quality (VOC):",
            "Humidity",
            "1-wire DS18B20"]

data = {
    controls[0]: '',
    controls[1]: '',
    controls[2]: '',
    controls[3]: '',
    "Time": from_date(),
    "Box number": box_number
}


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


def parse_json():
    with open("../data.json", 'r') as f:
        data_dict = json.load(f)
        for item in data_dict["data_from_sensors"]:
            for control in controls:
                print(control, item[control])
            print()


if __name__ == "__main__":
    timeout = {"minutes": 5}
    mqtt_client = MQTTClient(box_number, topics, controls, write_json, timeout)
    mqtt_client.mqtt_work()