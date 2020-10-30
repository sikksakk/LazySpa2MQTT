import requests
import json
import time
import paho.mqtt.client as paho
import datetime
import timeago

#Read config
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

email = config.get("Layzspa", 'email')
password = config.get("Layzspa", 'password')
did = config.get("Layzspa", 'did')
api_token = config.get("Layzspa", 'api_token')
mqtt_host = config.get("MQTT", 'host')
mqtt_client = config.get("MQTT", 'client')
mqtt_rootSubject = config.get("MQTT", 'rootSubject')
print("Read config:")
print("--------------------")
print(f'email:\t\t\t{email}')
if (password):
    print('password:\t\t********')
else:
    print('Password not set..')
print(f'did:\t\t{did}')
print(f'api_token:\t\t{api_token}')
print(f'mqtt_host:\t\t{mqtt_host}')
print(f'mqtt_client:\t\t{mqtt_client}')
print(f'mqtt_rootSubject:\t{mqtt_rootSubject}')
print("--------------------")

#Function to send a message to the MQTT Broker
def sendMQTT(subject, value):
    pub_subject = mqtt_rootSubject+"/"+subject
    client.publish(pub_subject,value)
    print(f'Sent \"{value}\" to subject {pub_subject}')

def LazySpaLogin(email, password):
    print("For now you have to get did + api_token manually")
    exit (1)
    
def finished(exitcode=0):
    client.disconnect()
    print(f'Exiting with code {exitcode}')
    exit(exitcode)

if (did == None or api_token == None) and (email and password):
    LazySpaLogin(email,password)
elif (did and api_token):
    print("LazySpa API config is OK")
else:
    print("You have to define either did and api_token, or email and password..")
    exit(1)

def onoroff(int):
    if (int):
        return "ON"
    else:
        return "OFF"

#Connect to the MQTT Broker
client=paho.Client(mqtt_client)
print(f'Connecting to MQTT broker: {mqtt_host}')
client.connect(mqtt_host)

#LazySpa API calls
parameters = {
     "did": did,
     "api_token": api_token
 }

response = requests.post("https://mobileapi.lay-z-spa.co.uk/v1/gizwits/is_online", params=parameters)
if response.status_code != 200 or response.json() == None:
    print(f'Response from API was not OK, exiting.. {response.status_code}')
    finished(1)
is_online = response.json()
data = is_online["data"]
if data != "true":
    print(f'Pump seems to be offline.. status from api is: {data}')
    finished(1)

response = requests.post("https://mobileapi.lay-z-spa.co.uk/v1/gizwits/status", params=parameters)
if response.status_code != 200 or response.json() == None:
    print(f'Response from API was not OK, exiting.. {response.status_code}')
    finished(1)

tmp = response.json()
data = tmp["data"]
attr = data["attr"]

#Send the updated_at formatted as a "x minutes ago" string
updated_at = datetime.datetime.fromtimestamp(data["updated_at"])
now = datetime.datetime.now() + datetime.timedelta(seconds = 60 * 3.4)
updated_ago = timeago.format(updated_at, now)
sendMQTT("updated_at_string", updated_ago)

#Send updated_at
sendMQTT("updated_at", data["updated_at"])

#Send temp_set
sendMQTT("temp_set", attr["temp_set"])

#Send temp_now
sendMQTT("temp_now", attr["temp_now"])

#Send earth
sendMQTT("earth", onoroff(attr["earth"]))

#Send filter_power
sendMQTT("filter_power", onoroff(attr["filter_power"]))

#Send heat_temp_reach
sendMQTT("heat_temp_reach", onoroff(attr["heat_temp_reach"]))

#Send heat_power
sendMQTT("heat_power", onoroff(attr["heat_power"]))

#Send locked
sendMQTT("locked", onoroff(attr["locked"]))

#Send power
sendMQTT("power", onoroff(attr["power"]))

#Send wave_power
sendMQTT("wave_power", onoroff(attr["wave_power"]))

finished()

# {
#     "data": {
#         "attr": {
#             "earth": 0,
#             "filter_appm_min": 0,
#             "filter_power": 1,
#             "filter_timer_min": 0,
#             "heat_appm_min": 0,
#             "heat_power": 1,
#             "heat_temp_reach": 1,
#             "heat_timer_min": 0,
#             "locked": 1,
#             "power": 1,
#             "system_err1": 0,
#             "system_err2": 0,
#             "system_err3": 0,
#             "system_err4": 0,
#             "system_err5": 0,
#             "system_err6": 0,
#             "system_err7": 0,
#             "system_err8": 0,
#             "system_err9": 0,
#             "temp_now": 38,
#             "temp_set": 38,
#             "temp_set_unit": "\u6444\u6c0f",
#             "wave_appm_min": 59940,
#             "wave_power": 0,
#             "wave_timer_min": 59940
#         },
#         "did": "asdfasdfasdfasdf",
#         "updated_at": 1603827824
#     }
# }