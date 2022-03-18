# This program provides functions for encrypting and decrypting a text file
# using a Caesar Cipher.

import string
import random

all_chars = list(string.ascii_lowercase + string.ascii_uppercase + string.digits +string.punctuation)
shift = 0

def validate(password):
    global shift
    try:
        decrypt(1, "sec.txt")
        text = open("sec.txt", 'r')
        line = text.readlines()
        text.close()
        encrypt(1, "sec.txt")
        shift = len(line[0])
        if (line[0] == password):
            return 1 #success
        else:
            return -1 #fail
    except:
        print("OH NO")
        text = open("sec.txt", 'a+')
        shift = len(password)
        text.write(password)
        text.close()
        encrypt(1, "sec.txt")
        return 1 #success (new password)

# encrypt(shift) encrypts a text file using a Ceasar Cipher using shift.
# Effects: Opens, reads, and modifies file.
# Requires: shift >= 1
# Time: O(nmh), where n is the number of lines in the document,
# m is the most characters on a line, and h is the length of all_chars
def encrypt(shift, name):
    text = open(name, 'r')
    lines = text.readlines()
    text.close()
    text = open(name, 'w')
    for line in lines:
        characters = list(line)
        for i, char in enumerate(characters):
            if char in all_chars :
                characters[i] = all_chars[(all_chars.index(char) + shift) % len(all_chars)]
            else:
                characters[i] = char
                continue
        text.write(''.join(characters))
    text.close()

# decrypt(shift) decrypts a text file using a Ceasar Cipher using shift.
# Effects: Opens, reads, and modifies file.
# Requires: shift >= 1
# Time: O(nmh), where n is the number of lines in the document,
# m is the most characters on a line, and h is the length of all_chars
def decrypt(shift, name):
    text = open(name, 'r')
    lines = text.readlines()
    text.close()
    text = open(name, 'w')
    for line in lines:
        characters = list(line)
        for i, char in enumerate(characters):
            if char in all_chars :
                characters[i] = all_chars[all_chars.index(char) - shift]
            else:
                characters[i] = char
                continue
        text.write(''.join(characters))
    text.close()

def encrypt_helper():
    global shift
    encrypt(shift, "log.txt")

def decrypt_helper():
    global shift
    decrypt(shift, "log.txt")