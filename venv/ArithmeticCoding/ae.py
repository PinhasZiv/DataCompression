

class Aencoder:
    size = 0
    file_str = None
    prob_table = {}
    str_list = []
    tag_list = []


    def __init__(self, path, freq_table, block_size):
        self.path = path
        self.freq_table = freq_table
        self.block_size = block_size

    # get the text from the file into a String field 'file_str'. initial block_size
    def get_file_txt(self):
        with open(self.path) as file:
            self.file_str = file.read()
        print(self.file_str)
        self.size = len(self.file_str)
        if self.size <= self.block_size:
            self.block_size = self.size

    # convert freq_table into probability table
    def get_prob_table(self):
        total = sum(list(self.freq_table.values()))
        sum1 = 0
        for key, value in self.freq_table.items():
            self.prob_table[key] = [value/total, sum1]
            sum1 += self.prob_table[key][0]

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

    def scaling(self, left, right, ctr):
        if (left >= 0.0) & (right < 0.5):
            left *= 2
            right *= 2
            output += '0'
            output += self.add_c(ctr, '1')
            ctr = 0
            return self.scaling(left, right, ctr)
        elif (left >= 0.5) & (right < 1.0):
            left = 2 * left - 1
            right = 2 * right - 1
            output += '1'
            output += self.add_c(ctr, '0')
            ctr = 0
            return self.scaling(left, right, ctr)
        elif (left >= 0.25) & (right < 0.75):
            left = 2 * left - 0.5
            right = 2 * right - 0.5
            ctr += 1
            return self.scaling(left, right, ctr)
        return left, right, ctr

    def encode_str(self, str):
        left, right, ctr = 0, 1, 0
        output = ""
        for char in str:
            w = right-left
            left = left + w*self.prob_table[char][1]
            right = left + w*self.prob_table[char][0]
            left, right, ctr = self.scaling(left, right, ctr)
            # if (left >= 0.0) & (right < 0.5):
            #     left *= 2
            #     right *= 2
            #     output += '0'
            #     output += self.add_c(ctr, '1')
            #     ctr = 0
            # elif (left >= 0.5) & (right < 1.0):
            #     left = 2*left - 1
            #     right = 2*right - 1
            #     output += '1'
            #     output += self.add_c(ctr, '0')
            #     ctr = 0
            # elif (left >= 0.25) & (right < 0.75):
            #     left = 2*left - 0.5
            #     right = 2*right - 0.5
            #     ctr += 1
        tag = (left+right) / 2
        print(tag)
        print(output)

