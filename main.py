from tkinter import *
from tkinter import messagebox
import random
# import pyperclip
import json

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
SUGAR = '#f5f4f4'
RED = '#ef4339'
FONT_NAME = "Courier"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def pass_generator():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password = [random.choice(LETTERS) for _ in range(0, nr_letters)]
    password += [random.choice(SYMBOLS) for _ in range(0, nr_symbols)]
    password += [random.choice(NUMBERS) for _ in range(0, nr_numbers)]

    random.shuffle(password)
    password = ''.join(password)
    pyperclip.copy(password)
    if len(password_entry.get()) == 0:
        password_entry.insert(0, password)
    else:
        password_entry.delete(0, END)
        password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().title()
    email = email_entry.get().title()
    password = password_entry.get().title()

    new_data = {website: {
        'Email': email,
        'Password': password,
                     }
                }

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title='Oops', message="Please don't leave any fields empty!")
    else:
        try:
            with open('data.json', 'r') as file_data:
                data = json.load(file_data)
                data.update(new_data)
        except FileNotFoundError:
            with open('data.json', 'w') as file_data:
                json.dump(new_data, file_data, indent=4)
        except json.decoder.JSONDecodeError:
            with open('data.json', 'w') as file_data:
                json.dump(new_data, file_data, indent=4)
        else:
            with open('data.json', 'w') as file_data:
                json.dump(data, file_data, indent=4)   # dump takes many inputs : the most important is the dictionary
                # and the file that you want to write inside
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def search():
    website = website_entry.get().title()
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        with open('data.json', 'w') as file_data:
            pass
    except json.decoder.JSONDecodeError:
        messagebox.showwarning('Warning', 'File is Empty')
    else:
        if website in data.keys():
            idx = data[website]
            messagebox.showinfo(website, f'Email: {email_entry.get()}\nPassword: {idx["Password"]}')
        else:
            messagebox.showinfo('Error', f'Website is not saved')

    # with open('data.txt') as data_file:
    #     data = data_file.readlines()
    #     message = ""
    #     found = 0
    #     print(type(website_entry.get()))
    # for d in data[2:]:
    #     x = d.split()
    #     if x[0].title() == website_entry.get().title():
    #         message += f'Email: {email_entry.get()}\nPassword: {x[4]}\n\n'
    #         found += 1
    # if found > 0:
    #     messagebox.showinfo(website_entry.get(), message)


# ---------------------------- UI SETUP ------------------------------- #
# window:
window = Tk()
window.title('Password Manager')
window.config(padx=40, pady=40, bg=SUGAR)

# Password logo:
Pass_img = PhotoImage(file='logo.png')
logo = Canvas(width=200, height=200, bg=SUGAR, highlightthickness=0)
logo.create_image(100, 100, image=Pass_img)
logo.grid(column=1, row=0)

# Labels:
website_label = Label(text='Website:', font=('', 10), bg=SUGAR)
website_label.grid(column=0, row=1)

email_label = Label(text='Email/Username:', font=('', 10), bg=SUGAR)
email_label.grid(column=0, row=2)

password_label = Label(text='Password:', font=('', 10), bg=SUGAR)
password_label.grid(column=0, row=3)

# Entries:
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=39)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, 'Tuqa_aburaddaha@outlook.com')

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons:
generate_pass = Button(text='Generate Password', bg=SUGAR, fg=RED, width=14, command=pass_generator)
generate_pass.grid(row=3, column=2, sticky=W)

add_button = Button(text='Add', bg=SUGAR, fg=RED, width=35, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text='Search', bg=SUGAR, fg=RED, width=14, command=search)
search_button.grid(row=1, column=2, sticky=W)

window.mainloop()
