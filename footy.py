import tkinter as tk
from tkinter import messagebox, ttk  # Added ttk for progress bar
import mysql.connector
from PIL import Image, ImageTk  
import subprocess  # To run external Python scripts

# Database Configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'footy_db'
DB_PORT = 3308  


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        charset='utf8'
    )


def admin_login():
    uname = username.get()
    pwd = password.get()

    if uname == "MESSI" and pwd == "2022":
        messagebox.showinfo("Admin Login", "Welcome Admin !")
        root.destroy()  # Close login window
        subprocess.run(['python', 'fbupdate.py'])  # Open admin panel
    else:
        messagebox.showerror("Login Failed", "Invalid Admin Credentials")


def open_signup_login():
    root.destroy() 
    try:
        subprocess.run(['python', 'signin.py'])  
    except FileNotFoundError:
        messagebox.showerror("Error", "signin.py file not found! Make sure it's in the same directory.")


def show_progress():
    loading_label = tk.Label(root, text="Loading...", font=("Helvetica", 20, "bold"), fg="#22c55e", bg="#0f172a")
    loading_label.place(relx=0.5, rely=0.4, anchor="center")  

    progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", style="green.Horizontal.TProgressbar")
    progress.place(relx=0.5, rely=0.5, anchor="center")  
    root.update()

    for i in range(101):
        progress["value"] = i
        root.update_idletasks()
        root.after(30)  

    loading_label.destroy()
    progress.destroy()
    show_login_frame()  


def show_login_frame():
    global username, password

    # Login Frame
    loginFrame = tk.Frame(root, width=350, height=400, bg="#0f172a")
    loginFrame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame
    loginFrame.pack_propagate(False)

    # Title
    tk.Label(loginFrame, text="Footy Stats Login", font=("Helvetica", 24, 'bold'), fg="#22c55e", bg="#0f172a").pack(pady=20)

    # Username & Password Fields
    username = tk.StringVar()
    password = tk.StringVar()

    style = {'font': ("Helvetica", 14), 'bg': "#1e293b", 'fg': "#e2e8f0", 'insertbackground': 'white'}

    tk.Label(loginFrame, text="Username:", font=("Helvetica", 12), bg="#0f172a", fg="#cbd5e1").pack(pady=(5, 0))
    tk.Entry(loginFrame, textvariable=username, **style, width=25, relief='flat').pack(pady=5)

    tk.Label(loginFrame, text="Password:", font=("Helvetica", 12), bg="#0f172a", fg="#cbd5e1").pack(pady=(10, 0))
    tk.Entry(loginFrame, textvariable=password, show="*", **style, width=25, relief='flat').pack(pady=5)

    # Buttons for Admin and User Login
    btn_style = {'font': ("Helvetica", 12), 'width': 20, 'padx': 10, 'pady': 5}

    tk.Button(loginFrame, text="Admin Login", bg="#dc2626", fg="white", command=admin_login, **btn_style).pack(pady=10)
    tk.Button(loginFrame, text="User Login", bg="#22c55e", fg="white", command=open_signup_login, **btn_style).pack(pady=5)

# Root Window
root = tk.Tk()
root.title("Footy Login")
root.geometry("1350x700+0+0")


style = ttk.Style()
style.theme_use("clam")
style.configure("green.Horizontal.TProgressbar", troughcolor="#1e293b", background="#22c55e", thickness=10)


bg_image = Image.open("back_fb.jpg")  
bg_image = bg_image.resize((1350, 700))  
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.image = bg_photo
bg_label.place(x=0, y=0)  

#for progrwess
show_progress()

# Run
root.mainloop()
