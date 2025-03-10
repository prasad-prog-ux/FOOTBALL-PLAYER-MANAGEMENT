from tkinter import *
from PIL import ImageTk
import os  
from tkinter import messagebox
import pymysql
import subprocess  # To run another python script

def forget_password():
    def new_password():
        if user_enter.get()==" " or new_password.get()=="" or confirmpass_entry.get()=="":
            messagebox.showerror("Error","All Fields are Required", parent=window)
        elif new_password.get()!=confirmpass_entry.get():
            messagebox.showerror("Error", "Password and confirm password are not same", parent=window)
        else:
            con = pymysql.connect(host="localhost", user="root", password="root", database="userdata")
            mycursor = con.cursor()
            query = "select * from data where username =%s"
            mycursor.execute(query, (user_enter.get()))
            row = mycursor.fetchone()
            if row == None:
                messagebox.showerror("Error", "Incorrect username", parent=window)
            else:
                query = "update data set password=%s where username=%s" 
                mycursor.execute(query, (new_password.get(), user_enter.get()))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Password changed successfully")
                window.destroy()

    window = Toplevel()
    window.title("Change Password")

    bgpic = ImageTk.PhotoImage(file="background.png")
    bglabel = Label(window, image=bgpic) 
    bglabel.grid()
    heading_label = Label(window, text="RESET PASSWORD", font=("arial", 18, "bold"), bg="white", fg="magenta2")
    heading_label.place(x=480, y=60)

    username_label = Label(window, text="Username", font=("arial", 11, "bold"), bg="white", fg="orchid1")
    username_label.place(x=470, y=130)

    username_entry = Entry(window, width=25, font=("arial", 11, "bold"), fg="magenta2", bd=0)
    username_entry.place(x=470, y=160)

    frame = Frame(window, width=250, height=2, bg="orchid1")
    frame.place(x=470, y=180)

    passwordnew_label = Label(window, text="New Password", font=("arial", 12, "bold"), bg="white", fg="orchid1")
    passwordnew_label.place(x=470, y=210)

    passwordnew_entry = Entry(window, width=25, font=("arial", 11, "bold"), fg="magenta2", bd=0)
    passwordnew_entry.place(x=470, y=240)

    confirmpass_label = Label(window, text="Confirm Password", font=("arial", 12, "bold"), bg="white", fg="orchid1")
    confirmpass_label.place(x=470, y=290)

    confirmpass_entry = Entry(window, width=25, font=("arial", 11, "bold"), fg="magenta2", bd=0)
    confirmpass_entry.place(x=470, y=320)

    submitButton = Button(window, text="Submit", fg="white", bg="firebrick1", activebackground="magenta2",
                     font=("Open Sans", 16, "bold"), activeforeground="white", 
                     cursor="hand2", bd=0, width=19, command=new_password)
    submitButton.place(x=470, y=390)

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
        if row == None:
            messagebox.showerror("Error", "Invalid username or password")
        else:
            messagebox.showinfo("Success", "Login is successful") 
            login_window.destroy()  # Close the login window
            
            # Open the user panel window
            import user_panel  # Assuming your user panel code is in user_panel.py
            user_panel.panel_window.mainloop()   

def signup_page():
    login_window.destroy()
    try:
        import signup  # Ensure signup.py exists in the same directory
    except ImportError:
        print("Error: signup.py not found!")

def hide():
    passwordEntry.config(show="*")
    eyeButton.config(image=closeeye, command=show)

def show():
    passwordEntry.config(show="")
    eyeButton.config(image=openeye, command=hide)

def user_enter(event):
    if usernameEntry.get() == "Username":
        usernameEntry.delete(0, END)
        usernameEntry.config(fg="black")

def password_enter(event):
    if passwordEntry.get() == "Password":
        passwordEntry.delete(0, END)
        passwordEntry.config(show="*", fg="black")

def password_leave(event):
    if passwordEntry.get() == "":
        passwordEntry.insert(0, "Password")
        passwordEntry.config(show="", fg="firebrick1")

# Initialize main window
login_window = Tk()
login_window.geometry("990x660+50+50")
login_window.resizable(0, 0)
login_window.title("Login Page")

# Load images safely
def load_image(file):
    if os.path.exists(file):
        return ImageTk.PhotoImage(file=file)
    else:
        print(f"Warning: {file} not found!")
        return None  # Returns None if file is missing

bgImage = load_image("bg.jpg")
if bgImage:
    bglabel = Label(login_window, image=bgImage)
    bglabel.place(x=0, y=0)

headingLabel = Label(login_window, text="USER LOGIN", font=("Microsoft Yahei UI Light", 23, "bold"),
                     bg="white", fg="firebrick1")
headingLabel.place(x=615, y=120)

# Username Entry
usernameEntry = Entry(login_window, width=20, font=("Microsoft Yahei UI Light", 14),
                      bd=0, fg="firebrick1")
usernameEntry.place(x=580, y=200)
usernameEntry.insert(0, "Username")
usernameEntry.bind("<FocusIn>", user_enter)

frame1 = Frame(login_window, width=250, height=2, bg="firebrick1")
frame1.place(x=580, y=222)

# Password Entry
passwordEntry = Entry(login_window, width=20, font=("Microsoft Yahei UI Light", 14),
                      bd=0, fg="firebrick1")
passwordEntry.place(x=580, y=260)
passwordEntry.insert(0, "Password")
passwordEntry.bind("<FocusIn>", password_enter)
passwordEntry.bind("<FocusOut>", password_leave)

frame2 = Frame(login_window, width=250, height=2, bg="firebrick1")
frame2.place(x=580, y=282)

# Load Eye Icons
openeye = load_image("openeye.png")
closeeye = load_image("closeye.png")

if openeye and closeeye:
    eyeButton = Button(login_window, image=openeye, bd=0, bg="white",
                       activebackground="white", cursor="hand2", command=hide)
    eyeButton.place(x=800, y=255)

# Forgot Password
forgetButton = Button(login_window, text="Forget Password?", bd=0, bg="white",
                      activebackground="white", cursor="hand2",
                      font=("Microsoft Yahei UI Light", 10),
                      fg="firebrick1", activeforeground="firebrick1", command=forget_password )
forgetButton.place(x=715, y=295)

# Login Button
loginButton = Button(login_window, text="Login", fg="white", bg="firebrick1",
                     activebackground="firebrick1",
                     font=("Open Sans", 16, "bold"), activeforeground="white",
                     cursor="hand2", bd=0, width=19, command=login_user)
loginButton.place(x=578, y=350)

# OR Label
orlabel = Label(login_window, text="--------------OR-----------------", font=("Open Sans", 16),
                fg="firebrick1", bg="white")
orlabel.place(x=583, y=400)

# Signup Section
signupLabel = Label(login_window, text="Don't have an account?", font=("Open Sans", 9, "bold"),
                    fg="firebrick1", bg="white")
signupLabel.place(x=590, y=500)

newButton = Button(login_window, text="Create an account", fg="blue", bg="white",
                   activebackground="white", font=("Open Sans", 9, "bold underline"),
                   activeforeground="blue", cursor="hand2", bd=0, command=signup_page)
newButton.place(x=727, y=500)

# User Login Button
userLoginButton = Button(login_window, text="User Login", fg="white", bg="green", 
                         font=("Open Sans", 16, "bold"), command=signup_page)
userLoginButton.place(x=578, y=450)

login_window.mainloop()

