import math
import json
import collections

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
        print(self.file_str)
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
            self.prob_table[key] = value/total
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

    # def scaling(self, low, high, ctr, output):
    #     if (low >= 0.0) and (high < 0.5):
    #         low *= 2
    #         high *= 2
    #         output += '0'
    #         output += self.add_c(ctr, '1')
    #         ctr = 0
    #         return self.scaling(low, high, ctr, output)
    #     elif (low >= 0.5) and (high < 1.0):
    #         low = 2 * low - 1
    #         high = 2 * high - 1
    #         output += '1'
    #         output += self.add_c(ctr, '0')
    #         ctr = 0
    #         return self.scaling(low, high, ctr, output)
    #     elif (low >= 0.25) and (high < 0.75):
    #         low = 2 * low - 0.5
    #         high = 2 * high - 0.5
    #         ctr += 1
    #         return self.scaling(low, high, ctr, output)
    #     return low, high, ctr, output

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

        for symbol in str1:
            hight = int(high)-int(low)+1
            high = str(math.floor(int(low) + self.interval_table[symbol][1]*hight)-1)
            low = str(math.floor(int(low) + self.interval_table[symbol][0]*hight))

            low = self.fill_num(low, '0')
            high = self.fill_num(high, '9')

            while low[0] == high[0]:
                output = output + low[0]
                while ctr > 0:
                    if low[0] == save_low:
                        output += '0'
                    else:
                        output += '1'
                    ctr = ctr - 1
                low = low[1:]+'0'
                high = high[1:]+'9'

            if low[1] == '9' and high[1] == '0':
                low = low[0] + low[2:] + '0'
                high = high[0] + high[2:] + '9'
                ctr += 1
                save_low = low[0]
                save_high = high[0]

            low = self.fill_num(low, '0')
            high = self.fill_num(high, '9')

        if output == "":
            output += str(math.floor((int(high) + int(low))/2))
        else:
            output += low[:2]
        self.output_num = output
        print("output_num:", output)
        print("output_size:", len(output))

    def output_file(self, path):
        with open(path, 'a') as file:
            file.write(json.dumps(self.prob_table))
            file.write(str(self.size))
            file.write(self.output_num)