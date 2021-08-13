import os.path
from tkinter import *
from tkinter import filedialog
from ArithmeticCoding import Aencoder
from ArithmeticDecoding import Adecoder

'''
Initialize the GUI window
'''
root = Tk()
root.title("Arithmetic Compression")

'''
Opens a window for selecting files from computer memory
'''
def browseFilesToCompress():
    global file_path
    global out
    file_path = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))

    out = file_path + ".ae"
    head, tail = os.path.split(out)
    button_compress.config(state=NORMAL)
    return file_path, out

'''
Perform the compression process on the selected file.
'''
def compress_file():
    compress(file_path, out)
    messages_label_compress.config(text="compressed successfully")

'''
Initialize a label to compress part and place the label in the GUI window.
'''
compression_label = Label(root, text="Compression", fg="blue", width = 60)
compression_label.grid(row=0, column=1)

'''
Initialize button for selecting a document and placing it in the GUI window.
'''
button_explore = Button(root,
                        text = "Browse Files",
                        command = browseFilesToCompress)
button_explore.grid(column=1, row=2)

'''
Initialize a button to compress a document and place it in the GUI window.
'''
button_compress = Button(root,
                        text = "Compress",
                        command = compress_file,
                        state=DISABLED)
button_compress.grid(column=1, row=3)

'''
Initialize a message label and place it in the GUI window.
'''
messages_label_compress = Label(root, text="", fg="orange", width=50)
messages_label_compress.grid(row=4, column=1)

'''
Opens a window for selecting files from computer memory.
Check whether the file to be selected for compression
has the suffix 'ae.' And print a message if not.
'''
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
        messages_label_decompress.config(text="")
    else:
        messages_label_decompress.config(text="This file is not compressed.\nPlease select a file with the extension '.ae'")
        # button_decompress.config(state=DISABLED)

    return file_path, out

'''
Perform the decompression process on the selected file.
'''
def decompress_file():
        decompress(file_path, out)
        messages_label_decompress.config(text="Decompressed successfully")

'''
Initialize a label to decompress part and place the label in the GUI window.
'''
decompression_label = Label(root, text="Decompression", fg="purple", width=60)
decompression_label.grid(row=0, column=0)

'''
Initialize button for selecting a document and placing it in the GUI window.
'''
button_choose_to_decompress = Button(root,
                        text = "Browse file",
                        command = browseFilesToDecompress)
button_choose_to_decompress.grid(row=2, column=0)

'''
Initialize a button to decompress a document and place it in the GUI window.
'''
button_decompress = Button(root,
                        text = "Decompress",
                        command = decompress_file,
                        state=DISABLED)
button_decompress.grid(row=3, column=0)

'''
Initialize a message label and place it in the GUI window.
'''
messages_label_decompress = Label(root, text="", fg="orange", width=50)
messages_label_decompress.grid(row=4, column=0)

'''
Perform the compression process on the selected file.
The compressed file is saved in the location of the original file,
with the same name and the suffix '.ae' extension.
'''
def compress(in_path, out_path):
    x1 = Aencoder(in_path, out_path)
    x1.get_file_txt()
    x1.get_prob_table()
    x1.get_interval_table()
    x1.encode_str()
    x1.write_output_file()

'''
Perform the decompression process on the selected file.
The new file is saved in the location of the original file,
with prefix 'decompressed_'.
'''
def decompress(old_path, out_path):
    x2 = Adecoder(old_path, out_path)
    x2.get_file_txt()
    x2.decode_num()

root.mainloop()