# This program implements the GUI for PyPass

# Import relevant modules
import string
import random
import tkinter as tk
from tkinter import ttk
from write_passwords import *
from security import encrypt_helper, decrypt_helper, change_master_pass
from ctypes import windll

def copy_text(message):
    """
    Clears the user's clipboard, and copies the string message to it.

    Effects:
        Modifies the state of the system's clipboard.
    
    Return:
        No return value

    Global:
        root: The main tkinter window (tk.TK)

    Args:
        message: Str (not asserted)

    Time:
        O(1)
    """
    root.clipboard_clear()
    root.clipboard_append(message)
    root.update()

def callback(event):
    """
    Displays the password for the selected password from event
    
    Effects:
        Modifies window (root)

    Return:
        Does not return any value

    Global:
        password_get_text: the ttk.Label where the password is displayed

    Args: 
        event: a tk.Listbox element (must be valid, not asserted)
    """
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        print(data)
        find_password(data, password_get_text)
        
########################################################
root = tk.Tk() # initialize window

root.title("PyPass") # Set window title

window_width = 800 # Update window elements
window_height = 700
root.geometry(f'{window_width}x{window_height}')
root.resizable(0,0)
root.iconbitmap('icon_i8Q_icon.ico')
########################################################
tabControl = ttk.Notebook(root) # Create notebook for tabs

s = ttk.Style() # Setting up styles
s.configure('TNotebook.Tab', font=('Calibri','16')) # Notebook tab font
s.configure('.', background= "#D4F1F4") # Background color
s.configure('big.TButton', font=('Calibri','16')) # Button font

generate_tab = ttk.Frame(tabControl) # Generate tab
tabControl.add(generate_tab, text ='Generate Password')

save_tab = ttk.Frame(tabControl) # Save tab
tabControl.add(save_tab, text ='View Passwords')

master_tab = ttk.Frame(tabControl) # Master Password tab
tabControl.add(master_tab, text ='Change Master Password')

help_tab = ttk.Frame(tabControl) # Save tab
tabControl.add(help_tab, text ='Help')

tabControl.pack(expand = True, fill="both") # Initialize Tabs
########################################################
# GENERATE PASSWORD TAB
########################################################
# Generate Password (ttk.Label, Static)
ttk.Label(generate_tab, text="Generate Password", font=("Calibri", 35)).pack() 

# Password label (ttk.Label, Dynamic)
password_text = ttk.Label(generate_tab, text="Please Enter a number between 1-50", 
                            font=("Calibri", 20), padding=20) 
password_text.pack()

# Enter length label (ttk.Label, Static)
length_frame = tk.Frame(generate_tab, background="#D4F1F4")
length_frame.pack()

ttk.Label(length_frame, text="Enter length here (1-50):  ", font=("Calibri", 15)).pack(side = LEFT)

# Enter password length here (ttk.Entry, Dynamic)
password_length = ttk.Entry(length_frame, textvariable=tk.StringVar()) 
password_length.pack(side = LEFT)

# Frame for Checkboxes (tk.Frame, Static)
options_frame_top = tk.Frame(generate_tab, background="#D4F1F4")
options_frame_top.pack()
options_frame_bot = tk.Frame(generate_tab, background="#D4F1F4")
options_frame_bot.pack()

# Checkboxes for password options (ttk.Checkbutton, Dynamic)
sym = tk.BooleanVar() # Toggle symbols in password
num = tk.BooleanVar() # Toggle numbers in password
lower = tk.BooleanVar() # Toggle lowercase in password
upper = tk.BooleanVar() # Toggle uppercase in password

ttk.Checkbutton(options_frame_top, text='Include Symbols',variable=sym, offvalue=False, onvalue=True).pack(side = LEFT)
ttk.Checkbutton(options_frame_top, text='Include Numbers',variable=num, offvalue=False, onvalue=True).pack(side = LEFT)
ttk.Checkbutton(options_frame_bot, text='Include lowercase letters',variable=lower, offvalue=False, onvalue=True).pack(side = LEFT)
ttk.Checkbutton(options_frame_bot, text='Include Uppercase Letters',variable=upper, offvalue=False, onvalue=True).pack(side = LEFT)

# Frame for Password Buttons (tk.Frame, Static)
generate_buttons_frame = tk.Frame(generate_tab, background="#D4F1F4")
generate_buttons_frame.pack()

# Generate password (ttk.Button, Dynamic)
ttk.Button(generate_buttons_frame, text='New Password', style='big.TButton',
            command=lambda: generate_password(password_length.get(), password_text, sym.get(), num.get(), 
            lower.get(), upper.get())).pack(side = LEFT)

# Copy password (ttk.Button, Dynamic)
ttk.Button(generate_buttons_frame, text="Copy Password", style='big.TButton',
            command=lambda: copy_text(password_text['text'])).pack(side = LEFT) 

# Save Password (ttk.Label, Static)
ttk.Label(generate_tab, text="Save Password", font=("Calibri", 35)).pack()

# Password Save Success (ttk.Label, Dynamic)
password_add_text = ttk.Label(generate_tab, text="Enter the label and password below!", font=("Calibri", 15))
password_add_text.pack()

# Enter label (ttk.Label, Static)
ttk.Label(generate_tab, text="Enter label here:", font=("Calibri", 15)).pack()

# Enter label for password here (ttk.Entry, Dynamic)
password_add_label = ttk.Entry(generate_tab, textvariable=tk.StringVar())
password_add_label.pack()

# Enter password (ttk.Label, Static)
ttk.Label(generate_tab, text="Enter password here (no spaces allowed):", font=("Calibri", 15)).pack()

# Enter password here (ttk.Entry, Dynamic)
password_add_val = ttk.Entry(generate_tab, textvariable=tk.StringVar()) 
password_add_val.pack()

# Add password (ttk.Button, Dynamic)
ttk.Button(generate_tab, text='Add Password', style='big.TButton',
            command=lambda: add_password(password_add_label.get(), password_add_val.get(), password_add_text, password_list)).pack()
########################################################
# SAVE PASSWORD TAB
########################################################
# Retrieve password (ttk.Label, Static)
ttk.Label(save_tab, text="Saved Passwords", font=("Calibri", 35), padding = 10).pack()

# List of saved passwords + scrollbar (tk.Listbox/tk.Scrollbar, Dynamic)
password_frame = tk.Frame(save_tab, background="#D4F1F4")
password_frame.pack()

password_list = tk.Listbox(password_frame, font = ('Calibri', 16), selectmode= 'SINGLE', width = 60)
password_list.bind("<<ListboxSelect>>", callback)
password_list.pack(side = "left", fill = "y")

scrollbar = tk.Scrollbar(password_frame, orient="vertical")
scrollbar.config(command=password_list.yview)
scrollbar.pack(side="right", fill="y")

# Selected Password (ttk.Label, Static)
ttk.Label(save_tab, text="Selected Password", font=("Calibri", 35)).pack()

# Selected password text (ttk.Label, Dynamic)
password_get_text = ttk.Label(save_tab, text="Please Select a Password!", font=("Calibri", 15))
password_get_text.pack()

# Copy Password (ttk.Button, Dynamic)
ttk.Button(save_tab, text="Copy Password", style='big.TButton',
            command=lambda: copy_text(password_get_text['text'])).pack()

# Delete Password (ttk.Button, Dynamic)
ttk.Button(save_tab, text='Delete Password', style='big.TButton',
            command=lambda: delete_password(password_list.get((password_list.curselection())[0]), 
            password_get_text, password_list, (password_list.curselection())[0])).pack()

########################################################
# MASTER PASSWORD TAB
########################################################
# CHANGE MASTER PASSWORD (ttk.Label, Static)
ttk.Label(master_tab, text="Change Master Password", font=("Calibri", 35)).pack()

# Enter old password (ttk.Entry, Dynamic)
ttk.Label(master_tab, text="Enter Previous Master Password:", font=("Calibri", 15)).pack()
old_master_pass = ttk.Entry(master_tab, textvariable=tk.StringVar()) 
old_master_pass.pack()

# Enter new password (ttk.Entry, Dynamic)
ttk.Label(master_tab, text="Enter New Master Password:", font=("Calibri", 15)).pack()
new_master_pass = ttk.Entry(master_tab, textvariable=tk.StringVar()) 
new_master_pass.pack()

# Confirm new password (ttk.Button, Dynamic)
ttk.Button(master_tab, text='Change Master Password', style='big.TButton',
            command=lambda: change_master_pass(old_master_pass.get(), 
            new_master_pass.get(), master_pass_status, password_list)).pack()

# Status (ttk.Label, Dynamic)
master_pass_status = ttk.Label(master_tab, text="", font=("Calibri", 15))
master_pass_status.pack()
########################################################
# HELP TAB
########################################################
# Generate password section (ttk.Label, Static)
ttk.Label(help_tab, text="Generate Password", font=("Calibri", 30)).pack()
ttk.Label(help_tab, text="For the password length, enter a number between 1-50 inclusive.", font=("Calibri", 15)).pack()
ttk.Label(help_tab, text="To copy the password, press the Copy Password button.", font=("Calibri", 15)).pack()

# Save password section (ttk.Label, Static)
ttk.Label(help_tab, text="Save Password", font=("Calibri", 30)).pack()
ttk.Label(help_tab, text="Your password label may consist of any character with multiple words.", font=("Calibri", 15)).pack()
ttk.Label(help_tab, text="Any whitespace at the beginning is ignored.", font=("Calibri", 15)).pack()
ttk.Label(help_tab, text="Your password may not contain any whitespace.", font=("Calibri", 15)).pack()

# View passwords section (ttk.Label, Static)
ttk.Label(help_tab, text="View Passwords", font=("Calibri", 30)).pack()
ttk.Label(help_tab, text="Click on any label on the list to view its password.", font=("Calibri", 15)).pack()
ttk.Label(help_tab, text="Press the Copy Password button to copy it to your clipboard.", font=("Calibri", 15)).pack()
ttk.Label(help_tab, text="Press the Delete Password button to delete it.", font=("Calibri", 15)).pack()


########################################################
def main_loop():
    """
    Initiates the main window for PyPass.

    Effects: 
        Displays window (Root).
    
    Return:
        Does not return any value.

    Global:
        root: a tkinter window (tk.Tk)
    """

    try:
        # modify DpiAwareness to improve readability of text
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        decrypt_helper()
        display_passwords(password_list) # Update Listbox on launch
        password_list.pack()
        root.mainloop()
        encrypt_helper()
