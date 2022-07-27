from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
import os, sys

root = Tk()
root.title('Khanda Paper')
root.geometry("1200x660")

# Set Var for Open File Name
global open_status_name
open_status_name = False

global selected
selected = False

# Create New File Function
def new_file():
    # Delete Prev. Text
    my_text.delete("1.0", END)
    # Update Status Bars
    root.title('New File - Khanda Paper')
    status_bar.config(text="New File        ")

    global open_status_name
    open_status_name = False

# Create Open File Function
def open_file():
    # Delete Prev. Text
    my_text.delete("1.0", END)

    # Grab Filename
    text_file = filedialog.askopenfilename(initialdir="C:/Documents", title="Open File", filetype=(("Text Files", "*.txt"),("All Files", "*.*")))

# Check File name
    if text_file:
        # Make Filename Global to Access
       global open_status_name
       open_status_name = text_file

    # Update Status Bars
    name = text_file
    status_bar.config(text=f'{name}        ')
    name = name.replace("C:/Documents/", "")
    root.title(f'{name} - Khanda Paper')

    # Open the File
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    # Add File to TextBox
    my_text.insert(END, stuff)

    # Close the Opened File
    text_file.close()

# Save As File
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/Documents", title="Save File", filetypes=(("Text Files", "*.txt"),("All Files", "*.*")))
    if text_file:
        # Update Status Bars
        name = text_file
        status_bar.config(text=f'Saved: {name}        ')
        name = name.replace("C:/Documents/", "")
        root.title(f'{name} - Khanda Paper')

        # Save The File
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        # Close the File
        text_file.close()

# Cut Text
def cut_text(e):
    global selected
    # Check for Keyboard shortcut
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            # Grab Selected Text
            selected = my_text.selection_get()
            # Delete Selected Text
            my_text.delete("sel.first", "sel.last")
            # Clear Clipboard
            root.clipboard_clear()
            root.clipboard_append(selected)

# Copy Text
def copy_text(e):
    global selected
    # Check For Keyboard shortcut
    if e:
        selected = root.clipboard_get()
    if my_text.selection_get():
         # Grab Selected Text
        selected = my_text.selection_get()
        # Clear Clipboard
        root.clipboard_clear()
        root.clipboard_append(selected)

# Paste Text
def paste_text(e):
    global selected
    # Check For Copied Text
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)

# Save File
def save_file():
    global open_status_name
    if open_status_name:
        # Save The File
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        # Close the File
        text_file.close()
        # Popup code
        status_bar.config(text=f'Saved: {open_status_name}        ')
    else:
        save_as_file()

# Bold Text
def bold_it():
    # Create Our Font
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")

    # Configure a Tag
    my_text.tag_configure("bold", font=bold_font)

    # Define Current Tags
    current_tags = my_text.tag_names("sel.first")

    # Is the tag set?
    if "bold" in current_tags:
        my_text.tag_remove("bold", "sel.first", "sel.last")
    else:
        my_text.tag_add("bold", "sel.first", "sel.last")

# Italic Text
def italic_it():
    # Create Our Font
    italics_font = font.Font(my_text, my_text.cget("font"))
    italics_font.configure(slant="italic")

    # Configure a Tag
    my_text.tag_configure("italic", font=italics_font)

    # Define Current Tags
    current_tags = my_text.tag_names("sel.first")

    # Is the tag set?
    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")
    else:
        my_text.tag_add("italic", "sel.first", "sel.last")

# Select all
def select_all():
    # Add sel Tag
    my_text.tag_add('sel', '1.0', 'end')

# Clear all
def clear_all():
    my_text.delete(1.0, END)

# Create Toolbar
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

# Create the main frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Create Scrollbar for Textbox
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Create Text Box
my_text = Text(my_frame, width=98, height=25, font=("Arial", 18), selectbackground="#e8e7e9", selectforeground="#3b3041", undo=True, yscrollcommand=text_scroll.set,)
my_text.pack()

# Configure ScrollBar
text_scroll.configure(command=my_text.yview)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add File Menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Add Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut   ", command=lambda: cut_text(False), accelerator="Ctrl+X")
edit_menu.add_command(label="Copy   ", command=lambda: copy_text(False), accelerator="Ctrl+C")
edit_menu.add_command(label="Paste   ", command=lambda: paste_text(False), accelerator="Ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="Undo   ", command=my_text.edit_undo, accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo   ", command=my_text.edit_redo, accelerator="Ctrl+Y")
edit_menu.add_separator()
edit_menu.add_command(label="Select All   ", command=select_all, accelerator="Ctrl+A")
edit_menu.add_command(label="Clear   ", command=clear_all,)

# Add Status bar to Bottom of app
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

# Edit Bindings
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)
# Select Bindings
root.bind('<Control-Key-a>', select_all)

# Create Button

# Bold Button
bold_button = Button(toolbar_frame, text="𝗕", command=bold_it)
bold_button.grid(row=0, column=0, sticky=W, padx=3)
# Italic Button
italic_button = Button(toolbar_frame, text="𝘐", command=italic_it)
italic_button.grid(row=0, column=1, padx=3)

# Undo/Redo Button
undo_button = Button(toolbar_frame, text="⟲", command=my_text.edit_undo)
undo_button.grid(row=0, column=2, padx=3)
# Italic Button
redo_button = Button(toolbar_frame, text="⟳", command=my_text.edit_redo)
redo_button.grid(row=0, column=3, padx=3)

root.mainloop()