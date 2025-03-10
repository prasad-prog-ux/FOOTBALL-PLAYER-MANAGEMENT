import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from PIL import Image, ImageDraw, ImageFont, ImageTk

# Database connection
def connect_database():
    try:
        con = pymysql.connect(host="localhost", user="root", password="root", database="footballplayerdata")
        return con
    except:
        messagebox.showerror("Error", "Database connectivity issue!")
        return None

# Function to fetch and display data
def fetch_data():
    con = connect_database()
    if con:
        try:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM player")
            rows = cursor.fetchall()
            con.close()
            if rows:
                for row in table.get_children():
                    table.delete(row)
                for row in rows:
                    table.insert("", "end", values=row)
            else:
                messagebox.showinfo("Info", "No records found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")

# Function to search players
def search_player():
    search_term = search_entry.get().strip()
    if not search_term:
        messagebox.showerror("Error", "Enter a search keyword!")
        return
    
    con = connect_database()
    if con:
        try:
            cursor = con.cursor()
            query = f"SELECT * FROM player WHERE name LIKE %s OR club LIKE %s OR country LIKE %s"
            cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            rows = cursor.fetchall()
            con.close()
            
            for row in table.get_children():
                table.delete(row)
            for row in rows:
                table.insert("", "end", values=row)
            
            if not rows:
                messagebox.showinfo("Info", "No matching players found.")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")

# Function to generate TOTY Card
def generate_toty_card():
    selected_item = table.focus()
    if not selected_item:
        messagebox.showerror("Error", "Select a player first!")
        return

    player_data = table.item(selected_item, "values")
    if not player_data:
        messagebox.showerror("Error", "No player data found!")
        return

    player_id, name, gender, age, country, club, goals_assists = player_data
    
    # Create card image with a red background for FIFA World Cup 2022
    card = Image.new("RGB", (400, 500), "#D50032")  # Red background (FIFA WC 2022 theme)
    draw = ImageDraw.Draw(card)

    # Load font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    # Draw player details on the card
    draw.text((20, 20), f"FIFA WORLD CUP 2022", font=font, fill="#FFD700")  # Gold title
    draw.text((20, 70), f"Name: {name}", font=font, fill="white")  # White text for the name
    draw.text((20, 120), f"Age: {age}", font=font, fill="white")  # White text for age
    draw.text((20, 170), f"Club: {club}", font=font, fill="white")  # White text for club
    draw.text((20, 220), f"Country: {country}", font=font, fill="white")  # White text for country
    draw.text((20, 270), f"Goals/Assists: {goals_assists}", font=font, fill="white")  # White text for stats

    # Convert Image to Tkinter PhotoImage and display
    card = card.resize((300, 400))  # Resize to fit
    card_img = ImageTk.PhotoImage(card)
    
    # Create a new window to show the FIFA World Cup card
    card_window = tk.Toplevel(panel_window)
    card_window.title(f"FIFA World Cup Card - {name}")
    card_window.geometry("320x450")

    card_label = tk.Label(card_window, image=card_img)
    card_label.image = card_img
    card_label.pack(padx=10, pady=10)

# Function to display the feedback form
def show_feedback_form():
    feedback_window = tk.Toplevel(panel_window)
    feedback_window.title("Feedback Form")
    feedback_window.geometry("400x300")
    
    # Feedback form components
    feedback_label = tk.Label(feedback_window, text="Please provide your feedback below:", font=("Arial", 12))
    feedback_label.pack(pady=10)
    
    feedback_text = tk.Text(feedback_window, width=40, height=8, font=("Arial", 12))
    feedback_text.pack(pady=10)
    
    def submit_feedback():
        feedback = feedback_text.get("1.0", "end-1c")
        if feedback.strip() == "":
            messagebox.showerror("Error", "Feedback cannot be empty.")
            return
        # You can save the feedback to a database or a file here
        # For now, we are just showing it in a message box
        messagebox.showinfo("Thank You", "Your feedback has been submitted!")
        feedback_window.destroy()

    submit_button = tk.Button(feedback_window, text="Submit Feedback", font=("Arial", 12), command=submit_feedback)
    submit_button.pack(pady=10)

# Function to logout
def logout():
    panel_window.destroy()
    import signin  # Redirect to login page

# Creating user panel window
panel_window = tk.Tk()
panel_window.title("User Panel - Football Player Statistics")
panel_window.geometry("900x500")

# Menu Bar
menu_bar = tk.Menu(panel_window)
panel_window.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=file_menu)
file_menu.add_command(label="Refresh", command=fetch_data)
file_menu.add_command(label="Logout", command=logout)
file_menu.add_command(label="Feedback", command=show_feedback_form)  # Add option to show feedback form

# Search Section
search_frame = tk.Frame(panel_window)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Search:", font=("Arial", 12))
search_label.pack(side=tk.LEFT, padx=5)
search_entry = tk.Entry(search_frame, font=("Arial", 12))
search_entry.pack(side=tk.LEFT, padx=5)
search_button = tk.Button(search_frame, text="Search", font=("Arial", 12), command=search_player)
search_button.pack(side=tk.LEFT, padx=5)

# Table for Player Data
table_frame = tk.Frame(panel_window)
table_frame.pack(fill="both", expand=True)

columns = ("Player ID", "Name", "Gender", "Age", "Country", "Club", "Goals/Assists")
table = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120)

table.pack(fill="both", expand=True)

# TOTY Card Generator Button
toty_button = tk.Button(panel_window, text="Generate TOTY Card", font=("Arial", 12, "bold"), bg="gold", command=generate_toty_card)
toty_button.pack(pady=10)

fetch_data()  # Load data on startup

panel_window.mainloop()
