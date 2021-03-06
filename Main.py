# This program implements the main screen for PyPass.

import tkinter as tk
from tkinter import ttk
from ctypes import windll
from security import validate
########################################################
def login(password, label):
    """
    Determines if the provided password is valid, then opens the main window

    Effects:
        Closes current window and opens new window
        Potentially modifies current window (ttk.Label)
    
    Return:
        Does not return any value
    
    Args:
        password: Str
        label: ttk.Label
    """

    if (validate(password) == 1):
        start_page.destroy()
        from PyPass import main_loop
        main_loop()
    else:
        label["text"] = "INCORRECT PASSWORD"
########################################################
start_page = tk.Tk()

start_page.title("PyPass") # Set window title

window_width = 450 # Update window elements
window_height = 450
start_page.geometry(f'{window_width}x{window_height}')
start_page.resizable(0,0)
start_page.iconbitmap('icon_i8Q_icon.ico')
start_page.configure(bg="Slategray3")

t = ttk.Style()
t.configure('.', background="Slategray3") # Label background
t.configure('big.TButton', font=('Calibri','16')) # Button font
########################################################
# Header (ttk.Label, Static)
ttk.Label(start_page, text="PyPass", font=("Calibri", 45)).pack()
ttk.Label(start_page, text="Enter Password:", font=("Calibri", 20)).pack()

# Password Entry (ttk.Entry, Dynamic)
password_login = ttk.Entry(start_page, textvariable=tk.StringVar()) 
password_login.pack()

# Login Button (ttk.Button, Dynamic)
ttk.Button(start_page, text='Login', style='big.TButton',
            command= lambda: login(password_login.get(), error)).pack()

# Error Text (ttk.Label, Dynamic)
error = ttk.Label(start_page, text = '', font=("Calibri", 25))
error.pack()

ttk.Label(start_page, text = 'Note that the default password is \'123\'.\n Please change at your own discretion.', font=("Calibri", 15)).pack()
########################################################    
try:
    # modify DpiAwareness to improve readability of text
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    start_page.mainloop()