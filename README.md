# Tesi Rossi Gaia
## Obiettivi: Soluzione IoT per l'attuazione remota di un braccio robotico tramite sensore inerziale

### ToDo
- [x] simulare in Python un client mittente e destinatario e farli comunicare tramite Node-Red e MQTT
- [x] permettere il movimento del braccio premendo i tasti sulla tastiera 
- [x] permettere il movimento del braccio tramite broker mqtt

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

### Movimento del braccio tramite broker mqtt
Si è utilizzato il broker mosquitto come in precedenza descritto in "Client in Python".

Si è andato quindi a defire il formato dei messaggi che devono essere scambiati tramite l'applicazione node-red e il braccio meArm, optando per l'invio dei dati con JSON.
Si è quindi creato un flow che permettesse di inviare messaggi al braccio e ricevere le risposte.
Comandi di movimento per il braccio e messaggi di risposta sono inviati con due topic differenti.

Una volta definito il formato dei messaggi, si è proceduto alla creazione dello script da avviare sul raspberry pi per ricevere i comandi di movimento e farli eseguire al braccio. 
Si è quindi importato il modulo ```json``` in python per poter leggere il contenuto dell'oggetto inviato tramite node-red.
Si sono quindi create le variabili in python che permettono il movimento dei vari attuatori del braccio.
Si è definita la funzione ```on_connect``` che permette di fare una subscription al topic meArm cosi da ricevere i comandi di movimento.
Si è definita la funzione ```on_messagge``` che viene chiamata ogni volta che viene ricevuto un messaggio con topic a cui ci si era iscritti.
In particolare, questa funzione legge il comando, chiama la funzione che effettivamente fa muovere il braccio, controlla il valore di ritorno per informare node-red se il movimento è avvenuto oppure no.
