from itertools import islice
from typing import List
from dataclasses import dataclass


@dataclass
class Packet:
    version: int
    type: int


@dataclass
class Literal(Packet):
    value: int


@dataclass
class Operator(Packet):
    length_type: int
    length: int
    subpackets: List[Packet]


def hex2bin(s):
    b = bin(int(f"0x{s}", 16))[2:]
    padding = (4 - len(b) % 4) % 4
    return '0' * padding + b


def bin2int(s):
    return int(f"0b{s}", 2)


def take(bits, n):
    return ''.join(islice(bits, n))


def take_int(bits, n):
    if n == 1:
        return int(next(bits))

    b = take(bits, n)
    if not b:  # no more bits
        return -1

    return bin2int(b)


def parse(payload):
    bits = hex2bin(payload)
    return parse_packet(iter(bits))


def parse_packet(bits):
    version = take_int(bits, 3)
    if version == -1:  # no more bits
        return

    type = take_int(bits, 3)

    if type == 4:
        return parse_literal(version, type, bits)

    else:
        return parse_operator(version, type, bits)


def parse_literal(version, type, bits):
    num = []
    more = True

    while more:
        more = take_int(bits, 1)
        num.extend(take(bits, 4))

    value = bin2int("".join(num))

    return Literal(version, type, value)


def parse_operator(version, type, bits):
    length_type = take_int(bits, 1)

    if length_type == 0:
        length = take_int(bits, 15)
        subpackets = parse_all_packets(islice(bits, length))

    else:
        length = take_int(bits, 11)
        subpackets = parse_npackets(bits, length)

    return Operator(
        version, type,
        length_type, length,
        subpackets
    )


def parse_npackets(bits, n):
    subpackets = []
    for _ in range(n):
        packet = parse_packet(bits)
        assert packet is not None
        subpackets.append(packet)
    return subpackets


def parse_all_packets(bits):
    packets = []
    while True:
        packet = parse_packet(bits)
        if packet is None:
            break
        packets.append(packet)
    return packets


def sum_versions(packet):
    total = packet.version
    if isinstance(packet, Operator):
        for sub in packet.subpackets:
            total += sum_versions(sub)
    return total


def load_data(path):
    with open(path, 'r') as f:
        return f.read().strip()


def part1(data):
    packet = parse(data)
    return sum_versions(packet)


def part2(data):
    pass


def main():
    data = load_data('input.txt')
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    main()


class Test:

    def test_parse_literal(self):
        payload = 'D2FE28'
        parsed = parse(payload)
        assert isinstance(parsed, Literal)
        assert parsed.version == 6
        assert parsed.value == 2021

    def test_parse_operator_type0(self):
        payload = '38006F45291200'
        parsed = parse(payload)
        assert isinstance(parsed, Operator)
        assert parsed.version == 1
        assert parsed.type == 6
        assert parsed.length_type == 0
        assert parsed.length == 27
        assert len(parsed.subpackets) == 2
        assert parsed.subpackets[0].value == 10
        assert parsed.subpackets[1].value == 20

    def test_parse_operator_type1(self):
        payload = 'EE00D40C823060'
        parsed = parse(payload)
        assert isinstance(parsed, Operator)
        assert parsed.version == 7
        assert parsed.type == 3
        assert parsed.length_type == 1
        assert parsed.length == 3
        assert len(parsed.subpackets) == 3
        assert parsed.subpackets[0].value == 1
        assert parsed.subpackets[1].value == 2
        assert parsed.subpackets[2].value == 3

    def test_sum_versions(self):
        packet = parse('8A004A801A8002F478')
        assert sum_versions(packet) == 16

    def test_sum_versions2(self):
        packet = parse('620080001611562C8802118E34')
        assert sum_versions(packet) == 12

    def test_sum_versions3(self):
        packet = parse('C0015000016115A2E0802F182340')
        assert sum_versions(packet) == 23

    def test_sum_versions2(self):
        packet = parse('A0016C880162017C3686B18A3D4780')
        assert sum_versions(packet) == 31
