from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip
import json

# change this how you please
DEFAULT_EMAIL = 'USERNAME@email.com'


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password() -> None:
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    Password = ''.join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, Password)
    pyperclip.copy(Password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_login() -> None:
    website: str = website_entry.get()
    username: str = username_entry.get()
    password: str = password_entry.get()

    new_data: dict = {
        website: {
            'username': username,
            'password': password,
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title='ERROR', message='No empty fields.')
    else:
        try:
            with open('data.json', 'r') as file:
                try:
                    data: dict = json.load(file)
                except json.decoder.JSONDecodeError:
                    data: dict = {}
        except FileNotFoundError:
            data: dict = {}
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)

        data.update(new_data)

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
            website_entry.delete(0, END)
            password_entry.delete(0, END)

    website_entry.focus()


# ---------------------------- SEARCH LOGIN ------------------------------- #
def find_password() -> None:
    try:
        with open('data.json', 'r') as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {}
    except FileNotFoundError:
        messagebox.showerror(title='ERROR', message='No Data File found.')
    else:
        website: str = website_entry.get()
        if website in data:
            messagebox.showinfo(title=website, message=f"Username: {data[website]['username']}\n"
                                                       f"Password: {data[website]['password']}")
        elif website == '':
            messagebox.showerror(title='ERROR', message='Please input a website.')
        else:
            messagebox.showerror(title='ERROR', message=f"{website} doesn't exist in our database.")
    finally:
        website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)
window.minsize(height=200, width=200)

# --- CANVAS --- #
canvas = Canvas(width=200, height=200, highlightthickness=0, )
logo_img = PhotoImage(file='lock.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# --- LABELS --- #
website_label = Label(text='Website:')
website_label.grid(row=1, column=0, sticky='E')

login_name_label = Label(text='Email/Username:')
login_name_label.grid(row=2, column=0, sticky='E')

password_label = Label(text='Password:')
password_label.grid(row=3, column=0, sticky='E')

# --- ENTRIES --- #
website_entry = Entry(width=32)
website_entry.grid(row=1, column=1, sticky='W')
website_entry.focus()

username_entry = Entry()
username_entry.grid(row=2, column=1, columnspan=2, sticky='EW')
username_entry.insert(0, DEFAULT_EMAIL)

password_entry = Entry(width=32)
password_entry.grid(row=3, column=1, sticky='W')

# --- BUTTONS --- #
search_button = Button(text='Search', bg='DarkGoldenrod', fg='floral white', command=find_password)
search_button.grid(row=1, column=2, sticky='EW')

generate_button = Button(text='Generate Password', bg='medium sea green', fg='floral white', command=generate_password)
generate_button.grid(row=3, column=2, sticky='EW')

add_login_button = Button(text='Add', bg='IndianRed1', fg='floral white', command=save_login)
add_login_button.grid(row=4, column=1, columnspan=2, sticky='EW')

window.bind('<Return>', lambda event=None: save_login())

window.mainloop()
