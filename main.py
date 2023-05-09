from png import png_image


input_file = "imgs/baboon.png"

if __name__ == '__main__':
    image = png_image.PNG(input_file)
    image.find_chunks()
