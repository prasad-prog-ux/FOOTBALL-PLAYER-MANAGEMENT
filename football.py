import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from PIL import Image, ImageTk  
import subprocess  # To open fb.py

# Database Configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'footy_db'
DB_PORT = 3308  # Use the correct port!

# Function to get database connection
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        charset='utf8'
    )

# Import user and admin windows (won't execute on import)
import user_window
import admin_window

def login():
    uname = username.get()
    pwd = password.get()

    if uname == "" or pwd == "":
        messagebox.showerror("Error", "Please fill in all details")
        return

    # **ADMIN LOGIN OVERRIDE**
    if uname == "MESSI" and pwd == "2022":
        messagebox.showinfo("Admin Login", "Welcome Admin MESSI!")
        root.destroy()  # Close login window
        subprocess.run(['python', 'fb.py'])  # Open fb.py
        return

    # **Database Authentication for Users**
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, pwd))
    result = cursor.fetchone()
    conn.close()

    if result:
        role = result[3]
        root.destroy()  # Close login page before opening user/admin panel
        if role == 'admin':
            admin_window.show()
        else:
            user_window.show()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def register():
    uname = username.get()
    pwd = password.get()
    r = role.get()

    if not r:
        messagebox.showwarning("Missing Role", "Please select a role")
        return

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (uname, pwd, r))
        conn.commit()
        messagebox.showinfo("Success", f"Registered as {r.capitalize()}")
    except:
        messagebox.showerror("Error", "Registration Failed. Username may already exist.")
    conn.close()

# Root Window
root = tk.Tk()
root.title("Footy Login")
root.geometry("1350x700+0+0")

# Background Image
bg_image = Image.open("back_fb.jpg")  
bg_image = bg_image.resize((1350, 700))  
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0)  

# Login Frame
loginFrame = tk.Frame(root, width=350, height=350, bg="#0f172a")
loginFrame.place(x=500, y=180)
loginFrame.pack_propagate(False)

# Title
tk.Label(loginFrame, text="Footy Login", font=("Helvetica", 24, 'bold'), fg="#22c55e", bg="#0f172a").pack(pady=20)

# Username & Password
username = tk.StringVar()
password = tk.StringVar()
role = tk.StringVar()

style = {'font': ("Helvetica", 14), 'bg': "#1e293b", 'fg': "#e2e8f0", 'insertbackground': 'white'}

tk.Entry(loginFrame, textvariable=username, **style, width=25, relief='flat').pack(pady=10)
tk.Entry(loginFrame, textvariable=password, show="*", **style, width=25, relief='flat').pack(pady=10)

# Role Dropdown
role_label = tk.Label(loginFrame, text="Select Role:", bg="#0f172a", fg="#cbd5e1", font=("Helvetica", 12))
role_label.pack(pady=(10, 0))
role_dropdown = ttk.Combobox(loginFrame, textvariable=role, values=["user", "admin"], font=("Helvetica", 12), state="readonly")
role_dropdown.pack(pady=5)

# Buttons
btn_style = {'font': ("Helvetica", 12), 'width': 20, 'padx': 10, 'pady': 5}
tk.Button(loginFrame, text="Login", bg="#22c55e", fg="white", command=login, **btn_style).pack(pady=10)
tk.Button(loginFrame, text="Register", bg="#1e293b", fg="#22c55e", command=register, **btn_style).pack(pady=5)

# Run
root.mainloop()
