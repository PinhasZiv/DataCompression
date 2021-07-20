import math
from decimal import Decimal, getcontext

class Aencoder:
    size = 0
    file_str = None
    freq_table = {}
    prob_table = {}
    interval_table = {}
    tag_list = []


    def __init__(self, path):
        self.path = path

    # get the text from the file into a String field 'file_str'.
    def get_file_txt(self):
        with open(self.path, 'rb') as file:
            self.file_str = file.read()
        print(self.file_str)
        self.size = len(self.file_str)

    # initial freq_table by scanning the file_str.
    # initial prob_table by going through the freq_table
    def get_prob_table(self):
        for symbol in self.file_str:
            if symbol in self.freq_table:
                self.freq_table[symbol] += 1
            else:
                self.freq_table[symbol] = 1
        total = sum(list(self.freq_table.values()))
        for key, value in self.freq_table.items():
            self.prob_table[key] = value/total


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

    def scaling(self, low, high, ctr, output):
        if (low >= 0.0) and (high < 0.5):
            low *= 2
            high *= 2
            output += '0'
            output += self.add_c(ctr, '1')
            ctr = 0
            return self.scaling(low, high, ctr, output)
        elif (low >= 0.5) and (high < 1.0):
            low = 2 * low - 1
            high = 2 * high - 1
            output += '1'
            output += self.add_c(ctr, '0')
            ctr = 0
            return self.scaling(low, high, ctr, output)
        elif (low >= 0.25) and (high < 0.75):
            low = 2 * low - 0.5
            high = 2 * high - 0.5
            ctr += 1
            return self.scaling(low, high, ctr, output)
        return low, high, ctr, output

    def fill_num(self, str2, digit):
        size = len(str2)
        while size < 8:
            str2 = str2 + digit
            size = size + 1

        return str2

    def encode_str(self, str1):
        low, high, ctr = 00000000, 99999999, 0
        output = "."

        for symbol in str1:

            low = float(low)
            high = float(high)

            low = int(self.fill_num(str(math.floor(low)), '0'))
            high = int(self.fill_num(str(math.floor(high)), '0'))

            range = high-low + 1
            high = low + self.interval_table[symbol][1]*range
            low = low + self.interval_table[symbol][0]*range

            low = self.fill_num(str(math.floor(low)), '0')

            high = str(math.floor(high))

            while low[0] == high[0]:
                output = output + low[0]
                low = low[1:]+'0'
                high = high[1:]+'9'
            if low[0] != high[0]:
                if low[1] == '9' and high[1] == '0':
                    low = low[0] + low[2:] + '0'
                    high = high[0] + high[2:] + '9'
                    ctr += 1

        if output == '.':
            output += str((int(high) + int(low))/2)
        print(output)