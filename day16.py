from dataclasses import dataclass, field
with open("day16_input.txt") as f:
    hexa = f.read().strip()

def get_bits(stream, count):
    return "".join(next(stream) for _ in range(count))

def get_header(stream):
    return int(get_bits(stream, 3), base=2), int(get_bits(stream, 3), base=2)

def get_literal(stream):
    num_bits = 0
    ret = ""
    while True:
        more = get_bits(stream, 1) == "1"
        ret += get_bits(stream, 4)
        num_bits += 5
        if not more:
            return int(ret, base=2), num_bits

@dataclass
class Packet:
    version: int
    typeid: int
    value: int | None = None
    subpackets: list["Packet"] | None = field(default_factory=list)

def get_packet(stream):
    version, typeid = get_header(stream)
    bits_used = 6
    packet = Packet(version=version, typeid=typeid)

    match typeid:
        case 4:  # Literal value
            value, length = get_literal(stream)
            packet.value = value
            bits_used += length
            return packet, bits_used
        case _:  # Operator
            mode = get_bits(stream, 1)
            bits_used += 1
            match mode:
                case "0":
                    length = int(get_bits(stream, 15), base=2)
                    subpackets = iter(get_bits(stream, length))
                    bits_used += length
                    used = 0
                    while used != length:
                        subpacket, subpacket_size = get_packet(subpackets)
                        packet.subpackets.append(subpacket)
                        used += subpacket_size
                case "1":
                    num_subpackets = int(get_bits(stream, 11), base=2)
                    for _ in range(num_subpackets):
                        subpacket, subpacket_size = get_packet(stream)
                        bits_used += subpacket_size
                        packet.subpackets.append(subpacket)

    return packet, bits_used
            

def process(data):
    stream = iter(bin(int(data, base=16))[2:].zfill(4 * len(data))) # Fill so leading zeroes are not lost
    return get_packet(stream)

x, _ = process("EE00D40C823060")
print(x)