from dataclasses import dataclass, field

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
    length_type: int | None = None
    subpackets: list["Packet"] | None = field(default_factory=list)

def get_packet(stream):
    version, typeid = get_header(stream)
    bits_used = 6
    packet = Packet(version=version, typeid=typeid)

    if typeid == 4:
        value, length = get_literal(stream)
        packet.value = value
        bits_used += length
    else:
        mode = get_bits(stream, 1)
        bits_used += 1
        match mode:
            case "0":
                packet.length_type = 0
                length = int(get_bits(stream, 15), base=2)
                bits_used += 15
                substream = iter(get_bits(stream, length))
                bits_used += length
                used = 0
                while used != length:
                    sub_packet, sub_bits_used = get_packet(substream)
                    packet.subpackets.append(sub_packet)
                    used += sub_bits_used
            case "1":
                packet.length_type = 1
                num_subpackets = int(get_bits(stream, 11), base=2)
                bits_used += 11
                for _ in range(num_subpackets):
                    sub_packet, sub_bits_used = get_packet(stream)
                    bits_used += sub_bits_used
                    packet.subpackets.append(sub_packet)

    return packet, bits_used
            
def parse(data):
    stream = iter(bin(int(data, base=16))[2:].zfill(4 * len(data))) # Fill so leading zeroes are not lost
    return get_packet(stream)[0]


with open("day16_input.txt") as f:
    data = parse(f.read().strip())

def version_sum(root: Packet):
    return root.version + sum(version_sum(node) for node in root.subpackets)

print("Part 1:", version_sum(data))