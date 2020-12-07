def getSeed(key):
    keySeed = 1
    key = key.lower()
    for i in range(len(key) - 1):
        keySeed *= ord(key[i]) * (ord(key[i]) - ord(key[i + 1]))
    return abs(keySeed) % (2**32-1)
