from tkinter import *
import pymysql
import re
from tkinter import messagebox
from PIL import Image, ImageTk

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def is_valid_password(password):
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'  # Minimum 8 chars, at least 1 letter and 1 number
    return re.match(pattern, password)

def clear():
    emailEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirmEntry.delete(0, END)  
    check.set(0)

def connect_database():
    email = emailEntry.get()
    username = usernameEntry.get()
    password = passwordEntry.get()
    confirm_password = confirmEntry.get()  

    if not email or not username or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required")
        return
    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email format")
        return
    if not is_valid_password(password):
        messagebox.showerror("Error", "Password must be at least 8 characters long and include both letters and numbers")
        return
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return
    if check.get() == 0:
        messagebox.showerror("Error", "Please accept Terms & Conditions")
        return

    try:
        con = pymysql.connect(host="localhost", user="root", password="root")
        mycursor = con.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS userdata")
        mycursor.execute("USE userdata")
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(50),
                username VARCHAR(100),
                password VARCHAR(15)
            )
        """)
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {str(e)}")
        return

    mycursor.execute("SELECT * FROM data WHERE username=%s", (username,))
    if mycursor.fetchone():
        messagebox.showerror("Error", "Username already exists")
    else:
        mycursor.execute("INSERT INTO data (email, username, password) VALUES (%s, %s, %s)", (email, username, password))
        con.commit()
        con.close()
        messagebox.showinfo("Success", "Registration successful")
        clear()
        signup_window.destroy()
        import signin

def login_page():
    signup_window.destroy()
    import signin

signup_window = Tk()
signup_window.title("Signup Page")
signup_window.geometry("990x660+50+50")
signup_window.resizable(0, 0)
signup_window.configure(bg="#0f172a")


bg_image = Image.open("football1.jpg")
bg_image = bg_image.resize((990, 660), Image.LANCZOS)
background = ImageTk.PhotoImage(bg_image)

# Set Background Image
bgLabel = Label(signup_window, image=background)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

frame = Frame(signup_window, bg="#0f172a")
frame.place(x=554, y=100)

heading = Label(frame, text="CREATE AN ACCOUNT", font=("Helvetica", 24, "bold"), bg="#0f172a", fg="#22c55e")
heading.grid(row=0, column=0, padx=10, pady=10)

# Email
emailLabel = Label(frame, text="Email", font=("Helvetica", 10, "bold"), bg="#0f172a", fg="#22c55e")
emailLabel.grid(row=1, column=0, sticky="w", padx=25, pady=(10, 0))
emailEntry = Entry(frame, width=25, font=("Helvetica", 10, "bold"), fg="white", bg="#1e293b", bd=0)
emailEntry.grid(row=2, column=0, sticky="w", padx=25)

frame1 = Frame(frame, width=250, height=2, bg="#22c55e")
frame1.grid(row=3, column=0, sticky="w", padx=25)

# Username
usernameLabel = Label(frame, text="Username", font=("Helvetica", 10, "bold"), bg="#0f172a", fg="#22c55e")
usernameLabel.grid(row=4, column=0, sticky="w", padx=25, pady=(10, 0))
usernameEntry = Entry(frame, width=25, font=("Helvetica", 10, "bold"), fg="white", bg="#1e293b", bd=0)
usernameEntry.grid(row=5, column=0, sticky="w", padx=25)

frame2 = Frame(frame, width=250, height=2, bg="#22c55e")
frame2.grid(row=6, column=0, sticky="w", padx=25)

# Password
passwordLabel = Label(frame, text="Password", font=("Helvetica", 10, "bold"), bg="#0f172a", fg="#22c55e")
passwordLabel.grid(row=7, column=0, sticky="w", padx=25, pady=(10, 0))
passwordEntry = Entry(frame, width=25, font=("Helvetica", 10, "bold"), fg="white", bg="#1e293b", bd=0, show="*")
passwordEntry.grid(row=8, column=0, sticky="w", padx=25)

frame3 = Frame(frame, width=250, height=2, bg="#22c55e")
frame3.grid(row=9, column=0, sticky="w", padx=25)


confirmLabel = Label(frame, text="Confirm Password", font=("Helvetica", 10, "bold"), bg="#0f172a", fg="#22c55e")
confirmLabel.grid(row=10, column=0, sticky="w", padx=25, pady=(10, 0))
confirmEntry = Entry(frame, width=25, font=("Helvetica", 10, "bold"), fg="white", bg="#1e293b", bd=0, show="*")
confirmEntry.grid(row=11, column=0, sticky="w", padx=25)

frame4 = Frame(frame, width=250, height=2, bg="#22c55e")
frame4.grid(row=12, column=0, sticky="w", padx=25)

# Terms 
check = IntVar()
terms = Checkbutton(frame, text="I agree to Terms & Conditions", font=("Helvetica", 9, "bold"), fg="#22c55e", bg="#0f172a", variable=check)
terms.grid(row=13, column=0, padx=15, pady=10)

signupButton = Button(frame, text="Signup", font=("Open Sans", 9, "bold"), width=17, bg="#22c55e", fg="#0f172a", command=connect_database)
signupButton.grid(row=14, column=0, pady=10)

loginButton = Button(frame, text="Log in", font=("Open Sans", 9, "bold underline"), bg="#0f172a", fg="#22c55e", command=login_page)
loginButton.grid(row=15, column=0, sticky="e", padx=25, pady=10)

signup_window.mainloop()
