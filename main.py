from png import png_image


if __name__ == '__main__':
    input_file = "imgs/parrot_plte.png"
    image = png_image.PNG(input_file)
    image.process_chunks()
    image.display_chunk("IDAT")