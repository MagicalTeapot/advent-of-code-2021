from dataclasses import dataclass, field
from pprint import pprint
from math import prod

def to_int(string):
    return int(string, base=2)

class StreamReader:
    def __init__(self, data):
        self.stream = iter(data)
        self.bits_read = 0
        self.size = len(data)

    def __iter__(self):
        while self.bits_read < self.size:
            yield self.get_packet()

    def get_bits(self, count):
        self.bits_read += count
        return "".join(next(self.stream) for _ in range(count))

    def get_literal(self):
        ret = ""
        while True:
            more = self.get_bits(1) == "1"
            ret += self.get_bits(4)
            if not more:
                return to_int(ret)

    def get_packet(self):
        packet = Packet(
            version=to_int(self.get_bits(3)), typeid=to_int(self.get_bits(3))
        )
        
        if packet.typeid == 4:
            packet.value = self.get_literal()
            return packet

        if self.get_bits(1) == "0":
            length = to_int(self.get_bits(15))
            substream = StreamReader(self.get_bits(length))
            packet.subpackets = list(substream)
        else:
            num_subpackets = to_int(self.get_bits(11))
            packet.subpackets = [self.get_packet() for _ in range(num_subpackets)]

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

        return packet

@dataclass
class Packet:
    version: int
    typeid: int
    value: int | None = None
    subpackets: list["Packet"] = field(default_factory=list)
            
def parse(data):
    stream = bin(int(data, base=16))[2:].zfill(4 * len(data)) # Fill so leading zeroes are not lost
    return StreamReader(stream).get_packet()

def version_sum(root: Packet):
    return root.version + sum(version_sum(node) for node in root.subpackets)

with open("day16_input.txt") as f:
    data = parse(f.read().strip())

print("Part 1:", version_sum(data))
print("Part 2:", data.value)