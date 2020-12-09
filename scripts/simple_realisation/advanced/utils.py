import os

def getSeed(key):
    keySeed = 1
    key = key.lower()
    for i in range(len(key) - 1):
        keySeed *= ord(key[i]) * (ord(key[i]) - ord(key[i + 1]))
    return keySeed


def save_time(file_name, t1, t2, out_file):
    mode = 'w'
    if os.path.exists(out_file):
        mode = 'a'
    with open(out_file, mode) as f:
        f.write(file_name + ' - ' + str(t2 - t1) + '\n')
