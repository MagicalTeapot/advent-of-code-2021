from dataclasses import dataclass, field
from pprint import pprint
from math import prod

class StreamReader:
    def __init__(self, stream):
        self.stream = stream
        self.bits_read = 0

    def get_bits(self, count):
        self.bits_read += count
        return "".join(next(self.stream) for _ in range(count))

    def get_header(self):
        return int(self.get_bits(3), base=2), int(self.get_bits(3), base=2)

    def get_literal(self):
        ret = ""
        while True:
            more = self.get_bits(1) == "1"
            ret += self.get_bits(4)
            if not more:
                return int(ret, base=2)

@dataclass
class Packet:
    version: int
    typeid: int
    value: int | None = None
    subpackets: list["Packet"] = field(default_factory=list)

def get_packet(stream):
    reader = StreamReader(stream)
    version, typeid = reader.get_header()

    if typeid == 4:
        packet = Packet(version=version, typeid=typeid, value=reader.get_literal())
        return packet, reader.bits_read
        
    packet = Packet(version=version, typeid=typeid)
    mode = reader.get_bits(1)
    if mode == "0":
        length = int(reader.get_bits(15), base=2)
        substream = iter(reader.get_bits(length))
        used = 0
        while used != length:
            sub_packet, sub_bits_used = get_packet(substream)
            packet.subpackets.append(sub_packet)
            used += sub_bits_used
    else:
        num_subpackets = int(reader.get_bits(11), base=2)
        for _ in range(num_subpackets):
            sub_packet, sub_bits_used = get_packet(stream)
            reader.bits_read += sub_bits_used
            packet.subpackets.append(sub_packet)

    match packet.typeid:
        case 0:
            packet.value = sum(p.value for p in packet.subpackets)
        case 1:
            packet.value = prod(p.value for p in packet.subpackets)
        case 2:
            packet.value = min(p.value for p in packet.subpackets)
        case 3:
            packet.value = max(p.value for p in packet.subpackets)
        case 5:
            first, second = packet.subpackets
            packet.value = 1 if first.value > second.value else 0
        case 6:
            first, second = packet.subpackets
            packet.value = 1 if first.value < second.value else 0
        case 7:
            first, second = packet.subpackets
            packet.value = 1 if first.value == second.value else 0

    return packet, reader.bits_read
            
def parse(data):
    stream = iter(bin(int(data, base=16))[2:].zfill(4 * len(data))) # Fill so leading zeroes are not lost
    return get_packet(stream)[0]


with open("day16_input.txt") as f:
    data = parse(f.read().strip())
    pprint(data)

def version_sum(root: Packet):
    return root.version + sum(version_sum(node) for node in root.subpackets)

print("Part 1:", version_sum(data))
print("Part 2:", data.value)