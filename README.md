# Tesi Rossi Gaia
## Obiettivi: Soluzione IoT per l'attuazione remota di un braccio robotico tramite sensore inerziale

### ToDo
[x] simulare in Python un client mittente e destinatario e farli comunicare tramite Node-Red e MQTT

### Client in Python
Si è utilizzato il broker mosquitto sulla porta 1883. Per avviare il broker

```
sudo service mosquitto start
```

mentre per terminarlo
```
sudo service mosquitto stop
```

Si è utilizzata l'implementazione di MQTT di Eclipse con Eclipse Paho.

Si è creato anche un flow su Node-RED per permettere la comunicazione tra il client in Python e Node-RED

![immagine del flow](http://github.com/GaiaRossi/Tesi-Rossi-Gaia/blob/main/images/nodered_client_flow.png)
