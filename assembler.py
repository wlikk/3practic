import sys
import csv

OPCODES = {
    "load": 42,
    "read": 56,
    "write": 57,
    "abs": 47
}


def parse_instruction(row):
    op = row[0].strip().lower()
    args = [arg.strip() for arg in row[1:]]
    return op, args


def encode_load(const):
    a = 42
    b = int(const)
    word = (a & 0x3F) | ((b & 0x7FFFFF) << 6)
    return word.to_bytes(4, byteorder='little')


def encode_read(addr):
    a = 56
    b = int(addr)
    word = (a & 0x3F) | ((b & 0x1FFFF) << 6)
    return word.to_bytes(4, byteorder='little')


def encode_write(addr):
    a = 57
    b = int(addr)
    word = (a & 0x3F) | ((b & 0x1FFFF) << 6)
    return word.to_bytes(4, byteorder='little')


def encode_abs(offset):
    a = 47
    b = int(offset)
    word = (a & 0x3F) | ((b & 0x7F) << 6)
    return word.to_bytes(4, byteorder='little')


def run_tests():
    """Проверка тестов из спецификации"""
    test_cases = [
        ("load", ["846"], "0xAA 0xD3 0x00 0x00"),
        ("read", ["554"], "0xB8 0x8A 0x00 0x00"),
        ("write", ["921"], "0x79 0xE6 0x00 0x00"),
        ("abs", ["34"], "0xAF 0x08 0x00 0x00"),
    ]
    for op, args, expected in test_cases:
        if op == "load":
            b = encode_load(args[0])
        elif op == "read":
            b = encode_read(args[0])
        elif op == "write":
            b = encode_write(args[0])
        elif op == "abs":
            b = encode_abs(args[0])
        got = ' '.join([f'0x{b:02X}' for b in b])
        if got == expected:
            print(f"✓ {op} {args}: OK")
        else:
            print(f"✗ {op} {args}: got {got}, expected {expected}")


def assemble_csv(input_path, output_path, test_mode=False):
    with open(input_path, 'r', newline='') as f:
        reader = csv.reader(f, skipinitialspace=True)
        instructions = []
        for row in reader:
            if not row or row[0].startswith('#'):
                continue
            instructions.append(parse_instruction(row))

    binary = bytearray()
    for op, args in instructions:
        if op == "load":
            binary.extend(encode_load(args[0]))
        elif op == "read":
            binary.extend(encode_read(args[0]))
        elif op == "write":
            binary.extend(encode_write(args[0]))
        elif op == "abs":
            binary.extend(encode_abs(args[0]))
        else:
            raise ValueError(f"Unknown opcode: {op}")

    if test_mode:
        for i in range(0, len(binary), 4):
            chunk = binary[i:i + 4]
            print(' '.join([f'0x{b:02X}' for b in chunk]))
    else:
        with open(output_path, 'wb') as f:
            f.write(binary)


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--test":
        run_tests()
        return

    if len(sys.argv) < 4:
        print("Usage:")
        print("  python assembler.py --test  # запуск тестов")
        print("  python assembler.py <input.csv> <output.bin> <test_mode: 0/1>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    test_mode = sys.argv[3] == "1"
    assemble_csv(input_file, output_file, test_mode)


if __name__ == "__main__":
    main()