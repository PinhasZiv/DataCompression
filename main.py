from ArithmeticCoding.ae import Aencoder


path = "C:\\Users\פינחס זיו\PycharmProjects\DataCompression\\venv\ArithmeticCoding\\newFile.txt"

x1 = Aencoder(path)

x1.get_file_txt()
print(x1.get_size())
x1.get_prob_table()
x1.get_interval_table()
x1.encode_str(x1.file_str)
