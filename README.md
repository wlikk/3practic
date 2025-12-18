# Конфигурационное управление. Вариант 9

## Запуск этапов

### Требования
- Python 3.6 или выше
- Установленные стандартные библиотеки (csv, struct, xml.etree.ElementTree)

### Этап 1: Ассемблер
**Проверка встроенных тестов из спецификации:**
```
python assembler.py --test
```
Ожидаемый вывод: 4 теста с пометкой OK.

**Проверка тестов из файла tests.csv:**
```
python assembler.py tests.csv tests_output.bin 1
```
Выведет байты команд. Должно совпасть с:
- load,846 → 0xAA 0xD3 0x00 0x00
- read,554 → 0xB8 0x8A 0x00 0x00
- write,921 → 0x79 0xE6 0x00 0x00
- abs,34 → 0xAF 0x08 0x00 0x00

**Ассемблирование своей программы:**
```
python assembler.py program.csv program.bin 0
```
Создаст бинарный файл program.bin.

### Этап 2: Интерпретатор и память
**Сборка тестовой программы (копирование массива):**
```
python assembler.py array_copy.csv array_copy.bin 0
```

**Запуск интерпретатора:**
```
python vm.py array_copy.bin dump.xml 0 3000
```

**Проверка результата:**
Откройте файл dump.xml и убедитесь, что:
- Адреса 1000-1004 содержат значения 10,20,30,40,50
- Адреса 2000-2004 содержат те же значения (копирование успешно)

### Этап 3: Команда abs() (АЛУ)
**Сборка тестовой программы для abs():**
```
python assembler.py test_abs.csv test_abs.bin 0
```

**Запуск интерпретатора:**
```
python vm.py test_abs.bin dump_abs.xml 0 700
```

**Проверка результата:**
Откройте файл dump_abs.xml и убедитесь, что:
- Адрес 600 содержит 5 (abs от -5)
- Адрес 601 содержит 10 (abs от 10)
- Адрес 602 содержит 15 (abs от -15)

## Краткая демонстрация всех этапов
```bash
# Этап 1
python assembler.py --test
python assembler.py tests.csv test.bin 1

# Этап 2
python assembler.py array_copy.csv array_copy.bin 0
python vm.py array_copy.bin dump.xml 0 3000

# Этап 3
python assembler.py test_abs.csv test_abs.bin 0
python vm.py test_abs.bin dump_abs.xml 0 700
```

## Описание файлов
- assembler.py - ассемблер (этап 1)
- vm.py - интерпретатор (этапы 2-3)
- program.csv - пример программы
- tests.csv - тесты из спецификации УВМ
- array_copy.csv - тест копирования массива (этап 2)
- test_abs.csv - тест команды abs() (этап 3)
- *.bin - скомпилированные программы
- *.xml - дампы памяти после выполнения