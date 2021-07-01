import asyncio, binascii, sys, curses
from threading import Thread
from bleak import BleakClient

mitch_ble_address = "C8:49:E4:54:41:41"
CMMD_CHAR_UUID = "d5913036-2d8a-41ee-85b9-4e361aa5c8a7"
DATA_CHAR_UUID = "09bf2c52-d1d9-c0b7-4145-475964544307"

async_loop = asyncio.new_event_loop()

client = None
connected = False

READ_ACCESS_BYTE = 0x82
WRITE_ACCESS_BYTE = 0x02

#settaggio del funzionamento del bracciale
#sys tx
STATE_OF_SYSTEM = 0xF8
#attivo tutto il possibile del bracciale
MODE = 0x04
#funzionera con frequenza 50hz
FREQUENCY = 0x04
#lunghezza dei dati inviati
LENGTH = 0x03

async def connection(address):
    global client
    global connected

    client = BleakClient(address)
    print("Client connesso: {}".format(client.is_connected))
    #da fare nel caso in cui la connessione non sia 
    #avvenuta subito ma devo aspettare in modo asincrono
    #il mitch che si connetta
    if not client.is_connected:
        await client.connect()
        print("Client connesso: {}".format(client.is_connected))
        connected = client.is_connected

        #set delle opzioni
        #protocollo tlv, lunghezza totale 20 byte
        pkt = bytearray([WRITE_ACCESS_BYTE, LENGTH, STATE_OF_SYSTEM, MODE, FREQUENCY])
        for i in range(15):
            pkt.append(0)
        print("Packet: {}, lenght of packet: {}".format(binascii.hexlify(pkt), len(pkt)))

        await client.write_gatt_char(CMMD_CHAR_UUID, pkt, True)

        response = await client.read_gatt_char(CMMD_CHAR_UUID)
        print("Risposta: {}".format(response.hex()))

        #inizio a leggere i valori
        await client.start_notify(DATA_CHAR_UUID, notification_handler)
        await asyncio.sleep(20.0)
        await client.stop_notify(DATA_CHAR_UUID)

        await client.disconnect()
        exit(0)

def notification_handler(sender, data):
    #print("Letto sullo stream dati: {}".format(binascii.hexlify(data)))
    data_conversion(data)

def main_callback():
    asyncio.set_event_loop(async_loop)
    asyncio.get_event_loop().run_until_complete(connection(mitch_ble_address))
    async_loop.run_forever()

def data_conversion(pkg):
    num_list = list(pkg)

    # gyro
    x_gyro = int.from_bytes(bytes(num_list[4:6]), byteorder='little', signed=True)*0.07*0.01745
    y_gyro = int.from_bytes(bytes(num_list[6:8]), byteorder='little', signed=True)*0.07*0.01745
    z_gyro = int.from_bytes(bytes(num_list[8:10]), byteorder='little', signed=True)*0.07*0.01745

    # axl
    #x sensibilita ) / 1000 ) x gravita
    x_axl = ((int.from_bytes(bytes(num_list[10:12]), byteorder='little', signed=True)*0.488)/1000)*9.8066
    y_axl = ((int.from_bytes(bytes(num_list[12:14]), byteorder='little', signed=True)*0.488)/1000)*9.8066
    z_axl = ((int.from_bytes(bytes(num_list[14:16]), byteorder='little', signed=True)*0.488)/1000)*9.8066

    sys.stdout.write("\rGiroscopio: {0:.2f}, {1:.2f}, {2:.2f} | Accelerometro: {3:.2f}, {4:.2f}, {5:.2f}\r".format(x_gyro, y_gyro, z_gyro,
                                                                        x_axl, y_axl, z_axl))
    sys.stdout.flush()

    print()

main_thread = Thread(target=main_callback)
main_thread.start()