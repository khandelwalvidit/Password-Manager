from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json
import os, sys

BACKGROUND = "#fffae7"
WHITE = "#ffffff"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_add = [choice(letters) for _ in range(randint(8, 10))]
    symbols_add = [choice(symbols) for _ in range(randint(2, 4))]
    numbers_add = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = letters_add + numbers_add + symbols_add

    shuffle(password_list)

    password = "".join(password_list)
    password_input.delete(0, END)
    password_input.insert(0, f"{password}")
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": username,
            "password": password
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title=" Oops ", message=" Please don't leave any fields empty")
    else:
        is_ok = messagebox.askokcancel(title="Confirm the Info",
                                       message=f" Website: {website}\n\n Username:  {username}\n\n "
                                               f"Password:  {password}\n\n Do you want to save?")
        if is_ok:
            try:
                with open(file="password_data.json", mode="r") as data_file:
                    # Read data into data variable
                    data = json.load(data_file)
            except FileNotFoundError:
                with open(file="password_data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                with open(file="password_data.json", mode="w") as data_file:
                    # Appending the data file
                    data.update(new_data)
                    # Saving the data into json file
                    json.dump(data, data_file, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)


# ---------------------------- Search ------------------------------- #
def search_password():
    website = str(website_input.get())
    if len(website) == 0:
        messagebox.showerror(title="Oops", message="Please Enter Website")
    else:
        try:
            with open(file="password_data.json", mode="r") as search_data:
                json_data = json.load(search_data)

        except:
            messagebox.showerror(title="Error", message="No Data file found")
        else:
            if website in json_data:
                email = json_data[website]["email"]
                password = json_data[website]["password"]
                messagebox.showinfo(f"{website}", f" Email: {email}\n\n Password: {password}")
                pyperclip.copy(password)
            else:
                messagebox.showerror(title="Unknown website", message="Website not saved")


# ---------------------------- UI SETUP ------------------------------- #

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


window = Tk()
window.title("Password Manager")
window.config(padx=66, pady=66, bg=BACKGROUND)

canvas = Canvas(width=200, height=200, highlightthickness=0, bg=BACKGROUND)
lock_img = PhotoImage(file=resource_path("logo.png"))
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# Website
website_label = Label(text="Website:", font=("Arial", 15), padx=20, pady=5, bg=BACKGROUND)
website_label.grid(row=1, column=0)

website_input = Entry(width=38, font=("Arial", 15))
website_input.grid(row=1, column=1)
website_input.focus()

# Username

username_label = Label(text="Email/Username:", font=("Arial", 15), padx=20, pady=10, bg=BACKGROUND)
username_label.grid(row=3, column=0)

username_input = Entry(width=49, font=("Arial", 15))
username_input.grid(row=3, column=1, columnspan=2)

# Password
password_label = Label(text="password:", font=("Arial", 15), padx=20, pady=10, bg=BACKGROUND)
password_label.grid(row=4, column=0)

password_input = Entry(width=38, font=("Arial", 15))
password_input.grid(row=4, column=1)

generate_password_button = Button(text="Generate Password", width=14, padx=10, bg=WHITE, font=("Arial", 9, "bold"),
                                  command=password_generator)
generate_password_button.grid(row=4, column=2)

# Add button
add_button = Button(text="Add", width=77, pady=5, bg=WHITE, font=("Arial", 9, "bold"), command=save_data)
add_button.grid(row=5, column=1, columnspan=2)

# Search button

search_button = Button(text="Search", width=14, padx=10, bg=WHITE, font=("Arial", 9, "bold"),
                       command=search_password)
search_button.grid(row=1, column=2)

window.mainloop()
