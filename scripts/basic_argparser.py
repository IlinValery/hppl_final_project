import argparse
import numpy as np
from PIL import Image

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-i', '--input-image', type=str, help='Path to the bmp/png image', default='../data/image.bmp')
group.add_argument('-o', '--output-image', type=str, help='Path to the bmp/png image for saving',
                   default='../data/outputs/out.bpmпше згдд')
group.add_argument('-k', '--key', type=str, help='Path to the txt file with key', default='../data/key.txt')
group.add_argument('-f', '--file', type=str, help='Path to the txt file with message for encrypt',
                   default='../data/texts/default.txt')
group.add_argument('--c', '--show-clock', default=False, action='store_true')
args = parser.parse_args()

key = open(args.key, "r").read()
file_text = open(args.file, "r").read()
image = np.array(Image.open(args.input_image).convert('RGB'))

if __name__ == '__main__':
    print(f'Following arguments was recognized: \n{args}')
    print(key)
    print(file_text)
    print(image.shape)
