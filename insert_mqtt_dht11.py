from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
iclient = InfluxDBClient(host='localhost', port=8086, username='influx_ship', password='1234', database='riatechdb')

def on_connect( client, userdata, flags, rc ):
   print('Connect with result code ' + str(rc) )
   client.subscribe('MyOffice/#')

def on_message( client, userdata, msg ):
   print( msg.topic +' '+str(msg.payload) )        # 수신되는 topic은 MyOffice/Indoor/Temp 또는 MyOffice/Indoor/Humi
   information = msg.topic.split('/')              # ['MyOffice', 'Indoor', 'Temp']
   json_body = [ ]
   data_point = { 'measurement':'sensors',
        'tags':{'Location':' ', 'Sublocation':' '},
        'fields': {'Temp': 0.0, 'Humi':0.0}
                }
   data_point['tags']['Location'] = information[0]
   data_point['tags']['Sublocation'] = information[1]
   data_point['fields'][information[2]] = float(msg.payload)
   json_body.append(data_point)
   iclient.write_points( json_body )

client = mqtt.Client( )
client.username_pw_set(username='mqtt_ship', password='1234')
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)
client.loop_forever( )
