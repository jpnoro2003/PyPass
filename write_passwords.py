# This file contains functions for the main application regarding creating, reading, writing,
# and modifying the passwords in the log file

# Import modules
import string
import random
import tkinter as tk
from tkinter import ttk
from tkinter import *

def generate_password(len, message, sym, num, lower, upper):
    """
    Generates a password given a length between 1-50 and booleans indicating which
    characters to include, then updates a ttk.Label with the password or an error message.

    Effects:
        Modifies window (ttk.Label)
        Produces output in console

    Return:
        Does not return any value

    Args: 
        len: Str
        message: ttk.Label (must be valid, not asserted)
        sym, num, lower, upper: Bool
    
    Time: 
        O(n), where n is the integer represented in len
    """

    if ((sym == False) and (num == False) and (lower == False) and (upper == False)):
        print("YIKES")
        message['text'] = "ALL CHARACTERS EXCLUDED"
        message.pack()
        return

    lowercase = list(string.ascii_lowercase) # lowercase characters list
    uppercase = list(string.ascii_uppercase) # uppercase characters list
    numbers = list(string.digits) # digits characters list
    punctuation = list(string.punctuation) # punctuation characters list

    choices = "" # string containing all possible characters for selection
    if (sym == True):
        choices += string.punctuation
    if (num == True):
        choices += string.digits
    if (lower == True):
        choices += string.ascii_lowercase
    if (upper == True):
        choices += string.ascii_uppercase
        
    password = ""

    try:
        pass_len = int(len) ## try to get number from input
        if ((pass_len > 50) or (pass_len < 1)) :
            message['text'] = "PLEASE KEEP LENGTH BETWEEN 1 AND 50" # Display input message
            message.pack()
            return
    except:
        message['text'] = "INVALID LENGTH" # Display input message
        message.pack()
        return

    choices = list(choices) # Change string into list
    for i in range(pass_len) :
        password += (random.choice(choices)) # Add characters
    
    message['text'] = password
    message.pack()

def display_passwords(label):
    """
    Displays the labels from log.txt onto a tk.Listbox

    Effects:
        Modifies window (tk.Listbox)
        Produces output in console
        Reads from file (log.txt)

    Return:
        Does not return any value

    Args: 
        label: tk.Listbox (must be valid, not asserted)
    
    Time: 
        O(nlogn), where n is the number of passwords in log.txt
    """

    label.delete(0, END)
    print("ATTEMPTING TO DISPLAY PASSWORDS... ")
    passwords = open("log.txt", 'r')
    lines = passwords.readlines()
    passwords.close()

    i = len(lines)
    lines.sort() # Uses timsort, O(nlogn)
    
    for line in lines:
        a = line.split()
        print(line)
        label.insert(i, ' '.join(a[:-1]))
        print("INSERTED!!!!")
        --i
    label.pack()
    print("SUCCESS")

def find_password(name, label):
    """
    Finds the password for name in log.txt, then updates the label with it.
    
    Effects:
        Modifies window (ttk.Label)
        Produces output in console
        Reads from file (log.txt)

    Return:
        Str (representing password) or Int (-1, unsuccessful)

    Args:
        name: Str
        label: ttk.Label (must be valid, not asserted)
    
    Time: 
        O(n), where n is the number of passwords in log.txt
    """
    print(name)
    passwords = open("log.txt", 'r')

    for line in passwords:
        print((''.join(line.split()[0:-1])).upper())
        if ((' '.join((line.split()[0:-1])).upper()) == name.upper()):
            passwords.close()
            print("FIND_PASSWORD: SUCCESS")
            try: 
                label["text"] = line.split()[-1]
                return (line.split()[-1]) # Return Success
            except:
                label["text"] = "" # Case of password with all spaces
                return "" # Return Success
    
    passwords.close()
    label["text"] = "PASSWORD NOT FOUND"
    print("FIND_PASSWORD: FAIL")
    return -1 # Error

def delete_password(name, label, entries, position):
    """
    Deletes the entry for 'name' in log.txt if possible, then modifies 
    a Label and Labellist accordingly

    Effects:
        Modifies window (ttk.Label, tk.Labellist)
        Produces output in console
        Reads/Modifies file (log.txt)

    Return:
        Bool (true if successful, false otherwise)

    Args:
        name: Str
        label: ttk.Label (must be valid, not asserted)
        entries: tk.Labellist (must be valid, not asserted)
        position: Int (must represent position on entries, not asserted)
    
    """
    print("PASSWORD LABEL: " + name)
    passwords = open("log.txt", 'r')
    lines = passwords.readlines()
    passwords.close()
    success = False
    passwords = open("log.txt", 'w')

    for line in lines:
        if not ((' '.join((line.split()[0:-1])).upper()) == name.upper()): #line.startswith(name.upper())
            passwords.write(line)
        else:
            success = True

    print("DELETE_PASSWORD: "+str(success))
    if (success) :
        label["text"] = "PASSWORD DELETED"
    else:
        label["text"] = "PASSWORD NOT FOUND"
        
    label.pack()
    entries.delete(position)
    entries.pack()
    return success

def add_password(name, password, label, entries):
    """
    Updates log.txt with a password for name, then updates label
    and entries accordingly.

    Effects:
        Modifies window (ttk.Label, tk.Labellist)
        Produces output in console
        Reads/Modifies file (log.txt)

    Return:
        Int (1 if successful, -1 otherwise)

    Args:
        name: Str
        password: Str
        label: ttk.Label (must be valid, not asserted)
        entries: tk.Labellist (must be valid, not asserted)
    
    Time: 
        O(nlogn), where n is the number of passwords in log.txt
    """

    print("Inputted name: " + str(name).upper())

    if (len(name.split()) == 0): #Empty label
        print("ADD_PASSWORD: FAIL")
        label["text"] = "EMPTY LABEL FIELD"
        return -1 #Error, Improper label (blank)

    if (len(password) == 0): #blank password
        print("ADD_PASSWORD: FAIL")
        label["text"] = "EMPTY PASSWORD FIELD"
        return -1 # Error, password left blank
    
    if (len(password.split()) != 1): #Multi word password
        print("ADD_PASSWORD: FAIL")
        label["text"] = "MULTIPLE WORDS IN PASSWORD"
        return -1 # Error, password left blank

    passwords = open("log.txt", 'r')
    lines = passwords.readlines()
    passwords.close()
    
    if (find_password(name.upper(), label) != -1): # password already in database
        print("ADD_PASSWORD: FAIL")
        label["text"] = "LABEL ALREADY EXISTS"
        label.pack()
        return -1 # Error, entry already exists

    passwords = open("log.txt", "w")

    titles = list()
    for line in lines:
        titles.append(' '.join(line.split()[:-1]))

    titles.append(name.upper())
    titles.sort()
    index = titles.index(name.upper())
    lines.insert(index, name.upper()+" "+password+"\n")
    lines = "".join(lines)
    passwords.write(lines)
    print("ADD_PASSWORD: SUCCESS")
    label["text"] = "SUCCESS"
    label.pack()

    passwords.close()
    display_passwords(entries)
    return 1 # success

