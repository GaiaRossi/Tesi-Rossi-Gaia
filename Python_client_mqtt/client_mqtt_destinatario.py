import paho.mqtt.client as mqtt

# funzione chiamata quando il client si vuole
# connettere al broker
def on_connect(client, userdata, flags, rc):
    print("Connesso con un codice {}".format(str(rc)))

    #subscribe al topic debug
    client.subscribe('debug')

# funzione chiamata quando viene ricevuto
# un messaggio per il topic a cui
# si è fatto il subscribe
def on_message(client, userdata, msg):
    print("Topic: {}, messaggio: {}".format(msg.topic, msg.payload.decode("UTF-8")))

# creazione client e set delle funzioni
# precedentemente create
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# indicazione dell'indirizzo ip del broker
server_ip_address = "127.0.0.1"
port = 1883

# connessione con il broker
client.connect(server_ip_address, port)


#client che ascolta per sempre
client.loop_forever()