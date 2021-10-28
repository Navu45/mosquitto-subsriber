from paho.mqtt import client as mqtt_client
from datetime import datetime, timedelta


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(self, client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    for i in range(len(self.topics)):
        if str(msg.topic) == self.topics[i]:
            self.data[self.controls[i]] = msg.payload.decode()


class MQTTClient(mqtt_client.Client):
    def __init__(self, box_number, topics, controls, operation, timeout):
        super().__init__()
        self.box_number = box_number
        self.ip_address = f"192.168.2.{self.box_number}"
        self.username = "user"
        self.psw = "123123"
        self.topics = topics
        self.data = {controls[i]: '' for i in range(len(controls))}
        self.operation = operation
        self.on_message = on_message
        self.on_connect = on_connect
        self.timeout = timeout

    def mqtt_work(self):
        client = mqtt_client.Client()
        client.username_pw_set(self.username, self.username)
        client.connect(self.ip_address, 1883)

        for topic in self.topics:
            client.subscribe(topic)

        now = datetime.now()
        timeout = timedelta(days=self.timeout["days"], hours=self.timeout["hours"],
                            minutes=self.timeout["minutes"], seconds=self.timeout["seconds"])
        while (now - datetime.now()) < timeout:
            client.loop_start()
            self.execute()
            client.loop_stop()

    def execute(self):
        self.operation()
