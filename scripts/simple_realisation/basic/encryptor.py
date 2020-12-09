import argparse
from PIL import Image
from utils import channelsToOne, shiftChannels, flattenImageAndShift, save_time
import numpy as np
import timeit


def encrypt(img, text, out_path):
    imageCrypt = img.copy()

    imgSize = imageCrypt.shape[0] * imageCrypt.shape[1]
    textSize = 0
    for line in text:
        textSize += len(line)

    print(textSize)

    assert textSize > 0, "Empty text file"
    assert textSize < imgSize, "Image is too small"

    pixStep = np.floor(imageCrypt.shape[0] * imageCrypt.shape[1] / textSize)
    pixStep = int(pixStep)
    thisPix = 1

    # write the pixStep into the 0, 0 pixel in image
    r = imageCrypt[0, 0, 0]
    g = imageCrypt[0, 0, 1]
    b = imageCrypt[0, 0, 2]

    imageCrypt[0, 0, 0], imageCrypt[0, 0, 1], imageCrypt[0, 0, 2] = shiftChannels(r, g, b, pixStep)

    for line in text:
        for symbol in line:
            thisChar = ord(symbol)
            if thisChar > 1000:
                thisChar -= 800  # костыль для русских букоф

            if thisChar > pixStep:  # вмещаем с остатком
                whole = np.floor(thisChar / (pixStep - 1))
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
                        default='../../../data/image.bmp')
    parser.add_argument('-o', '--output-image', type=str, help='Path to the bmp/png image for saving',
                        default='../../../data/out.bmp')
    parser.add_argument('-f', '--file', type=str, help='Path to the txt file with message for encrypt',
                        default='../../../data/texts/default.txt')
    parser.add_argument('--c', '--show-clock', default=False, action='store_true')
    args = parser.parse_args()

    with open(args.file, "r") as f:
        file_text = f.read()
    image = np.array(Image.open(args.input_image).convert('RGB'))

    t1 = timeit.default_timer()
    encrypt(image, file_text, out_path=args.output_image)
    t2 = timeit.default_timer()
    save_time(args.file.split('/')[-1], t1, t2, 'basic_encryptor_times.txt')
