from tkinter import *
from PIL import ImageTk
import pymysql
from tkinter import messagebox
def signup_page():
    login_page.destroy()  # Close the login window
    try:
        import signup  # Ensure signup.py exists in the same directory
    except ImportError:
        print("Error: signup.py not found!")

    # Open the user panel window after sign up
    import user_panel  # Assuming your user panel code is in user_panel.py
    user_panel.panel_window.mainloop()  # Run the user panel windo
def clear():
    emailEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirmEntry.delete(0, END)
    check.set(0)

def connect_database():
    if emailEntry.get() == "" or usernameEntry.get() == "" or passwordEntry.get() == "" or confirmEntry.get() == "":
        messagebox.showerror("Error", "All fields are required")
    elif passwordEntry.get() != confirmEntry.get():
        messagebox.showerror("Error", "Passwords do not match")
    elif check.get() == 0:
        messagebox.showerror("Error", "Please accept Terms & Conditions")
    else:
        try:
            con = pymysql.connect(host="localhost", user="root", password="root")
            mycursor = con.cursor()
        except:
            messagebox.showerror("Error", "Database connectivity issue, please try again")
            return

        try:
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
            messagebox.showerror("Error", f"Error while setting up database: {str(e)}")
            return

        mycursor.execute("USE userdata")
        mycursor.execute("SELECT * FROM data WHERE username=%s", (usernameEntry.get(),))
        row = mycursor.fetchone()

        if row is not None:
            messagebox.showerror("Error", "Username already exists")
        else:
            mycursor.execute("INSERT INTO data (email, username, password) VALUES (%s, %s, %s)",
                             (emailEntry.get(), usernameEntry.get(), passwordEntry.get()))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Registration successful")
            clear()
            signup_window.destroy()
            import signin  # Redirect to signin page

def login_page():
    signup_window.destroy()
    import signin  # Ensure signin.py exists in the same directory

signup_window = Tk()
signup_window.title("Signup Page")
signup_window.geometry("990x660+50+50")
signup_window.resizable(0, 0)

# Load Background Image
background = ImageTk.PhotoImage(file="bg.jpg")
bgLabel = Label(signup_window, image=background)
bgLabel.grid()

# Main Frame
frame = Frame(signup_window, bg="white")
frame.place(x=554, y=100)

# Heading
heading = Label(frame, text="CREATE AN ACCOUNT", font=("Microsoft Yahei UI Light", 19, "bold"), bg="white", fg="firebrick1")
heading.grid(row=0, column=0, padx=10, pady=10)

# Email
emailLabel = Label(frame, text="Email", font=("Microsoft Yahei UI Light", 10, "bold"), bg="white", fg="firebrick1")
emailLabel.grid(row=1, column=0, sticky="w", padx=25, pady=(10, 0))

emailEntry = Entry(frame, width=25, font=("Microsoft Yahei UI Light", 10, "bold"), fg="black", bg="white", bd=0)
emailEntry.grid(row=2, column=0, sticky="w", padx=25)

frame1 = Frame(frame, width=250, height=2, bg="firebrick1")
frame1.grid(row=3, column=0, sticky="w", padx=25)

# Username
usernameLabel = Label(frame, text="Username", font=("Microsoft Yahei UI Light", 10, "bold"), bg="white", fg="firebrick1")
usernameLabel.grid(row=4, column=0, sticky="w", padx=25, pady=(10, 0))

usernameEntry = Entry(frame, width=25, font=("Microsoft Yahei UI Light", 10, "bold"), fg="black", bg="white", bd=0)
usernameEntry.grid(row=5, column=0, sticky="w", padx=25)

frame2 = Frame(frame, width=250, height=2, bg="firebrick1")
frame2.grid(row=6, column=0, sticky="w", padx=25)

# Password
passwordLabel = Label(frame, text="Password", font=("Microsoft Yahei UI Light", 10, "bold"), bg="white", fg="firebrick1")
passwordLabel.grid(row=7, column=0, sticky="w", padx=25, pady=(10, 0))

passwordEntry = Entry(frame, width=25, font=("Microsoft Yahei UI Light", 10, "bold"), fg="black", bg="white", bd=0, show="*")
passwordEntry.grid(row=8, column=0, sticky="w", padx=25)

frame3 = Frame(frame, width=250, height=2, bg="firebrick1")
frame3.grid(row=9, column=0, sticky="w", padx=25)

# Confirm Password
confirmLabel = Label(frame, text="Confirm Password", font=("Microsoft Yahei UI Light", 10, "bold"), bg="white", fg="firebrick1")
confirmLabel.grid(row=10, column=0, sticky="w", padx=25, pady=(10, 0))

confirmEntry = Entry(frame, width=25, font=("Microsoft Yahei UI Light", 10, "bold"), fg="black", bg="white", bd=0, show="*")
confirmEntry.grid(row=11, column=0, sticky="w", padx=25)

frame4 = Frame(frame, width=250, height=2, bg="firebrick1")
frame4.grid(row=12, column=0, sticky="w", padx=25)

# Terms and Conditions
check = IntVar()
terms = Checkbutton(frame, text="I agree to Terms & Conditions", font=("Microsoft Yahei UI Light", 9, "bold"),
                    fg="firebrick1", bg="white", activebackground="white", activeforeground="firebrick1", bd=0, variable=check)
terms.grid(row=13, column=0, padx=15, pady=10)

# Signup Button
signupButton = Button(frame, text="Signup", font=("Open Sans", 9, "bold"), width=17, bd=0,
                      bg="firebrick1", fg="white", activebackground="firebrick1", activeforeground="white", command=connect_database)
signupButton.grid(row=14, column=0, pady=10)

# Already have an account?
already = Label(frame, text="Already have an account?", font=("Open Sans", 9, "bold"), bg="white", fg="black")
already.grid(row=15, column=0, sticky="w", padx=25, pady=10)

# Login Button
loginButton = Button(frame, text="Log in", font=("Open Sans", 9, "bold underline"), bg="white", fg="blue",
                     bd=0, cursor="hand2", activebackground="white", activeforeground="blue", command=login_page)
loginButton.grid(row=15, column=0, sticky="e", padx=25, pady=10)

signup_window.mainloop()
