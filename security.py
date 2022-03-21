# This program provides functions for encrypting and decrypting a text file
# using a Caesar Cipher and functions for the Master Password for PyPass

import string
import random

all_chars = list(string.ascii_lowercase + 
                string.ascii_uppercase + string.digits 
                + string.punctuation) # list of all upper/lowercase, digits and punctuation
shift = 0 # Shift used for Caesar
master_pass = "" # Master Password

def validate(password):
    """
    Determines if the consumed password is the same as the password
    stored in sec.txt. Returns 1 if the passwords match or if sec.txt
    does not exist (creates sec.txt), and -1 otherwise

    Effects:
        Reads, Writes, Creates, Encrypts and Decrypts file
    
    Return:
        Int (1 or -1)

    Global:
        shift: Int
        master_pass: Str

    Args:
        password: Str
    """
    global shift, master_pass
    try:
        decrypt(1, "sec.txt")
        text = open("sec.txt", 'r')
        line = text.readlines()
        text.close()
        encrypt(1, "sec.txt")
        shift = len(line[0])
        if (line[0] == password):
            master_pass = password
            print(master_pass)
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
        master_pass = password
        return 1 #success (new password)

def encrypt(shift, name):
    """
    Encrypts a text file using a Caesar Cipher

    Effects:
        Reads, Writes and Encrypts file
    
    Return:
        Does not return any value

    Args:
        shift: Int
        name: str
    
    Requires:
        shift >= 1 [not asserted]
        name represents a valid text file in the same directory [not asserted]
    """
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

def decrypt(shift, name):
    """
    Decrypts a text file using a Caesar Cipher

    Effects:
        Reads, Writes and Decrypts file
    
    Return:
        Does not return any value

    Args:
        shift: Int
        name: Str
    
    Requires:
        shift >= 1 [not asserted]
        name represents a valid text file in the same directory [not asserted]
    """
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

def change_master_pass(old, new, label, listbox):
    """
    Changes the master password to new if old matches the old master password.
    Updates label depending on its success.

    Effects:
        Reads, Writes, Encrypts and Decrypts files
    
    Return:
        Does not return any value

    Global:
        shift: Int
        master_pass: Str

    Args:
        old: Str
        new: Str
        label: ttk.Label
        listbox: tk.Listbox
    """
    global shift, master_pass
    if (old != master_pass):
        label["text"] = "INCORRECT MASTER PASSWORD"
    else:
        label["text"] = "MASTER PASSWORD UPDATED"
        shift = len(new)
        master_pass = new
        text = open("sec.txt", 'w')
        text.write(new)
        text.close()
        encrypt(1, "sec.txt")
        encrypt(shift, "log.txt")
        decrypt(shift, "log.txt")


def encrypt_helper():
    """
    Wrapper function for encryption for PyPass.py
    
    Return:
        Does not return any value

    Global:
        shift: Int
    """    
    global shift
    encrypt(shift, "log.txt")

def decrypt_helper():
    """
    Wrapper function for encryption for PyPass.py
    
    Return:
        Does not return any value

    Global:
        shift: Int
    """    
    global shift
    decrypt(shift, "log.txt")