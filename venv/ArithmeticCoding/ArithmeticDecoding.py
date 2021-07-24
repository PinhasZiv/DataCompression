import math
from decimal import Decimal, getcontext

getcontext().prec = 9999999

class Adecoder:

    interval_table = {}
    change_interval_table = {}

    def __init__(self, path, num, prob, size_str):
        self.path = path
        self.num = num
        self.prob_table = prob
        self.size_str = size_str



    # get the text from the file into a String field 'file_str'.
    def get_file_txt(self):
        with open(self.path, 'rb') as file:
            self.file_str = file.read()
        print(self.file_str)
        self.size = len(self.file_str)

    def get_interval_table(self):
        sum1 = 0
        for key, value in self.prob_table.items():
            current_prob = value
            self.interval_table[key] = [sum1, sum1 + current_prob]
            sum1 += current_prob
        self.change_interval_table = self.interval_table

    def update_change_interval_table(self, low, high):
        hight = int(high) - int(low)
        for key, value in self.change_interval_table.items():
            value[1] = int(low) + self.interval_table[key][1] * hight
            value[0] = int(low) + self.interval_table[key][0] * hight

    def fill_num(self, str_num, digit):
        size = len(str_num)
        while size < 16:
            str_num = str_num + digit
            size = size + 1
        return str_num

    def decode_num(self):
        low, high, ctr = '0000000000000000', '9999999999999999', 0
        rest = None
        if len(self.num) < 16:
            num = self.fill_num(self.num, '0')
        else:
            num = self.num[:16]
            rest = self.num[16:]
        output = ""

        for i in range(self.size_str):
            for symbol, value in self.interval_table.items():
                hight = int(high) - int(low) + 1
                if int(low) + int(num) >= int(low) + value[0]*hight and int(low) + int(num) < int(low) + value[1]*hight:
                    #need to find how should we know which type needed to convert back?
                    output = output + str(symbol)
                    high = str(math.floor(int(low) + value[1] * hight - 1))
                    low = str(math.floor(int(low) + value[0] * hight))
                    num = num[1:]


                    if high[0] == low[0]:
                        high = high[1:]
                        low = low[1:]
                        high = self.fill_num(high, '9')
                        low = self.fill_num(low, '0')
                        while len(num) < 16:
                            if rest != None and len(rest) > 0:
                                num = num + rest[0]
                                rest = rest[1:]
                            else:
                                num = self.fill_num(num, '0')


                    # self.update_change_interval_table(low, high)
                    break

                if low[1] == '9' and high[1] == '0':
                    low = low[0] + low[2:] + '0'
                    high = high[0] + high[2:] + '9'
                    ctr += 1

                    # low = self.fill_num(low, '0')
                    # high = self.fill_num(high, '9')

        print("decompressed file:", output)
        print(len(output))



