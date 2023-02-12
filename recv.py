from rflib import *

def nibble_at(b, i):
    return b.encode('hex')[i]

def nibble_count(b):
    return len(b) * 2

def is_manchester(n):
    length = nibble_count(n)
    for i in range(length):
        nibble = nibble_at(n, i)
        if nibble != 'e' and nibble != '8':
            return False
    return True

def manchester_to_chan(b):
    value = b.encode('hex')
    if value == 'e888':
        return "CH1 "
    elif value == 'eeee':
        return "CH2 "
    else:
        return value + " "

def manchester_to_mode(b):
    value = b.encode('hex')
    if value == '888e':
        return "Shock    "
    elif value == '88e8':
        return "Vibrate  "
    elif value == '8e88':
        return "Beep     "
    elif value == 'e8e8':
        return "Auto     "
    elif value == 'eeee':
        return "Shutdown "
    else:
        return value + " "

def manchester_to_blob(n):
    acc = 0
    length = nibble_count(n)
    for i in range(length):
        nibble = nibble_at(n, i)
        if nibble == 'e':
            acc |= 1 << ((length - 1) - i)
    return str(acc) + " "

def manchester_to_int(b):
    value = b.encode('hex')
    if value == '88888888':
        return "0 "
    elif value == '8888eee8':
        return "1 "
    elif value == '888eee88':
        return "2 "
    elif value == '88e8e8e8':
        return "3 "
    elif value == '88eee888':
        return "4 "
    elif value == '8e888ee8':
        return "5 "
    elif value == '8e8e8e88':
        return "6 "
    elif value == '8ee888e8':
        return "7 "
    else:
        return value + " "

print("Setting up dongle...")
while True:
    try:
        d = RfCat()
        d.setFreq(434000000)
        d.setMdmModulation(MOD_ASK_OOK)
        d.setMdmDRate(3550)
        d.makePktFLEN(32)
        d.setMdmSyncWord(0x01f8)
        d.setMdmSyncMode(2)
        d.setMdmNumPreamble(0)
        d.setEnableMdmManchester(False)
        d.setPktPQT(0)
        break
    except:
        pass

print("Listening...")

while True:
    try:
        dat = d.RFrecv(1)[0]
        if is_manchester(dat) and len(dat) == 32:
            print(
                manchester_to_chan(dat[0:2]) +
                manchester_to_mode(dat[2:4]) +
                manchester_to_blob(dat[4:12]) +
                manchester_to_int(dat[12:16]) +
                manchester_to_int(dat[16:20]) +
                manchester_to_int(dat[20:24]) +
                manchester_to_int(dat[24:28]) +
                manchester_to_chan(dat[28:30]) +
                manchester_to_mode(dat[30:32])
                )
    except chipcon_usb.ChipconUsbTimeoutException:
        pass
