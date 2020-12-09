from argparse import ArgumentParser
import numpy as np
from PIL import Image
from utils import save_time
import timeit


def decrypt(image_reference, image_crypted, out_path="decrypt_text.txt"):
    imgSize = image_reference.size

    pixels_reference = image_reference.reshape(imgSize // 3, 3)
    pixels_crypted = image_crypted.reshape(imgSize // 3, 3)

    decrypted_text = ""
    step = (pixels_crypted[0] - pixels_reference[0]).sum()
    step = int(step)
    start_pixel_number = 1

    while True:
        # Sum up all differences in pixels per one step
        ascii_code = 0
        for i in range(step):
            ascii_code += (pixels_crypted[start_pixel_number + i] - pixels_reference[start_pixel_number + i]).sum()
        ascii_code = int(ascii_code)

        # Exit if there no differences in the step
        if ascii_code == 0:
            break

        # Cheat for russian letters, from ASCII
        if ascii_code > 200:
            ascii_code += 800

        # Add found letter
        decrypted_text += chr(ascii_code)
        # print(ascii_code)

        # Change position of the next start pixel to the end of the step
        start_pixel_number += step

        # Check if the next step fully exists in the image
        if start_pixel_number + step > imgSize:
            break

    with open(out_path, 'w') as f:
        f.write(decrypted_text)


if __name__ == '__main__':
    parser = ArgumentParser('Basic decryptor.')
    parser.add_argument('-ir',
                        '--image_ref_path',
                        type=str,
                        help='Path to image which is used as a reference.',
                        default='../../../data/basic/colored/original.bmp')
    parser.add_argument('-ic',
                        '--image_crypt_path',
                        type=str,
                        help='Path to a crypted image',
                        default='../../../data/basic/colored/crypted.bmp')
    parser.add_argument('-f', '--file', type=str, help='Path to the txt file with decrypted message',
                        default='../../../data/outputs/decrypt_txt.txt')
    args = parser.parse_args()

    image_reference = np.array(Image.open(args.image_ref_path).convert('RGB'))
    image_crypted = np.array(Image.open(args.image_crypt_path).convert('RGB'))

    t1 = timeit.default_timer()
    decrypt(image_reference, image_crypted, out_path=args.file)
    t2 = timeit.default_timer()
    save_time(args.file.split('/')[-1], t1, t2, 'decryptor_times.txt')
