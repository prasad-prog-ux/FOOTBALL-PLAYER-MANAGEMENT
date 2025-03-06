from tkinter import *
from ttkthemes import ThemedTk
from tkinter import ttk, messagebox, filedialog
import pymysql
import time
import pandas


def connect_database():
    def connect():
        try:
            global con, mycursor
            con = pymysql.connect(
                host=hostEntry.get(),
                user=usernameEntry.get(),
                password=passwordEntry.get(),
                database="footballsystem"
            )
            mycursor = con.cursor()

          
            query = """
            CREATE TABLE IF NOT EXISTS player (
                playerid INT NOT NULL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(50),
                gender VARCHAR(30),
                dob DATE
            )
            """
            mycursor.execute(query)
            messagebox.showinfo("Success", "Database Connected Successfully!", parent=connectwindow)

            
            addplayerButton.config(state=NORMAL)
            searchplayerButton.config(state=NORMAL)
            updateplayerButton.config(state=NORMAL)
            showplayerButton.config(state=NORMAL)
            deleteplayerButton.config(state=NORMAL)
            exportplayerButton.config(state=NORMAL)

            connectwindow.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Database Connection Failed: {e}", parent=connectwindow)

    
    connectwindow = Toplevel()
    connectwindow.grab_set()  
    connectwindow.geometry("470x250+730+230")
    connectwindow.title("Database Connection")
    connectwindow.resizable(0, 0)

    Label(connectwindow, text="Hostname", font=("Arial", 20, "bold")).grid(row=0, column=0, padx=20)
    hostEntry = Entry(connectwindow, font=("roman,", 16, "bold"), bd=4)
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    Label(connectwindow, text="Username", font=("Arial", 20, "bold")).grid(row=1, column=0, padx=20)
    usernameEntry = Entry(connectwindow, font=("roman,", 16, "bold"), bd=4)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    Label(connectwindow, text="Password", font=("Arial", 20, "bold")).grid(row=2, column=0, padx=20)
    passwordEntry = Entry(connectwindow, font=("roman,", 16, "bold"), bd=4, show="*")
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    ttk.Button(connectwindow, text="Connect", command=connect).grid(row=3, columnspan=2, pady=7)

def iexit():
    result=messagebox.askyesno("Confirm","Do you want to exit? ")
    if result:
        root.destroy()
    else:
        pass    

def export_data():
    url=filedialog.askopenfilesfilename(defaultextension=".csv")

    indexing=playerTable.get_children()
    newlist=[]
    for index in indexing:
        content = playerTable.item(index)
        datalist=content['values']
        newlist.append(datalist)
        table=pandas.DataFrame(newlist,columns=["Playerid","Name","DOB","Gender","Email"])
        table.to_csv(url,index=False)
        messagebox.showinfo("Success","Data is saved successfully")


def toplevel_data(title,button_text,command):
    global playeridEntry, emailEntry, nameEntry, dobEntry, genderEntry, screen
     
    screen = Toplevel()
    screen.title("Update Player")
    screen.grab_set()
    screen.resizable(0, 0)

    Label(screen, text="Player ID", font=("roman", 20, "bold")).grid(row=0, column=0, padx=30, pady=15)
    playeridEntry = Entry(screen, font=("roman", 20, "bold"), width=24)
    playeridEntry.grid(row=0, column=1, padx=10, pady=15)

    Label(screen, text="Name", font=("roman", 20, "bold")).grid(row=1, column=0, padx=30, pady=15)
    nameEntry = Entry(screen, font=("roman", 20, "bold"), width=24)
    nameEntry.grid(row=1, column=1, padx=10, pady=15)

    Label(screen, text="Email", font=("roman", 20, "bold")).grid(row=2, column=0, padx=30, pady=15)
    emailEntry = Entry(screen, font=("roman", 20, "bold"), width=24)
    emailEntry.grid(row=2, column=1, padx=10, pady=15)

    Label(screen, text="Gender", font=("roman", 20, "bold")).grid(row=3, column=0, padx=30, pady=15)
    genderEntry = Entry(screen, font=("roman", 20, "bold"), width=24)
    genderEntry.grid(row=3, column=1, padx=10, pady=15)

    Label(screen, text="DOB (YYYY-MM-DD)", font=("roman", 20, "bold")).grid(row=4, column=0, padx=30, pady=15)
    dobEntry = Entry(screen, font=("roman", 20, "bold"), width=24)
    dobEntry.grid(row=4, column=1, padx=10, pady=15)

    ttk.Button(screen, text=button_text, command=command).grid(row=7, column=2, pady=15)
    if title == "Update player":
        indexing = playerTable.focus()
        content = playerTable.item(indexing)
        listdata = content["values"]
        playeridEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        emailEntry.insert(0, listdata[2])
        genderEntry.insert(0, listdata[3])
        dobEntry.insert(0, listdata[4])

def update_data():
    query = """UPDATE player SET name=%s, email=%s, dob=%s, gender=%s WHERE playerid=%s"""
    mycursor.execute(query, (
        nameEntry.get(), emailEntry.get(), dobEntry.get(), genderEntry.get(), playeridEntry.get()
    ))
    con.commit()
    messagebox.showinfo("Success", f"Player ID {playeridEntry.get()} modified successfully.", parent=screen)
    screen.destroy()
    show_player()

def show_player():
    query = "SELECT * FROM player"
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    playerTable.delete(*playerTable.get_children())
    for data in fetched_data:
        playerTable.insert("", END, values=data)

def delete_player():
    indexing = playerTable.focus() 
    content = playerTable.item(indexing)
    content_id = content["values"][0]
    query = "DELETE FROM player WHERE playerid=%s"
    mycursor.execute(query, (content_id,))
    con.commit()
    messagebox.showinfo("Deleted", f"Player ID {content_id} deleted successfully.")
    show_player()

def search_data():
    
    search_window = Toplevel()
    search_window.title("Search Player")
    search_window.geometry("400x300+730+230")
    search_window.grab_set()

    Label(search_window, text="Player ID", font=("roman", 20, "bold")).grid(row=0, column=0, padx=30, pady=15)
    playeridEntry = Entry(search_window, font=("roman", 20, "bold"), width=24)
    playeridEntry.grid(row=0, column=1, padx=10, pady=15)

    def perform_search():
        if playeridEntry.get().strip() == "":
            messagebox.showerror("Error", "Player ID is required!", parent=search_window)
            return

        query = "SELECT * FROM player WHERE playerid=%s"
        mycursor.execute(query, (playeridEntry.get(),))
        fetched_data = mycursor.fetchall()

        playerTable.delete(*playerTable.get_children())
        for data in fetched_data:
            playerTable.insert("", END, values=data)

        if not fetched_data:
            messagebox.showinfo("No Result", "No player found with the given Player ID.")

    ttk.Button(search_window, text="Search", width=20, command=perform_search).grid(row=7, column=1, pady=15)


def add_data():
    try:
        query = "INSERT INTO player (playerid, name, email, gender, dob) VALUES (%s, %s, %s, %s, %s)"
        mycursor.execute(query, (
            playeridEntry.get(), nameEntry.get(), emailEntry.get(), genderEntry.get(), dobEntry.get()
        ))
        con.commit()
        messagebox.showinfo("Success", "Player Added Successfully!", parent=screen)
        screen.destroy()

    except pymysql.err.IntegrityError:
        messagebox.showerror("Error", "Player ID already exists!", parent=screen)

# Main GUI
root = ThemedTk(theme="black")
root.geometry("1174x680+0+0")
root.resizable(0, 0)
root.title("FOOTBALL PLAYER MANAGEMENT SYSTEM")

datetimeLabel = Label(root, text="Loading...", font=("Times New Roman", 20, "bold"))
datetimeLabel.place(x=5, y=5)

def clock():
    current_time = time.strftime("%H:%M:%S")
    datetimeLabel.config(text=current_time)
    datetimeLabel.after(1000, clock)

clock()


addplayerButton = ttk.Button(root, text="Add Player", width=20, state=DISABLED, command=lambda:toplevel_data("Add player","Add ",add_data))
addplayerButton.place(x=50, y=80)

showplayerButton = ttk.Button(root, text="Show Players", width=20, state=DISABLED, command=show_player)
showplayerButton.place(x=50, y=150)

updateplayerButton = ttk.Button(root, text="Update Player", width=20, state=DISABLED, command=lambda:toplevel_data("Update player","Update",update_data))
updateplayerButton.place(x=50, y=220)

deleteplayerButton = ttk.Button(root, text="Delete Player", width=20, state=DISABLED, command=delete_player)
deleteplayerButton.place(x=50, y=290)

searchplayerButton = ttk.Button(root, text="Search Player", width=20, state=DISABLED, command=lambda:toplevel_data("Search player","Search",search_data))
searchplayerButton.place(x=50, y=360)

exportplayerButton = ttk.Button(root, text="Export Data", width=20, state=DISABLED)
exportplayerButton.place(x=50, y=430)

exitButton = ttk.Button(root, text="Exit", width=20, state=DISABLED,command=iexit)
exitButton.place(x=50, y=430)

ttk.Button(root, text="Connect to Database", command=connect_database).place(x=50, y=500)


playerTable = ttk.Treeview(root, columns=("playerid", "name", "email", "gender", "dob"), height=15, show="headings")
playerTable.place(x=350, y=80)

playerTable.heading("playerid", text="Player ID")
playerTable.heading("name", text="Name")
playerTable.heading("email", text="Email")
playerTable.heading("gender", text="Gender")
playerTable.heading("dob", text="DOB")


vertical_scroll = ttk.Scrollbar(root, orient="vertical", command=playerTable.yview)
vertical_scroll.place(x=1050, y=80, height=350)
playerTable.config(yscrollcommand=vertical_scroll.set)

horizontal_scroll = ttk.Scrollbar(root, orient="horizontal", command=playerTable.xview)
horizontal_scroll.place(x=350, y=470, width=700)
playerTable.config(xscrollcommand=horizontal_scroll.set)

root.mainloop()
