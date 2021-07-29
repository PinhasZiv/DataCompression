import math
from decimal import Decimal, getcontext

getcontext().prec = 20

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
        # print(self.file_str)
        self.size = len(self.file_str)

    def get_interval_table(self):
        sum1 = 0
        for key, value in self.prob_table.items():
            current_prob = value
            self.interval_table[key] = [sum1, sum1 + current_prob]
            sum1 += current_prob
        self.change_interval_table = self.interval_table

    def fill_num(self, str_num, digit):
        size = len(str_num)
        while size < 16:
            str_num = str_num + digit
            size = size + 1
        return str_num

    def decode_num(self):
        low, high, ctr = '0000000000000000', '9999999999999999', 0
        rest = 0
        if len(self.num) <= 16:
            num = self.fill_num(self.num, '0')
        else:
            num = self.num[:16]
            rest = self.num[16:]
        output = ""
        hight = int(high) - int(low) + 1
        for i in range(self.size_str):
            for symbol, value in self.interval_table.items():
                # print("symbol:", symbol, ", high_value:", str(math.floor(int(low) + value[1]*hight - 1)), ", low_value:", str(math.floor(int(low) + value[0] * hight)),
                #       ", num:", num)


                if int(num) >= int(math.floor(int(low) + value[0] * hight)) and int(num) < int(math.floor(int(low) + value[1] * hight - 1)):
                #if int(num) >= int(math.floor(int(low) + value[0] * hight)) and int(str(int(num))[:15] +'0') < int(str(int(math.floor(int(low) + value[1] * hight - 1)))[:15]+'1'):

                    output = output + chr(symbol)
                    high = str(math.floor(int(low) + value[1] * hight - 1))
                    low = str(math.floor(int(low) + value[0] * hight))

                    # need to find how should we know which type needed to convert back?
                    # print("symbol:", symbol, "high:", high, ", low:", low, ", hight:", hight, ", num:", num)

                    while len(low) < 16:
                        low = '0' + low
                    while len(high) < 16:
                        high = '0' + high

                    while high[0] == low[0]:
                        num = num[1:]
                        high = high[1:]
                        low = low[1:]
                        high = high + '9'
                        low = low + '0'
                        if rest != 0 and len(rest) > 0:
                            num = num + rest[0]
                            rest = rest[1:]
                        else:
                            num = num + '0'


                    # need to check how to recover this if stetment
                    while int(high[0]) - int(low[0]) == 1 and (low[1] == '9' and high[1] == '0'):
                        # if low[1] == '9' and high[1] == '0':
                        #     print("before scaling:", "high:", high, ", low:", low, )
                            low = low[0] + low[2:] + '0'
                            high = high[0] + high[2:] + '9'
                            num = num[0] + num[2:]
                            if rest != 0 and len(rest) > 0:
                                num = num + rest[0]
                                rest = rest[1:]
                            else:
                                num = num + '0'
                            # print("after scaling:", "high:", high, ", low:", low, )

                    hight = int(high) - int(low) + 1
                    break



        print("decompressed file:", output)
        print(len(output))



