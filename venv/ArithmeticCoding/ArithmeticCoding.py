import math
import collections
from decimal import Decimal, getcontext
import os

'''
Decimal is used to avoid the inaccuracy of a decimal number in 'freq_table'.
Decimal allows us to select the accuracy level of the decimal number
'''
getcontext().prec = 20


class Aencoder:

    def __init__(self, in_path, out_path):
        self.in_path = in_path
        self.size = 0
        self.file_str = None
        self.freq_table = {}
        self.prob_table = {}
        self.interval_table = {}
        self.output_num = None
        self.out_path = out_path

    '''
    get the text from the file into a String field 'file_str'.
    initial field 'size'
    '''
    def get_file_txt(self):
        with open(self.in_path, 'rb') as file:
            self.file_str = file.read()
        self.size = len(self.file_str)

    '''
    Iterate over "file_str" and create the 'freq_table' field
    that stores the number of frequencies of each character in the file
    convert 'freq_table' into 'prob_table',
    a table that stores the probability of each character in the file.
    '''
    def get_prob_table(self):
        for symbol in self.file_str:
            self.freq_table[symbol] = self.freq_table.get(symbol, 0) + 1
        total = sum(list(self.freq_table.values()))
        for key, value in self.freq_table.items():
            self.prob_table[key] = Decimal(Decimal(value) / Decimal(total))

    '''
    Iterate over 'freq_table' and create the 'interval_table' field which stores the interval [0: 1),
    divided into sub-intervals according to the probability of each character in the file.
    '''
    def get_interval_table(self):
        sum1 = 0
        for key, value in self.prob_table.items():
            current_prob = value
            self.interval_table[key] = (sum1, sum1 + current_prob)
            sum1 += current_prob

    '''
    Gets 2 parameters: string and number.
    Checks if the string length is less than 18.
    If it is small - add at the end of the string the digit obtained as a parameter
    until the string is completed to size 16.
    '''
    def fill_num(self, str_num, digit):
        size = len(str_num)
        while size < 18:
            str_num = str_num + digit
            size = size + 1
        return str_num

    '''
    Encrypt the file using arithmetic encoding.
    The coding is performed using a 16-digit integer implementation method,
    based on a hexa decimal base.
    '''
    def encode_str(self):
        low, high, ctr = '0x' + '0' * 16, '0x' + 'f' * 16, 0
        output = "0x"
        save_low, save_high = None, None
        height = int(high, 16) - int(low, 16) + 1

        for symbol in self.file_str:

            high = hex(math.floor(int(low, 16) + self.interval_table[symbol][1] * height) - 1)
            low = hex(math.floor(int(low, 16) + self.interval_table[symbol][0] * height))

            while len(low) < 18:
                low = low[:2] + '0' + low[2:]
            while len(high) < 18:
                high = high[:2] + '0' + high[2:]

            while low[2] == high[2]:
                output = output + low[2]
                while ctr > 0:
                    if low[2] == save_low:
                        output += 'f'
                    else:
                        output += '0'
                    ctr = ctr - 1
                low = low[:2] + low[3:] + '0'
                high = high[:2] + high[3:] + 'f'

            '''
            Performing scaling
            '''
            while int(high[2], 16) - int(low[2], 16) == 1 and (low[3] == 'f' and high[3] == '0'):
                low = low[:3] + low[4:] + '0'
                high = high[:3] + high[4:] + 'f'
                ctr += 1
                save_low = low[2]
                save_high = high[2]

            height = int(high, 16) - int(low, 16) + 1

        if output == "0x":
            output = hex(math.floor((int(high, 16) + int(low, 16)) / 2))
        else:
            add = hex(int((int(high, 16) + int(low, 16)) / 2))[2:4]
            output += add
        self.output_num = output

    '''
    Writing the compressed file that contains:
    Original file size, Freq table size, freq table, The encoded number
    '''
    def write_output_file(self):
        size_hex = hex(self.size)

        with open(self.out_path, "wb") as out:
            num = self.size.to_bytes(4, 'big')
            out.write(num)

            # write the num of symbols in the freq table - 1 byte size
            freq_table_size = len(self.freq_table)
            out.write(freq_table_size.to_bytes(1, 'big'))

            # 5 bytes each symbol - 1 bytes for key, 4 bytes for value.
            for symbol, value in self.freq_table.items():
                out.write(symbol.to_bytes(1, 'big'))
                out.write(value.to_bytes(4, 'big'))

            for i in range(2, len(self.output_num), 2):
                if i == len(self.output_num) -1:
                    num = self.output_num[i] + "0"
                else:
                    num = self.output_num[i:i + 2]

                out.write(bytearray([int(num, 16)]))
