from ArithmeticCoding.ae import Aencoder


path = "C:\\Users\פינחס זיו\PycharmProjects\DataCompression\\venv\ArithmeticCoding\\newFile.txt"

x1 = Aencoder(path, 100)

x1.get_file_txt()
print(x1.get_size())
x1.generate_str_list()
x1.get_prob_table()
x1.get_interval_table()

x1.print1()
x1.encode_file()
