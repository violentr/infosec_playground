#!/usr/bin/env python

import binascii

def process_image(bin_file):
    raw_data = ""
    with open(bin_file, 'r') as f:
        contents = f.readlines()
        for line in contents:
            line.strip()
            line = line.replace(r'\x', '')
            line.replace(' ', '')
            line.replace('\n', '')
            raw_data += line
    return raw_data

def main():
    print("[+] Processing binary image")
    data = process_image('./file.jpg')
    data = data.replace('\n', '')
    data = binascii.a2b_hex(data)

    print("[+] Creating image from binary data")
    with open('image.jpg', 'wb') as image_file:
        image_file.write(data)
        print("[+] File was saved to %s" % image_file.name)


if __name__ == '__main__':
    main()
