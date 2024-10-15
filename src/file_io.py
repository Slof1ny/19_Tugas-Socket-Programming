import os

if __package__ is None or __package__ == "":
    from utils import is_number
else:
    from .utils import is_number

# Path direktori parent (path folder repositori)
DIR_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def read_csv(folder_name: str, file_name: str) -> list[dict[str, str]]:
    """
    Membaca data dari file csv yang ditentukan dan mengembalikannya sebagai list dari dictionary.
    """
    file_path = f"{DIR_PATH}/data/{folder_name}/{file_name}"
    
    lines = []
    with open(file_path, "r") as f:
        for line in f:
            lines.append(line)
    
    parsed_lines = _parse(lines)
    keys = parsed_lines[0]
    formatted_data = []

    for i in range(1, len(parsed_lines)):
        data = {}
        for j in range(len(parsed_lines[i])):
            data[keys[j]] = parsed_lines[i][j]
        formatted_data.append(data)
    
    return formatted_data

def write_csv(folder_name:str, file_name: str, data: list[dict[str, str]]):
    """
    Menulis data ke file csv yang ditentukan.
    """
    file_path = f"{DIR_PATH}/data/{folder_name}/{file_name}"
    
    keys = []
    for key in data[0]:
        keys.append(key)
    data_csv = []
    data_csv.append(_to_csv(keys))
    
    for i in range(len(data)):
        data_csv.append(_to_csv([data[i][key] for key in keys]))

    with open(file_path, 'w') as f:
        for i in range(len(data_csv)):
            f.write(data_csv[i])

def get_folders(directory: str):
    folders = []
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            folders.append(item)
    return folders

def _parse(lines: list[str]) -> list[list[str]]:
    """
    Melakukan parsing string csv dan mengembalikan list dari list data per baris.
    """
    parsed_lines = []
    parsed_words = []
    temp = ""

    for line in lines:
        for char in line:
            if char == ',':
                if is_number(temp):
                    parsed_words.append(int(temp))
                else:
                    parsed_words.append(temp)
                temp = ""
            elif char == '\n':
                if is_number(temp):
                    parsed_words.append(int(temp))
                else:
                    parsed_words.append(temp)
                parsed_lines.append(parsed_words)
                parsed_words = []
                temp = ""
            else:
                temp += char

    if temp:
        if is_number(temp):
            parsed_words.append(int(temp)) #just so i can avoid changing temp from str to int
        else:
            parsed_words.append(temp)

    if parsed_words:
        parsed_lines.append(parsed_words)

    return parsed_lines

def _to_csv(data: list[str]) -> str:
    """
    Mengubah list dari string menjadi string dengan format csv.
    """
    joined = ""
    for i in range(len(data)):
        joined += str(data[i])
        if i != len(data) - 1:
            joined += ','
        else:
            joined += '\n'

    return joined


if __name__ == "__main__": # Hanya akan dieksekusi jika dijalankan secara langsung dan bukan sebagai modul
    x = read_csv("test_folder", "test.csv")
    write_csv("test_folder", "test123.csv", x)
    print(x)

