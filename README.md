# Tesi Rossi Gaia
## Obiettivi: Soluzione IoT per l'attuazione remota di un braccio robotico tramite sensore inerziale

### ToDo
- [x] simulare in Python un client mittente e destinatario e farli comunicare tramite Node-Red e MQTT
- [ ] permettere il movimento del braccio premendo i tasti sulla tastiera 

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

![immagine del flow](http://github.com/GaiaRossi/Tesi-Rossi-Gaia/blob/main/images/nodered_client_flow.png?raw=true)

### Movimento del braccio tramite tastiera
Si è utilizzato il modulo gpiozero per andare a modificare i valori degli angoli degli attuatori.

Per leggere i tasti premuti si è usato il modulo keyboard che richiede i permessi di root.

Il programma funziona bene, ma controllare la gestione del movimento e dei buffer che leggono la tastiera che rendono il movimento del braccio quasi imprevedibile.
