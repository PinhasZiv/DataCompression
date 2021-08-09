from ArithmeticCoding.ArithmeticCoding import Aencoder
from ArithmeticCoding.ArithmeticDecoding import Adecoder


path = r"C:\Users\פינחס זיו\Desktop\venv\ArithmeticCoding\rect.bmp"
new_path = r"C:\Users\פינחס זיו\Desktop\venv\ArithmeticCoding\new_file!!.txt"

x1 = Aencoder(path, new_path)


x1.get_file_txt()
# print(x1.get_size())
x1.get_prob_table()
x1.get_interval_table()

num1 = x1.encode_str()
x1.write_output_file(new_path)
# x1.output_file("C:\\Users\פינחס זיו\PycharmProjects\DataCompression\\venv\ArithmeticCoding\\compressed_file.txt")

x2 = Adecoder(new_path, x1.prob_table, x1.size)
x2.get_interval_table()
x2.get_file_txt()
x2.decode_num()
print("finish")

