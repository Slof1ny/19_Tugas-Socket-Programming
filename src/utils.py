from os import name, system

def clear():
    
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def is_number(num: str) -> bool:
    isNumber = True
    
    for char in num:
        if ord(char) > ord('9') or ord(char) < ord('0'):
            isNumber = False

    return isNumber

def to_lowercase(text: str) -> str:
    temp = ""
    for char in text:
        if ord("A") <= ord(char) <= ord("Z"):
            temp += chr(ord(char) + (ord("a") - ord("A")))
        else:
            temp += char
    return temp

def dict_copy(original_dict: dict[str, str]) -> dict[str,str]:
    new_dict = {}
    for key, value in original_dict.items():
        new_dict[key] = value
    return new_dict

def list_copy(original_list: list[str]) -> list[str]:
    new_list = [item for item in original_list]

    return new_list


if __name__ == "__main__":
    print(to_lowercase("aku adaLah SeOraNg-_ aGent pemBASmi MonsTer AaZzz"))