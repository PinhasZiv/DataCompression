import math
from decimal import Decimal, getcontext
import os

getcontext().prec = 20


class Adecoder:

    def __init__(self, in_path, out_path):
        self.in_path = in_path
        self.out_path = out_path
        self.size_str = 0
        self.prob_table = {}
        self.interval_table = {}
        self.file_str = ""

    # get the text from the file into a String field 'file_str'.
    def get_file_txt(self):
        with open(self.in_path, 'rb') as file:
            # get size of original file from compressed file.
            size_of_file = int.from_bytes(file.read(4), 'big')
            print("size_of_file:", size_of_file)
            self.size_str = size_of_file

            # get number of items in freq table
            freq_size = int.from_bytes(file.read(1), 'big')
            print("size of freq table: after!!", freq_size)

            # get freq table from compressed file
            freq_table = {}
            for i in range(freq_size):
                symbol = int.from_bytes(file.read(1), 'big')
                num2 = symbol % 16
                num1 = symbol // 16
                val = int.from_bytes(file.read(4), 'big')
                freq_table[symbol] = val

            self.get_prob_table(freq_table)

            compressed_file_size = os.stat(self.in_path).st_size
            for i in range(compressed_file_size):
                num = int.from_bytes(file.read(1), "big")
                num2 = num % 16
                num1 = num // 16
                self.file_str += hex(num1)[2] + hex(num2)[2]
        print(self.file_str)
        self.size = len(self.file_str)

    def get_prob_table(self, freq_table):
        total = sum(list(freq_table.values()))
        for key, value in freq_table.items():
            self.prob_table[key] = Decimal(Decimal(value) / Decimal(total))

        sum1 = 0
        for key, value in self.prob_table.items():
            current_prob = value
            self.interval_table[key] = (sum1, sum1 + current_prob)
            sum1 += current_prob

    def fill_num(self, str_num, digit):
        size = len(str_num)
        while size < 18:
            str_num = str_num + digit
            size = size + 1
        return str_num

    def decode_num(self):
        low, high, ctr = '0x' + '0' * 16, '0x' + 'f' * 16, 0
        rest = 0
        self.num = "0x" + self.file_str
        if len(self.num) <= 18:
            num = self.fill_num(self.num, '0')
        else:
            num = self.num[:18]
            rest = self.num[18:]
        output = bytearray()
        height = int(high, 16) - int(low, 16) + 1
        for i in range(self.size_str):
            for symbol in self.interval_table:

                if int(math.floor(int(low, 16) + self.interval_table[symbol][0] * height)) <= int(num, 16) < int(
                        math.floor(int(low, 16) + self.interval_table[symbol][1] * height - 1)):
                    output = output + bytearray([symbol])
                    high = hex(math.floor(int(low, 16) + self.interval_table[symbol][1] * height - 1))
                    low = hex(math.floor(int(low, 16) + self.interval_table[symbol][0] * height))

                    while len(low) < 18:
                        low = low[:2] + '0' + low[2:]
                    while len(high) < 18:
                        high = high[:2] + '0' + high[2:]

                    while high[2] == low[2]:
                        num = '0x' + num[3:]
                        high = '0x' + high[3:]
                        low = '0x' + low[3:]
                        high = high + 'f'
                        low = low + '0'
                        if rest != 0 and len(rest) > 0:
                            num = '0x' + num[2:] + rest[0]
                            rest = rest[1:]
                        else:
                            num = '0x' + num[2:] + '0'

                    while int(high[2], 16) - int(low[2], 16) == 1 and (low[3] == 'f' and high[3] == '0'):
                        # if low[1] == '9' and high[1] == '0':
                        #     print("before scaling:", "high:", high, ", low:", low, )
                        low = '0x' + low[2] + low[4:] + '0'
                        high = '0x' + high[2] + high[4:] + 'f'
                        num = '0x' + num[2] + num[4:]
                        if rest != 0 and len(rest) > 0:
                            num = '0x' + num[2:] + rest[0]
                            rest = rest[1:]
                        else:
                            num = '0x' + num[2:] + '0'
                        # print("after scaling:", "high:", high, ", low:", low, )

                    height = int(high, 16) - int(low, 16) + 1
                    break

        print("decompressed file:", output)
        with open(self.out_path, 'wb') as out:
            out.write(output)
            print(len(output))
