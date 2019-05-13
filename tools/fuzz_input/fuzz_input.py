#!/usr/bin/env python
import sys
import random
from pathlib import Path

''' Generate 1MB of bad data, payload for fuzzing input '''
try:
    output_file = sys.argv[1]
except:
    output_file = "fuzz_output.txt"

kilobytes = 1024

print("output file is %s", output_file)

def default_file():
    if not os.path.isfile(output_file):
        Path(output_file).touch()

def character_table():
    out = "chars_table.txt"
    with open(out, 'w') as f:
        for i in range(0, 255):
            string = "Char: %s Nr: %s \n" % (chr(i), i)
            print(string)
            f.write(string)

def random_number():
    nr = random.randint(95, 255)
    print("Random number is %s" % nr)
    return nr

with open(output_file, 'w') as f:
    for i in range(0, 255):
        char = chr(random_number())
        print("char is %s" % char)
        string = char * 1023 + "\n"
        print(string)
        f.write(string)

character_table()
