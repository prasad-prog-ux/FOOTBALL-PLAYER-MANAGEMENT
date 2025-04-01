import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
        messagebox.showinfo("Info", "Enter a search keyword!")
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

def send_feedback_email(user_email):
    sender_email = "your_email@example.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your email password
    subject = "Thank You for Your Feedback"
    body = "Thanks for your feedback! Hope to see you again."
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()
    except Exception as e:
        messagebox.showerror("Error", f"Email sending failed: {e}")

def feedback_form():
    feedback_window = tk.Toplevel(root)
    feedback_window.title("Feedback Form")
    feedback_window.geometry("400x300")
    tk.Label(feedback_window, text="Please provide your feedback:", font=("Helvetica", 12)).pack(pady=10)
    feedback_entry = tk.Text(feedback_window, height=5, width=40)
    feedback_entry.pack(pady=10)
    
    def submit_feedback():
        feedback_text = feedback_entry.get("1.0", tk.END).strip()
        if feedback_text:
            user_email = "user@example.com"  # Replace with actual user email
            send_feedback_email(user_email)
            messagebox.showinfo("Thank You", "Thanks for your feedback! Hope to see you again.")
            feedback_window.destroy()
    
    tk.Button(feedback_window, text="Submit", command=submit_feedback).pack(pady=10)

def exit_application():
    feedback_form()
    root.quit()

def toggle_theme():
    global current_theme
    if current_theme == "dark":
        root.configure(bg="white")
        current_theme = "light"
    else:
        root.configure(bg="#0f172a")
        current_theme = "dark"

root = tk.Tk()
root.title("Footy - User Panel")
root.geometry("1200x700")
root.configure(bg="#0f172a")
current_theme = "dark"

sidebar = tk.Frame(root, bg="#1e293b", width=200)
sidebar.pack(side="left", fill="y")

tk.Button(sidebar, text="Search", command=search_data).pack(pady=10, fill="x")
tk.Button(sidebar, text="Load Data", command=load_data).pack(pady=10, fill="x")
tk.Button(sidebar, text="Export CSV", command=export_csv).pack(pady=10, fill="x")
tk.Button(sidebar, text="Toggle Theme", command=toggle_theme).pack(pady=10, fill="x")
tk.Button(sidebar, text="Exit", command=exit_application).pack(pady=10, fill="x")

top_frame = tk.Frame(root, bg="#0f172a")
top_frame.pack(fill="x", pady=(10, 0))
tk.Label(top_frame, text="Welcome to the Footy Dashboard!", font=("Helvetica", 18, "bold"), bg="#0f172a", fg="#22c55e").pack(pady=10)

search_frame = tk.Frame(root, bg="#0f172a")
search_frame.pack(pady=10)
search_entry = tk.Entry(search_frame, font=("Helvetica", 12))
search_entry.pack(side=tk.LEFT, padx=5)
search_button = tk.Button(search_frame, text="Search", font=("Helvetica", 12), command=search_data)
search_button.pack(side=tk.LEFT, padx=5)

load_data()
root.mainloop()