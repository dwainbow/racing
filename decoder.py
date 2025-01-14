from salsa20 import Salsa20_xor 

def salsa20_dec(dat):
    key = b'Simulator Interface Packet GT7 ver 0.0'
    # Seed IV is always located here
    oiv = dat[0x40:0x44]
    iv1 = int.from_bytes(oiv, byteorder='little')
    # Notice DEADBEAF, not DEADBEEF
    iv2 = iv1 ^ 0xDEADBEAF
    iv = bytearray()
    iv.extend(iv2.to_bytes(4, 'little'))
    iv.extend(iv1.to_bytes(4, 'little'))
    ddata = Salsa20_xor(dat, bytes(iv), key[0:32])
    magic = int.from_bytes(ddata[0:4], byteorder='little')
    if magic != 0x47375330:
        return bytearray(b'')
    return ddata