from dataclasses import dataclass, field

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
        num_bits = 0
        ret = ""
        while True:
            more = self.get_bits(1) == "1"
            ret += self.get_bits(4)
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
    reader = StreamReader(stream)
    version, typeid = reader.get_header()
    packet = Packet(version=version, typeid=typeid)

    if typeid == 4:
        value, length = reader.get_literal()
        packet.value = value
    else:
        mode = reader.get_bits(1)
        match mode:
            case "0":
                packet.length_type = 0
                length = int(reader.get_bits(15), base=2)
                substream = iter(reader.get_bits(length))
                used = 0
                while used != length:
                    sub_packet, sub_bits_used = get_packet(substream)
                    packet.subpackets.append(sub_packet)
                    used += sub_bits_used
            case "1":
                packet.length_type = 1
                num_subpackets = int(reader.get_bits(11), base=2)
                for _ in range(num_subpackets):
                    sub_packet, sub_bits_used = get_packet(stream)
                    reader.bits_read += sub_bits_used
                    packet.subpackets.append(sub_packet)

    return packet, reader.bits_read
            
def parse(data):
    stream = iter(bin(int(data, base=16))[2:].zfill(4 * len(data))) # Fill so leading zeroes are not lost
    return get_packet(stream)[0]


with open("day16_input.txt") as f:
    data = parse(f.read().strip())

def version_sum(root: Packet):
    return root.version + sum(version_sum(node) for node in root.subpackets)

print("Part 1:", version_sum(data))