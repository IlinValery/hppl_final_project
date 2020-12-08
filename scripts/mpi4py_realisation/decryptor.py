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


def decrypt(image, key, out_path="decrypt_text.txt"):
    try:
        size_from_key = int(key[-2:-1])
    except ValueError:
        return

    start_rank_number = size_from_key // size
    if rank == size - 1:
        sub_images = size_from_key // size + size_from_key % size
    else:
        sub_images = size_from_key // size

    if sub_images == 0:
        start_rank_number = sub_images = 1

    np.random.seed(getSeed(key))
    np.random.shuffle(image)
    keys = [''.join([np.random.choice(alphabet) for _ in range(len(key))]) for _ in range(size_from_key)]

    decryptText = ""

    if rank <= size_from_key - 1:
        for i in range(sub_images):
            rank_from_key = rank * start_rank_number + i
            key = keys[rank_from_key]

            np.random.seed(getSeed(key))

            numImgPerRank = image.shape[0] // size_from_key
            image_from_key = image[rank_from_key * numImgPerRank:(rank_from_key + 1) * numImgPerRank, :]

            wpixs = []
            while True:
                while True:
                    ix = np.random.randint(0, image_from_key.shape[0]-1)
                    iy = np.random.randint(0, image_from_key.shape[1]-1)
                    if (ix, iy) not in wpixs:
                        wpixs.append((ix, iy))
                        break
                thisChar = 0
                thisChar |= ((image_from_key[ix, iy, 0] & 0x7) << 5)
                thisChar |= ((image_from_key[ix, iy, 1] & 0x3) << 3)
                thisChar |= (image_from_key[ix, iy, 2] & 0x7)

                if thisChar > 130:
                    thisChar += 890
                if thisChar == 0:
                    break
                decryptText += chr(thisChar)

    sendbuf = decryptText
    recvbuf = comm.gather(sendbuf, root=0)

    if rank == 0:
        with open(out_path, 'w') as f:
            f.write(''.join(recvbuf))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-image', type=str, help='Path to the bmp/png image', default='../../data/outputs/out.bmp')
    parser.add_argument('-k', '--key', type=str, help='Path to the txt file with key', default='../../data/key_mpi4py.txt')
    parser.add_argument('-f', '--file', type=str, help='Path to the txt file with decrypted message',
                       default='../../data/outputs/decrypt_txt.txt')
    parser.add_argument('--c', '--show-clock', default=False, action='store_true')
    args = parser.parse_args()

    with open(args.key, "r") as f:
        key = f.read()
    image = np.array(Image.open(args.input_image).convert('RGB'))
    
    decrypt(image, key, out_path=args.file)
