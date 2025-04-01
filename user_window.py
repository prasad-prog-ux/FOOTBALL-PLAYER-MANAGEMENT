import tkinter as tk 
from tkinter import ttk, messagebox, filedialog
import pymysql
import wikipediaapi  
from PIL import Image, ImageTk
import csv

# Initialize Wikipedia API
wiki = wikipediaapi.Wikipedia(language='en', user_agent='YourAppName/1.0')

def connect_database():
    try:
        con = pymysql.connect(host="localhost", user="root", password="root", database="footballplayerdata")
        return con
    except:
        messagebox.showerror("Error", "Database connectivity issue!")
        return None
def ask_feedback():
    feedback_window = tk.Toplevel(root)
    feedback_window.title("Feedback")
    feedback_window.geometry("400x300")
    feedback_window.configure(bg="#0f172a")

    tk.Label(feedback_window, text="We value your feedback!", font=("Helvetica", 14, "bold"), bg="#0f172a", fg="#22c55e").pack(pady=10)
    
    tk.Label(feedback_window, text="Enter your name:", bg="#0f172a", fg="#22c55e").pack()
    username_entry = tk.Entry(feedback_window, font=("Helvetica", 12))
    username_entry.pack(pady=5)
    
    feedback_text = tk.Text(feedback_window, height=5, width=40)
    feedback_text.pack(pady=5)

    def submit_feedback():
        username = username_entry.get().strip()
        feedback = feedback_text.get("1.0", tk.END).strip()
        
        if not username or not feedback:
            messagebox.showerror("Error", "Both name and feedback are required!")
            return
        
        conn = connect_database()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO feedback (username, feedback_text) VALUES (%s, %s)", (username, feedback))
                conn.commit()
                messagebox.showinfo("Thank You!", "Feedback submitted successfully!")
            except pymysql.MySQLError as e:
                messagebox.showerror("Error", f"Database error: {e}")
            finally:
                conn.close()
        
        feedback_window.destroy()  # Close feedback window only

    tk.Button(feedback_window, text="Submit", command=submit_feedback, bg="#22c55e", fg="black", font=("Helvetica", 12, "bold")).pack(pady=10)
    tk.Button(feedback_window, text="Skip", command=feedback_window.destroy, bg="gray", fg="white", font=("Helvetica", 12, "bold")).pack()

def on_close():
    ask_feedback()

def show_loading_screen():
    loading_frame = tk.Frame(root, bg="#0f172a")
    loading_frame.pack(fill="both", expand=True)
    
    label = tk.Label(loading_frame, text="Loading...", font=("Helvetica", 24, "bold"), bg="#0f172a", fg="#22c55e")
    label.pack(pady=50)

    progress = ttk.Progressbar(loading_frame, orient="horizontal", length=400, mode="determinate")
    progress.pack(pady=20)

    def update_progress(value):
        if value <= 100:
            progress["value"] = value
            root.after(30, update_progress, value + 2)
        else:
            loading_frame.destroy()
            main_ui()

    update_progress(0)

def main_ui():
    global tree, card1_label, card2_label, search_entry, wiki_search_entry, wiki_result_label, current_theme
    
    root.configure(bg="#0f172a")
    current_theme = "dark"

    sidebar = tk.Frame(root, bg="#1e293b", width=200)
    sidebar.pack(side="left", fill="y")

    tk.Button(sidebar, text="Load Data", command=load_data).pack(pady=10, fill="x")
    tk.Button(sidebar, text="Export CSV", command=export_csv).pack(pady=10, fill="x")
    tk.Button(sidebar, text="Toggle Theme", command=toggle_theme).pack(pady=10, fill="x")

    top_frame = tk.Frame(root, bg="#0f172a")
    top_frame.pack(fill="x", pady=(10, 0))

    tk.Label(top_frame, text="Welcome to the Footy Stats Dashboard!", font=("Helvetica", 18, "bold"), bg="#0f172a", fg="#22c55e").pack(side=tk.LEFT, padx=20)

    search_frame = tk.Frame(top_frame, bg="#0f172a")
    search_frame.pack(side=tk.RIGHT, padx=20)
    search_entry = tk.Entry(search_frame, font=("Helvetica", 12))
    search_entry.pack(side=tk.LEFT, padx=5)
    tk.Button(search_frame, text="Search", font=("Helvetica", 12), command=search_data).pack(side=tk.LEFT, padx=5)

    wiki_search_frame = tk.Frame(root, bg="#0f172a")
    wiki_search_frame.pack(fill="x", padx=20, pady=(10, 0))

    tk.Label(wiki_search_frame, text="Search Wikipedia:", font=("Helvetica", 14, "bold"), bg="#0f172a", fg="#22c55e").pack(side=tk.LEFT, padx=20)

    wiki_search_entry = tk.Entry(wiki_search_frame, font=("Helvetica", 12))
    wiki_search_entry.pack(side=tk.LEFT, padx=5)

    tk.Button(wiki_search_frame, text="Search", font=("Helvetica", 12), command=search_wikipedia).pack(side=tk.LEFT, padx=5)

    wiki_result_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#0f172a", fg="#22c55e", wraplength=1000)
    wiki_result_label.pack(padx=20, pady=(10, 20))

    stat_frame = tk.Frame(root, bg="#0f172a")
    stat_frame.pack(fill="x", padx=20, pady=(5, 10))

    card1_label = tk.Label(stat_frame, text="Total Players: 0", font=("Helvetica", 20, "bold"), bg="#0f172a", fg="#22c55e")
    card1_label.pack()
    card2_label = tk.Label(stat_frame, text="Avg Goals/Assists: 0.00", font=("Helvetica", 20, "bold"), bg="#0f172a", fg="#22c55e")
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

    load_data()

def load_stats():
    conn = connect_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), AVG(goals_assists) FROM player")
        total, avg_goals = cursor.fetchone()
        conn.close()
        card1_label.config(text=f"Total Players: {total}")
        card2_label.config(text=f"Avg Goals/Assists: {avg_goals:.2f}")

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
    root.configure(bg="white" if current_theme == "dark" else "#0f172a")
    current_theme = "light" if current_theme == "dark" else "dark"

def search_wikipedia():
    keyword = wiki_search_entry.get().strip()
    page = wiki.page(keyword)
    wiki_result_label.config(text=page.summary[:999] + '...' if page.exists() else "No results found.")

root = tk.Tk()
root.geometry("1200x700")
root.title("Footy - User Panel")
root.protocol("WM_DELETE_WINDOW", on_close)
show_loading_screen()
root.mainloop()
