from PIL import Image
from utils import getSeed
import numpy as np
import argparse
from mpi4py import MPI
import string

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

alphabet = list(string.ascii_lowercase + string.digits)


def encrypt(input_img, text, key, out_path="crypt_image.bmp"):
    try:
        process_num = int(key[-2:-1])
    except ValueError:
        if rank == 0:
            print("The key should have a number of processes in the end!")
        return

    assert process_num == size, "Number of processes doesn't correspond to required one from the key!"

    image = input_img.copy()
    image = image[:len(image) // size * size]

    # Shuffle initial image and define keys for each rank
    np.random.seed(getSeed(key))
    np.random.shuffle(image)
    keys = [''.join([np.random.choice(alphabet) for _ in range(len(key))]) for _ in range(size)]

    initial_key = key

    # Write text into pixels using a unique key
    key = keys[rank]
    np.random.seed(getSeed(key))

    numTextPerRank = len(text) // size
    if rank == size - 1:
        text = text[rank * numTextPerRank:]
    else:
        text = text[rank * numTextPerRank:(rank + 1) * numTextPerRank]

    numImgPerRank = image.shape[0] // size
    image = image[rank * numImgPerRank:(rank + 1) * numImgPerRank, :]

    imgSize = image.shape[0] * image.shape[1]
    textSize = len(text)
        
    assert len(text) > 0, "Empty text file"
    assert textSize < imgSize, "Image is too small"

#     добавляем ноль (ноль как число!) в самый конец текста
    text += '\0'
    textSize += 1

    wpixs = []
    for i in range(textSize):
        while True:
            ix = np.random.randint(0, image.shape[0]-1)
            iy = np.random.randint(0, image.shape[1]-1)
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

    sendbuf = image

    recvbuf = None
    if rank == 0:
        recvbuf = np.empty((numImgPerRank * size, image.shape[1], image.shape[2]), dtype=np.uint8)

    comm.Gather(sendbuf, recvbuf, root=0)

    if rank == 0:
        np.random.seed(getSeed(initial_key))
        order = np.arange(len(recvbuf))
        np.random.shuffle(order)
        order = order.argsort()
        recvbuf = recvbuf[order]

        im = Image.fromarray(recvbuf)
        im.save(out_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
#     group = parser.add_mutually_exclusive_group()
    parser.add_argument('-i', '--input-image', type=str, help='Path to the bmp/png image', default='../../data/fancy_guy.png')
    parser.add_argument('-o', '--output-image', type=str, help='Path to the bmp/png image for saving',
                       default='../../data/outputs/out.bmp')
    parser.add_argument('-k', '--key', type=str, help='Path to the txt file with key', default='../../data/key_mpi4py.txt')
    parser.add_argument('-f', '--file', type=str, help='Path to the txt file with message for encrypt',
                       default='../../data/texts/default.txt')
    parser.add_argument('--c', '--show-clock', default=False, action='store_true')
    args = parser.parse_args()

    with open(args.key, "r") as f:
        key = f.read()
    with open(args.file, "r") as f:
        file_text = f.read()
    image = np.array(Image.open(args.input_image).convert('RGB'))
    
    encrypt(image, file_text, key, out_path=args.output_image)
