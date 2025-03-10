from tkinter import ttk
import tkinter as tk
import pymysql
from PIL import Image, ImageTk  
from tkinter import messagebox
import subprocess

# Function to handle Admin Login (opens fb.py after correct credentials)
def admin_login():
    # Show message prompting the admin to fill in the details
    messagebox.showinfo("Admin Login", "Please fill in the admin details")
    
    # Make the existing login form visible for the admin
    usernameLabel.config(text="Admin Username")  # Change label text to Admin Username
    passwordLabel.config(text="Admin Password")  # Change label text to Admin Password
    loginbutton.config(command=verify_admin_credentials)  # Modify the login button to verify admin credentials

# Function to verify Admin Credentials (with the existing form)
def verify_admin_credentials():
    admin_username = usernamentry.get()
    admin_password = passwordentry.get()

    # Admin credentials (replace with your actual admin credentials)
    if admin_username == "MESSI" and admin_password == "10":
        messagebox.showinfo("Success", "Admin Login Successful")
        subprocess.run(['python', 'fb.py'])  # Open fb.py after successful login
    else:
        # Sophisticated message when incorrect admin credentials are entered
        messagebox.showerror("Access Denied", 
                             "You're not an admin. Please try User Login instead.")
        # Optionally, reset the fields or leave them as they are for further attempts
        usernamentry.delete(0, tk.END)
        passwordentry.delete(0, tk.END)

# Function to handle User Login (opens sign_in.py)
def user_login():
    subprocess.run(['python', 'signin.py'])  # Opens sign_in.py for User
    
# Function to handle login (for the main window)
def login():
    if usernamentry.get() == "" or passwordentry.get() == "":
        messagebox.showerror("Error", "Please fill the details")
    elif usernamentry.get() == "MESSI" and passwordentry.get() == "10":
        messagebox.showinfo("FOOTBALL PLAYER STATISTICS", "WELCOME") 
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Setting up the main window
window = tk.Tk()
window.title("FOOTBALL PLAYER STATISTICS")
window.geometry("1350x700+0+0")

# Background Image
background = Image.open("back_fb.jpg")  
background = background.resize((1350, 700))  
background = ImageTk.PhotoImage(background)
bgLabel = tk.Label(window, image=background)
bgLabel.place(x=0, y=0)  
bgLabel.image = background  

# Frame for login form
loginFrame = tk.Frame(window, width=300, height=200, bg="white")
loginFrame.place(x=525, y=250)  
loginFrame.pack_propagate(False)

# Logo Image
logoImage = tk.PhotoImage(file="football.png")
logolabel = tk.Label(loginFrame, image=logoImage)
logolabel.grid(row=0, column=0, columnspan=2, padx=10)

# Username input field
usernameimage = tk.PhotoImage(file="user.png")
usernameLabel = tk.Label(loginFrame, image=usernameimage, text="Username", compound="left", font=("times new roman", 20, "bold"))
usernameLabel.grid(row=1, column=0, padx=10)
usernamentry = tk.Entry(loginFrame, font=("times new roman", 20, "bold"), bd=7, width=15)
usernamentry.grid(row=1, column=1)

# Password input field
passwordimage = tk.PhotoImage(file="padlock.png")
passwordLabel = tk.Label(loginFrame, image=passwordimage, text="Password", compound="left", font=("times new roman", 20, "bold"))
passwordLabel.grid(row=2, column=0, padx=10)
passwordentry = tk.Entry(loginFrame, font=("times new roman", 20, "bold"), bd=7, width=15)
passwordentry.grid(row=2, column=1)

# Main Login Button (Initially handles the user login)
loginbutton = tk.Button(loginFrame, text="Login", font=("times new roman", 10, "bold"), width=12, fg="white", bg="royal blue", cursor="hand2", command=login)
loginbutton.grid(row=3, column=1, pady=10)

# Admin Login Button (opens Admin login form first)
admin_login_button = tk.Button(loginFrame, text="Admin Login", font=("times new roman", 10, "bold"), width=12, fg="white", bg="dark green", cursor="hand2", command=admin_login)
admin_login_button.grid(row=4, column=0, pady=10)

# User Login Button (opens sign_in.py)
user_login_button = tk.Button(loginFrame, text="User Login", font=("times new roman", 10, "bold"), width=12, fg="white", bg="dark red", cursor="hand2", command=user_login)
user_login_button.grid(row=4, column=1, pady=10)

# Run the GUI
window.mainloop()
