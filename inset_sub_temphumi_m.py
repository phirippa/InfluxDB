from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
iclient = InfluxDBClient(host='localhost', port=8086, 
                         username='influx_ship', password='1234', database='riatechdb')

def on_connect(client, userdata, flags, rc):
    print('Connect with result code ' + str(rc))
    client.subscribe('MyOffice/#')

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))   #msg.topic - 'MyOffice/Indoor/SensorValue'
    information = msg.topic.split('/')  # ['MyOffice', 'Indoor', 'SensorValue']
    payload = eval(msg.payload)

    json_body = []
    data_point = {  'measurement':'sensors',
                    'tags':{'Location':' ', 'SubLocation':' '},
                    'fields':{'Temp':0.0, 'Humi':0.0}
                 }
    data_point['tags']['Location']    = information[0]
    data_point['tags']['SubLocation'] = information[1]
    data_point['fields']['Temp'] = payload['Temp']
    data_point['fields']['Humi'] = payload['Humi']
    json_body.append(data_point)
    iclient.write_points(json_body)

client = mqtt.Client()
client.username_pw_set(username='mqtt_ship', password='1234')
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)
client.loop_forever()
