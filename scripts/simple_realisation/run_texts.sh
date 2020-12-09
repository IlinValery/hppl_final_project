#!/bin/bash

FILES=../../data/texts/*
for text in $FILES
do
    filename=$(basename -- $text)
    echo $filename
    python advanced/encryptor.py -i ../../data/fancy_guy.png -o ../../data/outputs/out.bmp -k ../../data/key.txt -f ../../data/texts/$filename
    python advanced/decryptor.py -i ../../data/outputs/out.bmp -k ../../data/key.txt -f ../../data/outputs/out_text.txt
done