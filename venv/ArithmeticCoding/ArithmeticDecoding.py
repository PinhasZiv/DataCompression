import math
from decimal import Decimal, getcontext
import os

getcontext().prec = 20


class Adecoder:

    def __init__(self, in_path, out_path, interval, size_str, num=0):
        self.in_path = in_path
        self.out_path = out_path
        self.num = num
        self.interval_table = interval
        self.size_str = size_str
        self.file_str = ""

    # get the text from the file into a String field 'file_str'.
    def get_file_txt(self):
        with open(self.in_path, 'rb') as file:
            file_size = os.stat(self.in_path).st_size
            for i in range(file_size):
                num = int.from_bytes(file.read(1), "big")
                num2 = num % 16
                num1 = num // 16
                self.file_str += hex(num1)[2] + hex(num2)[2]
        # print(self.file_str)
        self.size = len(self.file_str)

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
                # print("symbol:", symbol, ", high_value:", str(math.floor(int(low) + value[1]*height - 1)), ", low_value:", str(math.floor(int(low) + value[0] * height)),
                #       ", num:", num)

                if int(math.floor(int(low, 16) + self.interval_table[symbol][0] * height)) <= int(num, 16) < int(
                        math.floor(int(low, 16) + self.interval_table[symbol][1] * height - 1)):
                    # if int(num) >= int(math.floor(int(low) + value[0] * height)) and int(str(int(num))[:15] +'0') < int(str(int(math.floor(int(low) + value[1] * height - 1)))[:15]+'1'):

                    output = output + bytearray([symbol])
                    high = hex(math.floor(int(low, 16) + self.interval_table[symbol][1] * height - 1))
                    low = hex(math.floor(int(low, 16) + self.interval_table[symbol][0] * height))

                    # need to find how should we know which type needed to convert back?
                    # print("symbol:", symbol, "high:", high, ", low:", low, ", height:", height, ", num:", num)

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
        out = open(self.out_path, 'wb')
        out.write(output)
        print(len(output))
        out.close()
