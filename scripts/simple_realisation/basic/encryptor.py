import argparse
from PIL import Image
from utils import channelsToOne, shiftChannels, flattenImageAndShift
import numpy as np


def encrypt(img, text, out_path):
    imageCrypt = img.copy()

    imgSize = imageCrypt.shape[0] * imageCrypt.shape[1]
    textSize = 0
    for line in text:
        textSize += len(line)

    assert textSize > 0, "Empty text file"
    assert textSize < imgSize, "Image is too small"

    pixStep = imageCrypt.shape[0] * imageCrypt.shape[1] // textSize
    value = 256 - imageCrypt[0, 0, 0] + (256 - imageCrypt[0, 0, 1]) + (256 - imageCrypt[0, 0, 2])
    if pixStep > value:
        pixStep = value

    thisPix = 1

    # write the pixStep into the 0, 0 pixel in image
    r = imageCrypt[0, 0, 0]
    g = imageCrypt[0, 0, 1]
    b = imageCrypt[0, 0, 2]

    imageCrypt[0, 0, 0], imageCrypt[0, 0, 1], imageCrypt[0, 0, 2] = shiftChannels(r, g, b, pixStep)

    for line in text:
        for symbol in line:
            # print(symbol)
            thisChar = ord(symbol)
            if thisChar > 1000:
                thisChar -= 800  # костыль для русских букоф

            if thisChar > pixStep:  # вмещаем с остатком
                whole = thisChar // (pixStep - 1)
                left = thisChar % (pixStep - 1)
                for k in range(pixStep - 1):
                    index = thisPix + k
                    flattenImageAndShift(imageCrypt, index, whole)
                index = thisPix + pixStep - 1
                flattenImageAndShift(imageCrypt, index, left)
            else:
                for m in range(thisChar):
                    flattenImageAndShift(imageCrypt, thisPix + m, 1)

            thisPix += pixStep
            if thisPix + pixStep > imgSize:
                break

    im = Image.fromarray(imageCrypt)
    im.save(out_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #     group = parser.add_mutually_exclusive_group()
    parser.add_argument('-i', '--input-image', type=str, help='Path to the bmp/png image',
                        default='../../../data/original.bmp')
    parser.add_argument('-o', '--output-image', type=str, help='Path to the bmp/png image for saving',
                        default='../../../data/out.bmp')
    parser.add_argument('-f', '--file', type=str, help='Path to the txt file with message for encrypt',
                        default='../../../data/texts/default.txt')
    args = parser.parse_args()

    lines = []
    f = open(args.file)
    for line in f:
        lines.append(line)

    image = np.array(Image.open(args.input_image).convert('RGB'))

    encrypt(image, lines, out_path=args.output_image)
