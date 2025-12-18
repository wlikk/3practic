import sys
import struct
import xml.etree.ElementTree as ET


class UVM:
    def __init__(self, mem_size=65536):
        self.memory = [0] * mem_size  # объединённая память команд и данных
        self.stack = []
        self.pc = 0  # программный счётчик
        self.code_size = 0  # размер загруженного кода

    def load_binary(self, filepath):
        with open(filepath, 'rb') as f:
            data = f.read()
        self.code_size = len(data)  # запоминаем размер загруженного кода
        for i, byte in enumerate(data):
            if i < len(self.memory):
                self.memory[i] = byte
        print(f"Загружено {len(data)} байт из {filepath}")

    def fetch_instruction(self):
        # Останавливаемся, когда дошли до конца загруженного кода
        if self.pc >= self.code_size:
            return None
        if self.pc + 4 > len(self.memory):
            return None
        word = struct.unpack('<I', bytes(self.memory[self.pc:self.pc + 4]))[0]
        self.pc += 4
        return word

    def decode_execute(self, word):
        op = word & 0x3F  # младшие 6 бит — код операции

        # Игнорируем нулевую команду (пустые байты в конце файла)
        if op == 0:
            return

        if op == 42:  # load
            const = (word >> 6) & 0x7FFFFF  # 23 бита
            self.stack.append(const)
            print(f"LOAD const={const}, stack={self.stack}")
        elif op == 56:  # read
            addr = (word >> 6) & 0x1FFFF  # 19 бит
            if addr < len(self.memory):
                value = self.memory[addr]
                self.stack.append(value)
                print(f"READ addr={addr}, value={value}, stack={self.stack}")
            else:
                print(f"ОШИБКА: Адрес {addr} вне памяти")
        elif op == 57:  # write
            addr = (word >> 6) & 0x1FFFF
            if self.stack:
                value = self.stack.pop()
                if addr < len(self.memory):
                    self.memory[addr] = value & 0xFF
                    print(f"WRITE addr={addr}, value={value}")
                else:
                    print(f"ОШИБКА: Адрес {addr} вне памяти")
            else:
                print("ОШИБКА: Стек пуст при WRITE")
        elif op == 47:  # abs (РЕАЛИЗОВАНО В ЭТАПЕ 3)
            offset = (word >> 6) & 0x7F  # 7 бит смещения
            if self.stack:
                addr = self.stack.pop()
                eff_addr = addr + offset
                if 0 <= eff_addr < len(self.memory):
                    # Читаем значение как знаковое 8-битное
                    value = self.memory[eff_addr]
                    if value > 127:  # отрицательное в дополнении до двух
                        value = value - 256
                    abs_value = abs(value)
                    self.stack.append(abs_value)
                    print(f"ABS addr={addr}+{offset}={eff_addr}, value={value}, abs={abs_value}, stack={self.stack}")
                else:
                    print(f"ОШИБКА: Адрес {eff_addr} вне памяти")
            else:
                print("ОШИБКА: Стек пуст при ABS")
        else:
            print(f"ОШИБКА: Неизвестный код операции {op}")

    def run(self):
        print("Запуск выполнения...")
        while True:
            instr = self.fetch_instruction()
            if instr is None:
                break
            self.decode_execute(instr)
        print("Выполнение завершено.")

    def dump_memory_xml(self, filepath, start_addr, end_addr):
        root = ET.Element("memory_dump")
        root.set("start", str(start_addr))
        root.set("end", str(end_addr))
        for addr in range(start_addr, min(end_addr + 1, len(self.memory))):
            elem = ET.SubElement(root, "cell")
            elem.set("address", str(addr))
            elem.set("value", str(self.memory[addr]))
        tree = ET.ElementTree(root)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
        print(f"Дамп памяти сохранён в {filepath} (адреса {start_addr}-{end_addr})")


def main():
    if len(sys.argv) != 5:
        print("Использование: vm.py <binary_file> <dump.xml> <start_addr> <end_addr>")
        print("Пример: vm.py program.bin dump.xml 0 100")
        return
    binary_file = sys.argv[1]
    dump_file = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])

    uvm = UVM()
    uvm.load_binary(binary_file)
    uvm.run()
    uvm.dump_memory_xml(dump_file, start, end)


if __name__ == "__main__":
    main()
