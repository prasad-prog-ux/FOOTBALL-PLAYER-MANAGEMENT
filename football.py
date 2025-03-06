from tkinter import ttk
import tkinter as tk
import pymysql
from PIL import Image, ImageTk  
from tkinter import messagebox

# Create main window

# image = Image.open("logo.jpeg")  
# image = image.resize((50, 50))  
# logo = ImageTk.PhotoImage(image)
# # Title Label
# label = tk.Label(
#     window, 
#     text="WELCOME TO FOOTBALL PLAYER STATS",
#     font=("Times New Roman", 25), 
#     bd=12, 
#     relief=tk.GROOVE, 
#     fg="white",
#     bg="blue",
#     image=logo,
#     compound="left",
#     padx=5,
#     pady=5
# )
# label.pack(fill=tk.X)

# # Player Details Frame
# details = tk.LabelFrame(
#     window, 
#     text="Enter Player Details",
#     font=("Roboto Serif", 20), 
#     bd=15, 
#     relief=tk.GROOVE, 
#     bg="blue",
#     fg="white"
# )
# details.place(x=50,y=95,width=420,height=540)

# data_frame=tk.LabelFrame(window,bd=12,bg="blue",relief=tk.GROOVE)
# data_frame.place(x=480,y=95,width=850,height=540)
# # Run the GUI
# window.mainloop()


def login():
    if  usernamentry.get()=="" or passwordentry.get()=="":
        messagebox.showerror("Error","Please fill the details")
    elif usernamentry.get()=="MESSI" and passwordentry.get()=="10":
        messagebox.showinfo("FOOTBALL PLAYER STATISTICS","WELCOME") 
        import fb











window = tk.Tk()
window.title("FOOTBALL PLAYER STATISTICS")
window.geometry("1350x700+0+0")


background = Image.open("back.jpg")  
background = background.resize((1350, 700))  
background = ImageTk.PhotoImage(background)
bgLabel = tk.Label(window, image=background)
bgLabel.place(x=0, y=0, )  

bgLabel.image = background  

loginFrame = tk.Frame(window, width=300, height=200, bg="white")
loginFrame.place(x=525, y=250)  
loginFrame.pack_propagate(False)
logoImage=tk.PhotoImage(file="football.png")
logolabel=tk.Label(loginFrame,image=logoImage)
logolabel.grid(row=0,column=0,columnspan=2,padx=10)


usernameimage=tk.PhotoImage(file="user.png")
usernameLabel=tk.Label(loginFrame,image= usernameimage,text="username",compound="left",font=("times new roman",20,"bold"))
usernameLabel.grid(row=1,column=0,padx=10)
usernamentry=tk.Entry(loginFrame,font=("times new roman",20,"bold"),bd=7,width=15)
usernamentry.grid(row=1,column=1)



passwordimage=tk.PhotoImage(file="padlock.png")
passwordLabel=tk.Label(loginFrame,image= passwordimage,text="Password",compound="left",font=("times new roman",20,"bold"))
passwordLabel.grid(row=2,column=0,padx=10)
passwordentry=tk.Entry(loginFrame,font=("times new roman",20,"bold"),bd=7,width=15)
passwordentry.grid(row=2,column=1)


loginbutton=tk.Button(loginFrame,text="Login",font=("times new roman",10,"bold"),width=12,fg="white",bg="royal blue",cursor="hand2",command=login)
loginbutton.grid(row=3,column=1,pady=10)
# Run the GUI
window.mainloop()
