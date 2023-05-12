from png import png_image


if __name__ == '__main__':
    input_file = "imgs/baboon.png"
    image = png_image.PNG(input_file)
    image.process_chunks()
    image.display_chunk("iTXt")