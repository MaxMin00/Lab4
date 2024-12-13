# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np


#TODO 1: modify the following parameters
#Starting and end index, modify this
device_st = 0
device_end = 5

#Path to the dataset, modify this
data_path = "data2/vehicle{}.csv"

names = '''J1Vv2ymQvc6qyqZ
tD5GHF2BN0es3GW
Klr8eqPBXVFQoEZ
LBpaQWKf8v2EXP4
z140zo89kLdt5op
ffSNLC3yumrwqa4
EQyS2xiNminej1D
6itw9v4feAcml30
8hK2JFEGGNrVz3S
t8x7r05zIIOosuI
9ZU1pnaHlfoBWkX
3PQNFtZpsnX5weR
5qgG3OE09xNoble
2Wkd32sQA8WT7sL
lgtH9hlsMILLs9O'''.split("\n")
#Path to your certificates, modify this
certificate_formatter = "/Users/maxmin/Desktop/lab4/info/{}_cert.pem"
key_formatter = "/Users/maxmin/Desktop/lab4/info/{}_private.key"


class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        
        #TODO 2: modify your broker address
        self.client.configureEndpoint("a2qy3rahq3ilom-ats.iot.us-east-2.amazonaws.com", 8883)
        self.client.configureCredentials("/Users/maxmin/Desktop/lab4/info/AmazonRootCA1.pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        

    def customOnMessage(self,message):
        #TODO3: fill in the function to show your received message
        print("client {} received payload {} from topic {}".format(self.device_id, message.payload, message.topic))


    # Suback callback
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass


    def publish(self, Payload="payload"):
        #TODO4: fill in this function for your publish
        self.client.subscribeAsync("myTopic", 0, ackCallback=self.customSubackCallback)
        
        self.client.publishAsync("myTopic", Payload, 0, ackCallback=self.customPubackCallback)



print("Loading vehicle data...")
data = []
for i in range(5):
    a = pd.read_csv(data_path.format(i))
    data.append(a)

print("Initializing MQTTClients...")
clients = []
for device_id in range(device_st, device_end):
    device_id = names[device_id]
    client = MQTTClient(device_id,certificate_formatter.format(device_id,device_id) ,key_formatter.format(device_id,device_id))
    client.client.connect()
    clients.append(client)
 

while True:
    print("send now?")
    x = input()
    if x == "s":
        for i,c in enumerate(clients):
            c.publish()

    elif x == "d":
        for c in clients:
            c.client.disconnect()
        print("All devices disconnected")
        exit()
    else:
        print("wrong key pressed")

    time.sleep(3)





