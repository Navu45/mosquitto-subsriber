import matplotlib.pyplot as plt
import numpy
import csv

from mqtt_client.mqtt_client import MQTTClient

csv_file = "../data.csv"

box_number = "23"

topics = ["/devices/wb-msw-v3_21/controls/Humidity",
          '/devices/wb-ms_11/controls/Temperature',
          '/devices/power_status/controls/Vin']

controls = ["Humidity:",
            "Temperature:",
            "Voltage"]


def execute(self):
    string = ''.join(self.data.values())
    print(self.data)
    with open(csv_file, 'a', newline='\n') as file:
        file.write(string)
        file.write('\n')


# График влажности по времени
def create_linear():
    plt.plot(numpy.genfromtxt(csv_file, delimiter=',', usecols=0))
    plt.title('График влажности по времени')
    plt.show()


# Круговая диаграмма температуры
def create_pie():
    file = open(csv_file, 'r')
    lab_dict = csv.reader(file)
    labels = 'Холодно', 'В пределах допустимого', 'Тепло'
    sizes = [0, 0, 0]
    colors = ('blue', 'green', 'yellow')
    for line in lab_dict:
        print(line)
        if float(line[1]) <= 26.29:
            sizes[0] += 1
        elif float(line[1]) <= 26.38:
            sizes[1] += 1
        else:
            sizes[2] += 1

    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=45)
    plt.title("Круговая диаграмма температуры", pad=20)
    plt.show()


# Гистограмма напряжения на устройстве
def create_bar():
    plt.hist(numpy.genfromtxt(csv_file, delimiter=',', usecols=2))
    plt.title("Гистограмма напряжения на устройстве")
    plt.show()


if __name__ == "__main__":
    timeout = {"minutes": 10}
    mqtt_client = MQTTClient(22, topics, controls, execute, timeout=timeout)
    create_linear()
    create_pie()
    create_bar()
