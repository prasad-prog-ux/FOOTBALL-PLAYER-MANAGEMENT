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
                database="footballplayerdata"  
            )
            mycursor = con.cursor() 

            query = """
            CREATE TABLE IF NOT EXISTS player (
                playerid INT NOT NULL PRIMARY KEY,
                name VARCHAR(100),
                gender VARCHAR(30),
                age INT,
                country VARCHAR(50),
                club VARCHAR(50),
                goals_assists VARCHAR(50)
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

    Label(connectwindow, text="Hostname", font=("Arial", 20, "bold"), fg="#22c55e", bg="#0f172a").grid(row=0, column=0, padx=20)
    hostEntry = Entry(connectwindow, font=("Helvetica", 16, "bold"), bd=4, fg="#22c55e", bg="#0f172a")
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    Label(connectwindow, text="Username", font=("Arial", 20, "bold"), fg="#22c55e", bg="#0f172a").grid(row=1, column=0, padx=20)
    usernameEntry = Entry(connectwindow, font=("Helvetica", 16, "bold"), bd=4, fg="#22c55e", bg="#0f172a")
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    Label(connectwindow, text="Password", font=("Arial", 20, "bold"), fg="#22c55e", bg="#0f172a").grid(row=2, column=0, padx=20)
    passwordEntry = Entry(connectwindow, font=("Helvetica", 16, "bold"), bd=4, show="*", fg="#22c55e", bg="#0f172a")
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    ttk.Button(connectwindow, text="Connect", command=connect, style="TButton").grid(row=3, columnspan=2, pady=7)


def iexit():
    result = messagebox.askyesno("Confirm", "Do you want to exit? ")
    if result:
        root.destroy()
    else:
        pass    

def export_data():
    url = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

    if url:
        indexing = playerTable.get_children()
        newlist = []
        for index in indexing:
            content = playerTable.item(index)
            datalist = content['values']
            newlist.append(datalist)
        table = pandas.DataFrame(newlist, columns=["Playerid", "Name", "Gender", "Age", "Country", "Club", "Goals/Assists"])
        table.to_csv(url, index=False)
        messagebox.showinfo("Success", "Data is saved successfully")


def toplevel_data(title, button_text, command):
    global playeridEntry, nameEntry, genderEntry, ageEntry, countryEntry, clubEntry, goals_assistsEntry, screen

    screen = Toplevel()
    screen.title("Update Player")
    screen.grab_set()
    screen.resizable(0, 0)

    Label(screen, text="Player ID", font=("Helvetica", 20, "bold"), fg="#22c55e", bg="#0f172a").grid(row=0, column=0, padx=30, pady=15)
    playeridEntry = Entry(screen, font=("Helvetica", 20, "bold"), width=24, fg="#22c55e", bg="#0f172a")
    playeridEntry.grid(row=0, column=1, padx=10, pady=15)

    Label(screen, text="Name", font=("Helvetica", 20, "bold"), fg="#22c55e", bg="#0f172a").grid(row=1, column=0, padx=30, pady=15)
    nameEntry = Entry(screen, font=("Helvetica", 20, "bold"), width=24, fg="#22c55e", bg="#0f172a")
    nameEntry.grid(row=1, column=1, padx=10, pady=15)

    Label(screen, text="Gender", font=("Helvetica", 20, "bold"), fg="#22c55e", bg="#0f172a").grid(row=2, column=0, padx=30, pady=15)
    genderEntry = Entry(screen, font=("Helvetica", 20, "bold"), width=24, fg="#22c55e", bg="#0f172a")
    genderEntry.grid(row=2, column=1, padx=10, pady=15)

    Label(screen, text="Age", font=("Helvetica", 20, "bold"), fg="#22c55e", bg="#0f172a").grid(row=3, column=0, padx=30, pady=15)
    ageEntry = Entry(screen, font=("Helvetica", 20, "bold"), width=24, fg="#22c55e", bg="#0f172a")
    ageEntry.grid(row=3, column=1, padx=10, pady=15)

    Label(screen, text="Country", font=("Helvetica", 20, "bold"), fg="#22c55e", bg="#0f172a").grid(row=4, column=0, padx=30, pady=15)
    countryEntry = Entry(screen, font=("Helvetica", 20, "bold"), width=24, fg="#22c55e", bg="#0f172a")
    countryEntry.grid(row=4, column=1, padx=10, pady=15)

    Label(screen, text="Club", font=("Helvetica", 20, "bold"), fg="#22c55e", bg="#0f172a").grid(row=5, column=0, padx=30, pady=15)
    clubEntry = Entry(screen, font=("Helvetica", 20, "bold"), width=24, fg="#22c55e", bg="#0f172a")
    clubEntry.grid(row=5, column=1, padx=10, pady=15)

    Label(screen, text="Goals/Assists", font=("Helvetica", 20, "bold"), fg="#22c55e", bg="#0f172a").grid(row=6, column=0, padx=30, pady=15)
    goals_assistsEntry = Entry(screen, font=("Helvetica", 20, "bold"), width=24, fg="#22c55e", bg="#0f172a")
    goals_assistsEntry.grid(row=6, column=1, padx=10, pady=15)

    ttk.Button(screen, text=button_text, command=command, style="TButton").grid(row=7, column=2, pady=15)
    if title == "Update player":
        indexing = playerTable.focus()
        content = playerTable.item(indexing)
        listdata = content["values"]
        playeridEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        genderEntry.insert(0, listdata[2])
        ageEntry.insert(0, listdata[3])
        countryEntry.insert(0, listdata[4])
        clubEntry.insert(0, listdata[5])
        goals_assistsEntry.insert(0, listdata[6])


def update_data():
    query = """UPDATE player SET name=%s, gender=%s, age=%s, country=%s, club=%s, goals_assists=%s WHERE playerid=%s"""
    mycursor.execute(query, (
        nameEntry.get(), genderEntry.get(), ageEntry.get(), countryEntry.get(), clubEntry.get(), goals_assistsEntry.get(), playeridEntry.get()
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

    Label(search_window, text="Player ID", font=("Helvetica", 20, "bold"), fg="#22c55e", bg="#0f172a").grid(row=0, column=0, padx=30, pady=15)
    playeridEntry = Entry(search_window, font=("Helvetica", 20, "bold"), width=24, fg="#22c55e", bg="#0f172a")
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

    ttk.Button(search_window, text="Search", width=20, command=perform_search, style="TButton").grid(row=7, column=1, pady=15)


def add_data():
    try:
        query = "INSERT INTO player (playerid, name, gender, age, country, club, goals_assists) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(query, (
            playeridEntry.get(), nameEntry.get(), genderEntry.get(), ageEntry.get(), countryEntry.get(), clubEntry.get(), goals_assistsEntry.get()
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
root.configure(bg="#0f172a")  

datetimeLabel = Label(root, text="Loading...", font=("Times New Roman", 20, "bold"), bg="#0f172a", fg="#22c55e")
datetimeLabel.place(x=5, y=5)

def clock():
    current_time = time.strftime("%H:%M:%S")
    datetimeLabel.config(text=current_time)
    datetimeLabel.after(1000, clock)

clock()


slider_text = Label(root, text="Welcome to Football Management System! ", font=("Arial", 18), fg="#22c55e", bg="#0f172a")
slider_text.place(x=350, y=10)

def slide_text():
    current_x = slider_text.winfo_x()
    if current_x > 1174:
        slider_text.place(x=-slider_text.winfo_width())
    else:
        slider_text.place(x=current_x + 5, y=10)
    root.after(100, slide_text)

slide_text()

addplayerButton = ttk.Button(root, text="Add Player", width=20, state=DISABLED, command=lambda:toplevel_data("Add player", "Add ", add_data))
addplayerButton.place(x=50, y=80)

showplayerButton = ttk.Button(root, text="Show Players", width=20, state=DISABLED, command=show_player)
showplayerButton.place(x=50, y=150)

updateplayerButton = ttk.Button(root, text="Update Player", width=20, state=DISABLED, command=lambda:toplevel_data("Update player", "Update", update_data))
updateplayerButton.place(x=50, y=220)

deleteplayerButton = ttk.Button(root, text="Delete Player", width=20, state=DISABLED, command=delete_player)
deleteplayerButton.place(x=50, y=290)

searchplayerButton = ttk.Button(root, text="Search Player", width=20, state=DISABLED, command=lambda:toplevel_data("Search player", "Search", search_data))
searchplayerButton.place(x=50, y=360)

exportplayerButton = ttk.Button(root, text="Export Data", width=20, state=DISABLED, command=export_data)
exportplayerButton.place(x=50, y=430)

exitButton = ttk.Button(root, text="Exit", width=20, command=iexit)

exitButton.place(x=50, y=500)

ttk.Button(root, text="Connect to Database", command=connect_database).place(x=50, y=550)
rightFrame=Frame(root)
rightFrame.place(x=350,y=80,width=820,height=600)

ScrollbarX=Scrollbar(rightFrame,orient=HORIZONTAL)

ScrollbarY=Scrollbar(rightFrame,orient=VERTICAL)
playerTable = ttk.Treeview(rightFrame, columns=("playerid", "name", "gender", "age", "country", "club", "goals_assists"), height=15, show="headings", xscrollcommand=ScrollbarX.set, yscrollcommand=ScrollbarY.set)
ScrollbarX.pack(side=BOTTOM,fill=X)
ScrollbarY.pack(side=RIGHT,fill=Y)

ScrollbarX.config(command=playerTable.xview)
ScrollbarY.config(command=playerTable.yview)

playerTable.heading("playerid", text="Player ID")
playerTable.heading("name", text="Name")
playerTable.heading("gender", text="Gender")
playerTable.heading("age", text="Age")
playerTable.heading("country", text="Country")
playerTable.heading("club", text="Club")
playerTable.heading("goals_assists", text="Goals/Assists")

playerTable.column("playerid", width=100, anchor="center")
playerTable.column("name", width=200, anchor="center")
playerTable.column("gender", width=100, anchor="center")
playerTable.column("age", width=80, anchor="center")
playerTable.column("country", width=120, anchor="center")
playerTable.column("club", width=120, anchor="center")
playerTable.column("goals_assists", width=150, anchor="center")

playerTable.pack(fill=BOTH, expand=True)

root.mainloop()
