import numpy as np
import os


def channelsToOne(red, green, blue):
    r = np.base_repr(red, 2)
    r = r + '0000000000000000'
    r = int(r, base=2)

    g = np.base_repr(green, 2)
    g = g + '00000000'
    g = int(g, base=2)

    b = blue
    return 16777216 - (r + g + b)


def shiftChannels(red, green, blue, shift_num):
    num = channelsToOne(red, green, blue)
    num = 16777216 - num
    s = np.base_repr(num, base=2, padding=24)

    b = s[-8:]
    b = int(b, base=2)

    g = s[-16:-8]
    g = int(g, base=2)

    r = s[:-16]
    r = int(r, base=2)

    b += shift_num

    if b > 255:
        g = g + b - 255
        b = 0
        if g > 255:
            r = r + g - 255
            g = 0
            if r > 255:
                r = 0
    return r, g, b


def flattenImageAndShift (image, item, shift_value):
    width = image.shape[0]
    height = image.shape[1]
    image = image.reshape((width * height, 3))
    r = image[item, 0]
    g = image[item, 1]
    b = image[item, 2]

    red, green, blue = shiftChannels(r, g, b, shift_value)
    image[item, 0] = red
    image[item, 1] = green
    image[item, 2] = blue


def save_time(file_name, t1, t2, out_file):
    mode = 'w'
    if os.path.exists(out_file):
        mode = 'a'
    with open(out_file, mode) as f:
        f.write(file_name + ' - ' + str(t2 - t1) + '\n')