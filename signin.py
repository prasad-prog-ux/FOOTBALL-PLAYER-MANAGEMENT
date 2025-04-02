from tkinter import *

import os  
from tkinter import messagebox
import pymysql
from PIL import Image, ImageTk
import subprocess  # To run another python script

def login_page():
    signup_page.destroy()
    import footy

def forget_password():
    def new_password():
        if username_entry.get() == "" or passwordnew_entry.get() == "" or confirmpass_entry.get() == "":
            messagebox.showerror("Error", "All Fields are Required", parent=window)
        elif passwordnew_entry.get() != confirmpass_entry.get():
            messagebox.showerror("Error", "Password and confirm password are not same", parent=window)
        else:
            con = pymysql.connect(host="localhost", user="root", password="root", database="userdata")
            mycursor = con.cursor()
            query = "SELECT * FROM data WHERE username = %s"
            mycursor.execute(query, (username_entry.get(),))
            row = mycursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Incorrect username", parent=window)
            else:
                query = "UPDATE data SET password=%s WHERE username=%s" 
                mycursor.execute(query, (passwordnew_entry.get(), username_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Password changed successfully", parent=window)
                window.destroy()  # Ensure the window closes after success

    window = Toplevel()
    window.title("Change Password")
    window.configure(bg="#0f172a")  
    window.geometry("400x400")

    heading_label = Label(window, text="RESET PASSWORD", font=("Helvetica", 24, "bold"), bg="#0f172a", fg="#22c55e")
    heading_label.place(x=60, y=20)

    username_label = Label(window, text="Username", font=("Helvetica", 14, "bold"), bg="#0f172a", fg="#22c55e")
    username_label.place(x=30, y=80)

    username_entry = Entry(window, width=25, font=("Helvetica", 14, "bold"), fg="#22c55e", bg="#0f172a", bd=0)
    username_entry.place(x=30, y=110)

    passwordnew_label = Label(window, text="New Password", font=("Helvetica", 14, "bold"), bg="#0f172a", fg="#22c55e")
    passwordnew_label.place(x=30, y=150)

    passwordnew_entry = Entry(window, width=25, font=("Helvetica", 14, "bold"), fg="#22c55e", bg="#0f172a", bd=0)
    passwordnew_entry.place(x=30, y=180)

    confirmpass_label = Label(window, text="Confirm Password", font=("Helvetica", 14, "bold"), bg="#0f172a", fg="#22c55e")
    confirmpass_label.place(x=30, y=220)

    confirmpass_entry = Entry(window, width=25, font=("Helvetica", 14, "bold"), fg="#22c55e", bg="#0f172a", bd=0)
    confirmpass_entry.place(x=30, y=250)

    submitButton = Button(window, text="Submit", fg="white", bg="#22c55e", font=("Helvetica", 16, "bold"), 
                          activebackground="lightgreen", cursor="hand2", bd=0, width=19, command=new_password)
    submitButton.place(x=30, y=300)


def login_user():
    if usernameEntry.get() == "" or passwordEntry.get() == "":
        messagebox.showerror("Error", "All Fields are Required")
    else:
        try:
            con = pymysql.connect(host="localhost", user="root", password="root")
            mycursor = con.cursor()
        except:
            messagebox.showerror("Error", "Connection is not established, try again")
            return

        query = "use userdata"
        mycursor.execute(query)
        query = "select * from data where username=%s and password=%s"
        mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
        row = mycursor.fetchone()
        if row is None:
            messagebox.showerror("Error", "Invalid username or password")
        else:
            messagebox.showinfo("Success", "Login is successful") 
            login_window.destroy()
            import user_window
            user_window.mainloop()  

def signup_page():
    login_window.destroy()
    import signup

def hide():
    passwordEntry.config(show="*")
    eyeButton.config(image=closeeye, command=show)

def show():
    passwordEntry.config(show="")
    eyeButton.config(image=openeye, command=hide)

def user_enter(event):
    if usernameEntry.get() == "Username":
        usernameEntry.delete(0, END)
        usernameEntry.config(fg="#22c55e")

def password_enter(event):
    if passwordEntry.get() == "Password":
        passwordEntry.delete(0, END)
        passwordEntry.config(show="*", fg="#22c55e")

def password_leave(event):
    if passwordEntry.get() == "":
        passwordEntry.insert(0, "Password")
        passwordEntry.config(show="", fg="#22c55e")

login_window = Tk()
login_window.geometry("990x660+50+50")
login_window.resizable(0, 0)
login_window.title("Login Page")
login_window.configure(bg="#0f172a")
bg_image = Image.open("back.jpg")  
bg_image = bg_image.resize((990, 660), Image.LANCZOS)
background = ImageTk.PhotoImage(bg_image)


bg_label = Label(login_window, image=background)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

headingLabel = Label(login_window, text="USER LOGIN", font=("Helvetica", 24, "bold"),
                     bg="#0f172a", fg="#22c55e")
headingLabel.place(x=615, y=120)

usernameEntry = Entry(login_window, width=20, font=("Helvetica", 14),
                      bd=0, fg="#22c55e", bg="#0f172a")
usernameEntry.place(x=580, y=200)
usernameEntry.insert(0, "Username")
usernameEntry.bind("<FocusIn>", user_enter)

frame1 = Frame(login_window, width=250, height=2, bg="#22c55e")
frame1.place(x=580, y=222)

passwordEntry = Entry(login_window, width=20, font=("Helvetica", 14),
                      bd=0, fg="#22c55e", bg="#0f172a")
passwordEntry.place(x=580, y=260)
passwordEntry.insert(0, "Password")
passwordEntry.bind("<FocusIn>", password_enter)
passwordEntry.bind("<FocusOut>", password_leave)

frame2 = Frame(login_window, width=250, height=2, bg="#22c55e")
frame2.place(x=580, y=282)

openeye = ImageTk.PhotoImage(file="openeye.png")
closeeye = ImageTk.PhotoImage(file="closeye.png")

eyeButton = Button(login_window, image=openeye, bd=0, bg="#0f172a",
                   activebackground="#0f172a", cursor="hand2", command=hide)
eyeButton.place(x=800, y=255)

forgetButton = Button(login_window, text="Forget Password?", bd=0, bg="#0f172a",
                      font=("Helvetica", 10), fg="#22c55e", cursor="hand2", command=forget_password)
forgetButton.place(x=715, y=295)

loginButton = Button(login_window, text="Login", fg="white", bg="#22c55e",
                     font=("Helvetica", 16, "bold"), cursor="hand2", bd=0, width=19, command=login_user)
loginButton.place(x=578, y=350)

signupLabel = Label(login_window, text="Don't have an account?", font=("Helvetica", 9, "bold"),
                    fg="#22c55e", bg="#0f172a")
signupLabel.place(x=590, y=500)

newButton = Button(login_window, text="Create an account", fg="blue", bg="#0f172a",
                   font=("Helvetica", 9, "bold underline"), cursor="hand2", bd=0, command=signup_page)
newButton.place(x=727, y=500)

login_window.mainloop()
