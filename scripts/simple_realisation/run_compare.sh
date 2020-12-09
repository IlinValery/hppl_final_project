#!/bin/bash

FILES=../../data/texts/*
for text in $FILES
do
    filename=$(basename -- $text)
    python advanced/encryptor.py -i ../../data/basic/colored/original.bmp -o ../../data/outputs/out.bmp -k ../../data/key.txt -f ../../data/texts/$filename
    python advanced/decryptor.py -i ../../data/outputs/out.bmp -k ../../data/key.txt -f ../../data/outputs/out_text.txt

    python basic/encryptor.py -i ../../data/basic/colored/original.bmp -o ../../data/outputs/out.bmp -f ../../data/texts/$filename
    python basic/decryptor.py -ir ../../data/basic/colored/original.bmp -ic ../../data/outputs/out.bmp -f ../../data/outputs/out_text.txt

done

python plot_graphs.py