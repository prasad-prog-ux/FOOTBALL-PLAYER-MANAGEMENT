import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import pymysql
from PIL import Image, ImageDraw, ImageFont, ImageTk
import csv

def connect_database():
    try:
        con = pymysql.connect(host="localhost", user="root", password="root", database="footballplayerdata")
        return con
    except:
        messagebox.showerror("Error", "Database connectivity issue!")
        return None

def load_stats():
    conn = connect_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), AVG(goals_assists) FROM player")
        total, avg_goals = cursor.fetchone()
        conn.close()
        card1_label.config(text=str(total))
        card2_label.config(text=f"{avg_goals:.2f}")

def load_data():
    tree.delete(*tree.get_children())
    conn = connect_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM player")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)
        conn.close()
        load_stats()

def search_data():
    keyword = search_entry.get().strip()
    if not keyword:
        messagebox.showerror("Error", "Enter a search keyword!")
        return
    
    tree.delete(*tree.get_children())
    conn = connect_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM player WHERE name LIKE %s", ('%' + keyword + '%',))
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)
        conn.close()

def export_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    conn = connect_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM player")
        rows = cursor.fetchall()
        conn.close()
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Gender", "Age", "Country", "Club", "Goals/Assists"])
            writer.writerows(rows)
        messagebox.showinfo("Export Successful", "Data exported to CSV successfully!")

def toggle_theme():
    global current_theme
    if current_theme == "dark":
        root.configure(bg="white")
        current_theme = "light"
    else:
        root.configure(bg="#0f172a")
        current_theme = "dark"

def exit_application():
    feedback = simpledialog.askstring("Feedback", "We appreciate your feedback! Please share your thoughts:")
    if feedback:
        user_email = "user@example.com"  # Replace this with actual user email retrieval logic
        messagebox.showinfo("Thank You", f"Thanks for your feedback, hope to see you again!")
    root.destroy()

root = tk.Tk()
root.title("Footy - User Panel")
root.geometry("1200x700")
root.configure(bg="#0f172a")
current_theme = "dark"

sidebar = tk.Frame(root, bg="#1e293b", width=200)
sidebar.pack(side="left", fill="y")

top_frame = tk.Frame(root, bg="#0f172a")
top_frame.pack(fill="x", pady=(10, 0))

search_frame = tk.Frame(top_frame, bg="#0f172a")
search_frame.pack(pady=10)
search_entry = tk.Entry(search_frame, font=("Helvetica", 12))
search_entry.pack(side=tk.LEFT, padx=5)
search_button = tk.Button(search_frame, text="Search", font=("Helvetica", 12), command=search_data)
search_button.pack(side=tk.LEFT, padx=5)

tk.Label(top_frame, text="Welcome to the Footy Dashboard!", font=("Helvetica", 18, "bold"), bg="#0f172a", fg="#22c55e").pack(pady=10)

stat_frame = tk.Frame(root, bg="#0f172a")
stat_frame.pack(fill="x", padx=20, pady=(5, 10))

card1_label = tk.Label(stat_frame, text="0", font=("Helvetica", 20, "bold"), bg="#0f172a", fg="#22c55e")
card1_label.pack()
card2_label = tk.Label(stat_frame, text="0.00", font=("Helvetica", 20, "bold"), bg="#0f172a", fg="#22c55e")
card2_label.pack()

main_frame = tk.Frame(root, bg="#0f172a")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

style = ttk.Style()
style.configure("Treeview", background="#1e293b", foreground="white", rowheight=25, font=("Helvetica", 11))
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#22c55e", foreground="black")

tree = ttk.Treeview(main_frame, columns=("ID", "Name", "Gender", "Age", "Country", "Club", "Goals/Assists"), show="headings")
tree.pack(fill="both", expand=True)
for col in ("ID", "Name", "Gender", "Age", "Country", "Club", "Goals/Assists"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100)

tk.Button(sidebar, text="Load Data", command=load_data).pack(pady=10, fill="x")
tk.Button(sidebar, text="Export CSV", command=export_csv).pack(pady=10, fill="x")
tk.Button(sidebar, text="Toggle Theme", command=toggle_theme).pack(pady=10, fill="x")
tk.Button(sidebar, text="Exit", command=exit_application).pack(pady=10, fill="x")

load_data()
root.mainloop()
