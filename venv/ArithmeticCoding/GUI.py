import os.path
from tkinter import *
from tkinter import filedialog
from ArithmeticCoding import Aencoder
from ArithmeticDecoding import Adecoder

root = Tk()
root.title("Arithmetic Compression")

def browseFiles():
    global file_path
    global out
    file_path = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))

    # out = head + "/CompressedFile.txt"
    out = file_path + ".ae"
    head, tail = os.path.split(out)
    print("head:", head, " ,tail:", tail)
    button_compress.config(state=NORMAL)
    return file_path, out

def compress_file():
    compress(file_path, out)


compression_label = Label(root, text="Compression", fg="blue", width = 60)
compression_label.grid(row=0, column=1)

button_explore = Button(root,
                        text = "Browse Files",
                        command = browseFiles)
button_explore.grid(column=1, row=2)

button_compress = Button(root,
                        text = "Compress",
                        command = compress_file,
                        state=DISABLED)
button_compress.grid(column=1, row=3)




def browseFilesToDecompress():
    global file_path
    global out
    out = ""
    file_path = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
    compressed = file_path[len(file_path) - 3:]
    if compressed == '.ae':
        out = file_path[:len(file_path) - 3]
        head, tail = os.path.split(out)
        out = head + "/Decompressed_" + tail
        button_decompress.config(state=NORMAL)
        messages_label.config(text="")
    else:
        messages_label.config(text="This file is not compressed.\nPlease select a file with the extension '.ae'")
        # button_decompress.config(state=DISABLED)

    return file_path, out

def decompress_file():
        decompress(file_path, out)
        messages_label.config(text="Decompressed successfully")



decompression_label = Label(root, text="Decompression", fg="purple", width=60)
decompression_label.grid(row=0, column=0)


button_choose_to_decompress = Button(root,
                        text = "Browse file",
                        command = browseFilesToDecompress)
button_choose_to_decompress.grid(row=2, column=0)

button_decompress = Button(root,
                        text = "Decompress",
                        command = decompress_file,
                        state=DISABLED)
button_decompress.grid(row=3, column=0)

messages_label = Label(root, text="", fg="red", width=50)
messages_label.grid(row=4, column=0)

def compress(in_path, out_path):
    x1 = Aencoder(in_path, out_path)
    x1.get_file_txt()
    x1.get_prob_table()
    x1.get_interval_table()
    x1.encode_str()
    x1.write_output_file()

def decompress(old_path, out_path):
    x2 = Adecoder(old_path, out_path)
    x2.get_file_txt()
    x2.decode_num()


root.mainloop()