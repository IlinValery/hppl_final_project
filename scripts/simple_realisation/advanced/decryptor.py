import random
from PIL import Image
from utils import getSeed, save_time
import numpy as np
import argparse
import timeit


def decrypt(image, key, out_path="decrypt_text.txt"):
    imgSize = image.shape[0] * image.shape[1]
    random.seed(getSeed(key))
    decryptText = ""
    
    wpixs = []
    while True:
        while True:
            ix = random.randint(0, image.shape[0]-1)
            iy = random.randint(0, image.shape[1]-1)
            if (ix, iy) not in wpixs:
                wpixs.append((ix, iy))
                break
        thisChar = 0
        thisChar |= ((image[ix, iy, 0] & 0x7) << 5)
        thisChar |= ((image[ix, iy, 1] & 0x3) << 3)
        thisChar |= (image[ix, iy, 2] & 0x7)
        
        if thisChar > 130:
            thisChar += 890
        if thisChar == 0:
            break
        decryptText += chr(thisChar)
        
    with open(out_path, 'w') as f:
        f.write(decryptText)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-image', type=str, help='Path to the bmp/png image', default='../../../data/outputs/out.bmp')
    parser.add_argument('-k', '--key', type=str, help='Path to the txt file with key', default='../../../data/key.txt')
    parser.add_argument('-f', '--file', type=str, help='Path to the txt file with decrypted message',
                       default='../../../data/outputs/decrypt_txt.txt')
    parser.add_argument('--c', '--show-clock', default=False, action='store_true')
    args = parser.parse_args()

    with open(args.key, "r") as f:
        key = f.read()
    image = np.array(Image.open(args.input_image).convert('RGB'))

    t1 = timeit.default_timer()
    decrypt(image, key, out_path=args.file)
    t2 = timeit.default_timer()
    save_time(args.file.split('/')[-1], t1, t2, 'decryptor_times.txt')
