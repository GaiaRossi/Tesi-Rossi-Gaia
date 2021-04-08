import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connesso con un codice {}".format(str(rc)))


# creazione client
client = mqtt.Client()
client.on_connect = on_connect

# indicazione dell'indirizzo ip del broker
server_ip_address = "127.0.0.1"
port = 1883

# connessione al broker
client.connect(server_ip_address, port)

# set opzioni del messaggio da pubblicare
topic = "debug"
payload = "stringa_prova"


# avvio client publisher ma non
# all'infinito
client.loop_start()

# pubblicazione del messaggio con
# avviso a terminale
print("Invio un messaggio con topic {} e payload {}".format(topic, payload))
client.publish(topic, payload)

# attendo che il messaggio effettivamente
# arrivi
time.sleep(4)

# fermo il client
client.loop_stop()