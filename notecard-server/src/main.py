import json
import os
from periphery import I2C
import base64
import math

import notecard
from notecard import note

import asyncio
import websockets

productUID = os.getenv('NC_PRODUCT_UID')

print("Connecting to Notecard...")
port = I2C("/dev/i2c-1")
card = notecard.OpenI2C(port, 0, 0, debug=True)

def base64ToBody(payload):
    bytesInHex = base64.b64decode(payload).hex()
    payloadBytes = bytearray.fromhex(bytesInHex)

    rawTemp = payloadBytes[0] + payloadBytes[1] * 256
    formattedTemp = sflt162f(rawTemp) * 100

    rawHu = payloadBytes[2] + payloadBytes[3] * 256
    formattedHumidity = sflt162f(rawHu) * 100

    return {"tempC": formattedTemp, "humidity": formattedHumidity}

def sflt162f(rawSflt16):
    rawSflt16 &= 0xFFFF

    if (rawSflt16 == 0x8000):
	    return -0.0

    sSign = -1 if ((rawSflt16 & 0x8000) != 0) else 1

    exp1 = (rawSflt16 >> 11) & 0xF

    mant1 = (rawSflt16 & 0x7FF) / 2048.0

    f_unscaled = sSign * mant1 * math.pow(2, exp1 - 15)

    return f_unscaled

def baseToBytes(payload):
    return base64.b64decode(payload).hex()

async def addNote(websocket, path):
    async for message in websocket:
        print(f'New MSG: {message}')
        # req = {"req": "note.add"}
        # req["body"] = base64ToBody(message)
        # req["payload"] = message
        # req["sync"] = True
        # card.Transaction(req)

        # await websocket.send("Note added")

start_server = websockets.serve(addNote, "notecard-server", 8765)

async def main():
  print(f'Configuring Product: {productUID}...')

  req = {"req": "hub.set"}
  req["product"] = productUID
  req["mode"] = "periodic"
  req["outbound"] = 60
  req["inbound"] = 120
  req["align"] = True

  card.Transaction(req)

asyncio.get_event_loop().run_until_complete(main())

print('Starting Notecard websocket server...')
asyncio.get_event_loop().run_until_complete(start_server)
print('Websocket server listening...')
asyncio.get_event_loop().run_forever()