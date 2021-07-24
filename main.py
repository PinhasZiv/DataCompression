from ArithmeticCoding.ae import Aencoder
from ArithmeticCoding.ArithmeticDecoding import Adecoder


path = "C:\\Users\פינחס זיו\PycharmProjects\DataCompression\\venv\ArithmeticCoding\\newFile.txt"
new_path = "C:\\Users\פינחס זיו\PycharmProjects\DataCompression\\venv\ArithmeticCoding\\decompressed_file!!.txt"

x1 = Aencoder(path)


x1.get_file_txt()
print(x1.get_size())
x1.get_prob_table()
x1.get_interval_table()

num1 = x1.encode_str(x1.file_str)
x1.output_file("C:\\Users\פינחס זיו\PycharmProjects\DataCompression\\venv\ArithmeticCoding\\compressed_file.txt")

x2 = Adecoder(new_path, x1.output_num, x1.prob_table, x1.size)
x2.get_interval_table()
x2.decode_num()


