from utils.read_file import read_file, bytes_to_string
from utils.chunks import chunk_list


input_file = "imgs/baboon.png"

if __name__ == '__main__':
    bytes = read_file(input_file)
    for i in range(len(bytes) - 4):
        current_string = bytes_to_string(bytes[i:i+4])
        if current_string in chunk_list:
            print(f'Found {current_string} chunk')
