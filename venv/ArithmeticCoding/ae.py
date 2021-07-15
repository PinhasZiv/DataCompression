

class Aencoder:
    size = 0
    file_str = None
    freq_table = {}
    prob_table = {}
    interval_table = {}
    str_list = []
    tag_list = []


    def __init__(self, path, block_size):
        self.path = path
        self.block_size = block_size

    # get the text from the file into a String field 'file_str'. initial block_size
    def get_file_txt(self):
        with open(self.path, 'rb') as file:
            self.file_str = file.read()
        print(self.file_str)
        self.size = len(self.file_str)
        if self.size <= self.block_size:
            self.block_size = self.size

    # convert freq_table into probability table
    def get_prob_table(self):
        for str in self.str_list:
            for symbol in str:
                if symbol in self.freq_table:
                    self.freq_table[symbol] += 1
                else:
                    self.freq_table[symbol] = 1
        total = sum(list(self.freq_table.values()))
        sum1 = 0
        for key, value in self.freq_table.items():
            self.prob_table[key] = value/total


    def get_interval_table(self):
        sum1 = 0
        for key, value in self.prob_table.items():
            current_prob = value
            self.interval_table[key] = (sum1, sum1+current_prob)
            sum1 += current_prob


    # create a list of Strings based on block_size (to make the commpression easier)
    def generate_str_list(self):
        clone_file = self.file_str
        while len(clone_file) >= self.block_size:
            self.str_list.append(clone_file[:self.block_size])
            clone_file = clone_file[self.block_size:]
        self.str_list.append(clone_file)


    def print1(self):
        for item in self.str_list:
            print(item)

    # returns the size of the file
    def get_size(self):
        return self.size

    def add_c(self, i, num):
        str = ""
        while i > 0:
            str += num
            i -= 1
        return str

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

    def encode_file(self):
        for str in self.str_list:
            self.tag_list = self.encode_str(str)



    def encode_str(self, str):
        low, high, ctr = 0, 1, 0
        output = ""
        for char in str:
            range = high-low
            high = low + self.interval_table[char][1]*range
            low = low + self.interval_table[char][0]*range

            low, high, ctr, output = self.scaling(low, high, ctr, output)
        tag = (low+high) / 2
        print("output: ", output)
        return tag

