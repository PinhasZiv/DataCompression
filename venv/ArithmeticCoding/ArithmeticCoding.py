import math
import json
import collections
from decimal import Decimal, getcontext

getcontext().prec = 20

class Aencoder:
    size = 0
    file_str = None
    freq_table = {}
    prob_table = {}
    interval_table = {}
    tag_list = []
    output_num = None


    def __init__(self, path):
        self.path = path

    # get the text from the file into a String field 'file_str'. initial block_size
    def get_file_txt(self):
        with open(self.path, 'rb') as file:
            self.file_str = file.read()
        # print(self.file_str)
        self.size = len(self.file_str)

    # convert freq_table into probability table
    def get_prob_table(self):
        for symbol in self.file_str:
            if symbol in self.freq_table:
                self.freq_table[symbol] += 1
            else:
                self.freq_table[symbol] = 1
        total = sum(list(self.freq_table.values()))
        for key, value in self.freq_table.items():
            self.prob_table[key] = Decimal(Decimal(value)/Decimal(total))
        # sorting the prob_table. not necessary.
        self.prob_table = collections.OrderedDict(sorted(self.prob_table.items()))


    def get_interval_table(self):
        sum1 = 0
        for key, value in self.prob_table.items():
            current_prob = value
            self.interval_table[key] = (sum1, sum1+current_prob)
            sum1 += current_prob


    # returns the size of the file
    def get_size(self):
        return self.size

    def add_c(self, i, num):
        str1 = ""
        while i > 0:
            str1 += num
            i -= 1
        return str1

    def fill_num(self, str_num, digit):
        size = len(str_num)
        while size < 16:
            str_num = str_num + digit
            size = size + 1
        return str_num

    def encode_str(self, str1):
        low, high, ctr = '0000000000000000', '9999999999999999', 0
        output = ""
        save_low, save_high = None, None
        hight = int(high) - int(low) + 1

        for symbol in str1:

            high = str(math.floor(int(low) + self.interval_table[symbol][1]*hight)-1)
            low = str(math.floor(int(low) + self.interval_table[symbol][0]*hight))

            # print("symbol:", symbol, "high:", high, ", low:", low, ", hight:", hight, ", output:", output)

            while len(low) < 16:
                low = '0' + low
            while len(high) < 16:
                high = '0' + high

            while low[0] == high[0]:
                output = output + low[0]
                while ctr > 0:
                    if low[0] == save_low:
                        output += '9'
                    else:
                        output += '0'
                    ctr = ctr - 1
                low = low[1:]+'0'
                high = high[1:]+'9'

            while int(high[0]) - int(low[0]) == 1 and (low[1] == '9' and high[1] == '0'):
                # if low[1] == '9' and high[1] == '0':
                #     print("before scaling:", "high:", high, ", low:", low,)
                    low = low[0] + low[2:] + '0'
                    high = high[0] + high[2:] + '9'
                    ctr += 1
                    save_low = low[0]
                    save_high = high[0]
                    # print("DO SCALING")
                    # print("after scaling:", "high:", high, ", low:", low, )

            low = self.fill_num(low, '0')
            high = self.fill_num(high, '9')
            hight = int(high) - int(low) + 1

        if output == "":
            output += str(math.floor((int(high) + int(low))/2))
        else:
            add = str((int(high) + int(low)) / 2)[:2]
            output += add
        self.output_num = output
        # print("output_num:", output)
        # print("output_size:", len(output))

    def output_file(self, path):
        with open(path, 'a') as file:
            file.write(json.dumps(self.prob_table))
            file.write(str(self.size))
            file.write(self.output_num)