#!/usr/bin/env bash
#https://null-byte.wonderhowto.com/how-to/hack-like-pro-crack-passwords-part-4-creating-custom-wordlist-with-crunch-0156817/

#generate variations of the the word below
word=fristi

#lower and uppercase
#fristiLeak
if [ -x crunch ]; then
  pattern=@@@@
  min=10
  max=10
  letters=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
  crunch $min $max $letters -t $word$pattern -o ./wordlist.lst
else
  echo -e "crunch should be installed !"
fi
