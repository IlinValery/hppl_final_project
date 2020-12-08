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

def decrypt_func(image, key):
    decryptText = ""
    np.random.seed(getSeed(key))

    wpixs = []
    while True:
        while True:
            ix = np.random.randint(0, image.shape[0] - 1)
            iy = np.random.randint(0, image.shape[1] - 1)
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
    return decryptText


def decrypt(image, key, out_path="decrypt_text.txt"):
    try:
        size_from_key = int(key[-2:-1])
    except ValueError:
        return

    ranks = np.arange(size_from_key)
    ranks = np.array_split(ranks, size)[rank]

    np.random.seed(getSeed(key))
    np.random.shuffle(image)
    keys = [''.join([np.random.choice(alphabet) for _ in range(len(key))]) for _ in range(size_from_key)]
    image = np.array_split(image, size_from_key, axis=0)

    decryptText = ""
    for r in ranks:
        decryptText += decrypt_func(image[r], keys[r])

    decryptText = comm.gather(decryptText, root=0)

    if rank == 0:
        with open(out_path, 'w') as f:
            f.write(''.join(decryptText))


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
