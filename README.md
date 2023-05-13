# PNG Dissection

## About the project

### Main goals
 - Create an app which will decode information from the header of the PNG file.
 - Visualize the file's attributes (such as the size, colour depth, sampling frequency) and the file itself.
 - Display a graph of the file transformed using Fourier Transform.
 - Suggest the way of testing the correctness of the transformation.
 - Implement the option to delete all unnecessary data to anonymise the file without interfering with the image.

### Additional extensions
- TODO

## Possible places to hide information
 - In the IDAT chunk choice of filters is arbitrary. Because in the standard filtering mode (= 0)
   the number of possible filtering functions is equal to 5, there are 5 possible values to store
   at the beginning of each scanline of the uncompressed image.