from rflib import *

collar_addr = b'\x8e\x8e\x8e\x8e\x8e\x8e\x8e\x8e' # 0101010101010101

collar_val0 = b'\x88\x88\x88\x88' # 00000000
collar_val1 = b'\x88\x88\xee\xe8' # 00001110
collar_val2 = b'\x88\x8e\xee\x88' # 00011100
collar_val3 = b'\x88\xe8\xe8\xe8' # 00101010
collar_val4 = b'\x88\xee\xe8\x88' # 00111000
collar_val5 = b'\x8e\x88\x8e\xe8' # 01000110
collar_val6 = b'\x8e\x8e\x8e\x88' # 01010100
collar_val7 = b'\x8e\xe8\x88\xe8' # 01100010

collar_shock   = b'\x88\x8e' # 0001
collar_vibrate = b'\x88\xe8' # 0010
collar_beep    = b'\x8e\x88' # 0100
collar_auto    = b'\x8e\x8e' # 0101

collar_chan1   = b'\xe8\x88' # 1000
collar_chan2   = b'\xee\xee' # 1111

collar_sync = b'\x01\xf8' # 000111111000
collar_end  = b'\xe0'     # 1000

def select_value(val):
    if val == 0:
        return collar_val0
    elif val == 1:
        return collar_val1
    elif val == 2:
        return collar_val2
    elif val == 3:
        return collar_val3
    elif val == 4:
        return collar_val4
    elif val == 5:
        return collar_val5
    elif val == 6:
        return collar_val6
    elif val == 7:
        return collar_val7
    else:
        return bytearray()

def make_message(ch, cmd, v1, v2, v3, v4):
    message = collar_sync

    str = bytearray()

    if ch == 1:
        str += collar_chan1
    elif ch == 2:
        str += collar_chan2
    else:
        return bytearray()

    if cmd == 1:
        str += collar_beep
    elif cmd == 2:
        str += collar_vibrate
    elif cmd == 3:
        str += collar_shock
    elif cmd == 4:
        str += collar_auto
    else:
        return bytearray()

    message += str
    message += collar_addr
    message += select_value(v1)
    message += select_value(v2)
    message += select_value(v3)
    message += select_value(v4)
    message += str
    message += collar_end
    
    return message

d = RfCat()
d.setFreq(434000000)
d.setMdmSyncWord(0xfc)
d.setMdmModulation(MOD_ASK_OOK)
d.setMdmDRate(3550)
d.makePktFLEN(8)
d.setMaxPower()

msg = make_message(1,2,7,7,3,7)

d.RFxmit(msg)
d.RFxmit(msg)
