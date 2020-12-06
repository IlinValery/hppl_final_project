import random
from PIL import Image
from utils import getSeed
import numpy as np
import argparse


def encrypt(input_img, text, key, out_path="crypt_image.bmp"):
    image = input_img.copy()
    imgSize = image.shape[0] * image.shape[1]
    textSize = len(text)
        
    assert len(text) > 0, "Empty text file"
    assert textSize < imgSize, "Image is too small"
    
#     добавляем ноль (ноль как число!) в самый конец текста
    text += '\0'
    textSize += 1
    
    random.seed(getSeed(key))
    
    wpixs = []
    for i in range(textSize):
        while True:
            ix = random.randint(0, image.shape[0]-1)
            iy = random.randint(0, image.shape[1]-1)
            if (ix, iy) not in wpixs:
                wpixs.append((ix, iy))
                break
        thisChar = ord(text[i])
        if thisChar > 1000:
            thisChar -= 890 #  костыль для русских букв 
        thisColor = image[ix, iy]
#          упаковка в RGB 323
        image[ix, iy, 0] = (image[ix, iy, 0] & (0x1F << 3)) | ((thisChar & 0xE0) >> 5)
        image[ix, iy, 1] = (image[ix, iy, 1] & (0x3F << 2)) | ((thisChar & 0x18) >> 3)
        image[ix, iy, 2] = (image[ix, iy, 2] & (0x1F << 3)) | (thisChar & 0x7)
        
    im = Image.fromarray(image)
    im.save(out_path) 
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
#     group = parser.add_mutually_exclusive_group()
    parser.add_argument('-i', '--input-image', type=str, help='Path to the bmp/png image', default='../../../data/image.bmp')
    parser.add_argument('-o', '--output-image', type=str, help='Path to the bmp/png image for saving',
                       default='../../../data/outputs/out.bmp')
    parser.add_argument('-k', '--key', type=str, help='Path to the txt file with key', default='../../../data/key.txt')
    parser.add_argument('-f', '--file', type=str, help='Path to the txt file with message for encrypt',
                       default='../../../data/texts/default.txt')
    parser.add_argument('--c', '--show-clock', default=False, action='store_true')
    args = parser.parse_args()

    with open(args.key, "r") as f:
        key = f.read()
    with open(args.file, "r") as f:
        file_text = f.read()
    image = np.array(Image.open(args.input_image).convert('RGB'))
    
    encrypt(image, file_text, key, out_path=args.output_image)
#     print(f'Following arguments was recognized: \n{args}')
#     print(key)
#     print(file_text)
#     print(image.shape)
