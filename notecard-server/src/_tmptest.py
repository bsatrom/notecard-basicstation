import math

def bytesToBody(bytesInHex):
    payloadBytes = bytearray.fromhex(bytesInHex)

    print(payloadBytes)

    rawTemp = payloadBytes[0] + payloadBytes[1] * 256
    print(rawTemp)

    formattedTemp = sflt162f(rawTemp) * 100
    print(formattedTemp)

    rawHu = payloadBytes[2] + payloadBytes[3] * 256

    formattedHumidity = sflt162f(rawHu) * 100
    print(formattedHumidity)

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

print(bytesToBody("07747276"))
