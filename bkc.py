import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
from tkinter import Toplevel
from PIL import Image, ImageTk
from datetime import datetime

class HomePage:
    def __init__(self, master):
        self.master = master
        self.master.title("Dog Daycare Management")
        self.master.geometry("1000x800")

        pil_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\details-transformed.png')  
        pil_image = pil_image.resize((pil_image.width * 2, pil_image.height * 2))
        self.scaled_image = ImageTk.PhotoImage(pil_image)
        self.background_label = tk.Label(self.master, image=self.scaled_image)
        self.background_label.place(relx=0.5, rely=0.5, anchor="center")

        self.welcome_label = tk.Label(self.master, text="WELCOME TO DOG DAYCARE MANAGEMENT", font=("Helvetica", 50))
        self.welcome_label.place(relx=0.5, rely=0.2, anchor="center")

        self.next_button = tk.Button(self.master, text="Next", font=("Helvetica", 20), command=self.open_login_page, width=15, height=2)
        self.next_button.place(relx=0.5, rely=0.8, anchor="center")

    def open_login_page(self):
        self.master.destroy()
        login_page = LoginPage()

class LoginPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login Page")  
        self.root.geometry("1000x800")
        self.root.configure(bg="light green")  
        pil_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\delete-FwOf2LDRK-transformed.png')  
        pil_image = pil_image.resize((pil_image.width * 2, pil_image.height * 2))
        self.background_image = ImageTk.PhotoImage(pil_image)
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relx=0.5, rely=0.5, anchor="center")
        self.background_label.lower()
        self.welcome_label = tk.Label(self.root, text="LOGIN OPTIONS", font=("Helvetica", 30))
        self.welcome_label.place(relx=0.5, rely=0.1, anchor="center")  
        
        button_font = ("Helvetica", 20)  

        self.admin_button = tk.Button(self.root, text="Admin Login", font=button_font, bg="light blue", fg="black", command=self.open_admin_login)
        self.admin_button.place(relx=0.85, rely=0.45, anchor="center")

        self.customer_button = tk.Button(self.root, text="Customer Login", font=button_font, bg="light blue", fg="black", command=self.open_customer_login)
        self.customer_button.place(relx=0.15, rely=0.45, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", font=button_font, bg="light blue", fg="black", command=self.back_to_homepage)
        self.back_button.place(relx=0.5, rely=0.9, anchor="center")

        self.root.mainloop()
        
    def open_admin_login(self):
        self.root.destroy()
        admin_login_page = AdminLoginPage()

    def open_customer_login(self):
        self.root.destroy()
        customer_login_page = CustomerLoginPage()

    def back_to_homepage(self):
        self.root.destroy()
        homepage = HomePage(tk.Tk())


class AdminLoginPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Admin Login")
        self.root.geometry("1000x800")
        self.root.configure(bg="light yellow")  

        pil_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\cust.png')  
        pil_image = pil_image.resize((pil_image.width * 4, pil_image.height * 4))
        self.background_image = ImageTk.PhotoImage(pil_image)
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(relx=0.5, rely=0.5, anchor="center")
        background_label.lower()

        self.welcome_label = tk.Label(self.root, text="ADMIN LOGIN", font=("Helvetica", 30))
        self.welcome_label.place(relx=0.5, rely=0.1, anchor="center")

        entry_font = ("Helvetica", 20)
        self.username_label = tk.Label(self.root, text="Username:", font=("Helvetica", 20), bg="light yellow", fg="black")
        self.username_label.place(relx=0.3, rely=0.4, anchor="center")
        self.username_entry = tk.Entry(self.root, font=entry_font)
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")

        self.password_label = tk.Label(self.root, text="Password:", font=("Helvetica", 20), bg="light yellow", fg="black")
        self.password_label.place(relx=0.3, rely=0.5, anchor="center")
        self.password_entry = tk.Entry(self.root, show="*", font=entry_font)
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")

        button_font = ("Helvetica", 20)
        self.login_button = tk.Button(self.root, text="Login", font=button_font, command=self.login)
        self.login_button.place(relx=0.5, rely=0.6, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", font=button_font, command=self.back_to_login_page)
        self.back_button.place(relx=0.5, rely=0.8, anchor="center")

        self.root.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.validate_username(username) and self.validate_password(password):
            if username == "admin" and password == "aditya@01":  
                messagebox.showinfo("Success", "Logged in as admin!")
                self.root.destroy()
                admin_options_page = AdminOptionsPage()
            else:
                if self.check_credentials_in_db(username, password):
                    messagebox.showinfo("Success", "Logged in successfully!")
                    self.root.destroy()
                    admin_options_page = AdminOptionsPage()
                else:
                    messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "Invalid username or password format.")

    def validate_username(self, username):
        return username.isalnum()

    def validate_password(self, password):
        return (any(c.isalpha() for c in password) and 
                any(c.isdigit() for c in password) and 
                any(not c.isalnum() for c in password))

    def check_credentials_in_db(self, username, password):
        try:
            conn = sqlite3.connect('dog_daycare.db')  
            cur = conn.cursor()
            cur.execute("SELECT * FROM admin_login WHERE username = ? AND password = ?", (username, password))  
            user = cur.fetchone()
            conn.close()
            return user is not None
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return False

    def back_to_login_page(self):
        self.root.destroy()
        login_page = LoginPage()

class AdminOptionsPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Admin Options")
        self.root.geometry("1000x800")
        self.root.configure(bg="light yellow")  
        self.conn = sqlite3.connect("dog_daycare.db")  
        self.cursor = self.conn.cursor()
        
        pil_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\4dog.png')  
        pil_image = pil_image.resize((pil_image.width * 4, pil_image.height * 4))
        self.background_image = ImageTk.PhotoImage(pil_image)
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(relx=0.5, rely=0.5, anchor="center")
        background_label.lower()

        heading_font = ("Helvetica", 36)
        self.heading_label = tk.Label(self.root, text="ADMIN OPTIONS", font=heading_font)
        self.heading_label.place(relx=0.5, rely=0.1, anchor="center")

        button_font = ("Helvetica", 24)
        self.add_button = tk.Button(self.root, text="Add Dog Details", font=button_font, command=self.open_add_details_page)
        self.add_button.place(relx=0.5, rely=0.3, anchor="center")

        self.delete_button = tk.Button(self.root, text="Delete Dog Details", font=button_font, command=self.open_delete_details_page)
        self.delete_button.place(relx=0.5, rely=0.4, anchor="center")

        self.update_button = tk.Button(self.root, text="Update Dog Details", font=button_font, command=self.open_update_details_page)
        self.update_button.place(relx=0.5, rely=0.5, anchor="center")

        self.view_button = tk.Button(self.root, text="View Dog Registrations", font=button_font, command=self.open_view_member_details_page)
        self.view_button.place(relx=0.5, rely=0.6, anchor="center")

        self.view_button = tk.Button(self.root, text="View Booking Details ", font=button_font, command=self.open_view_booking_details_page)
        self.view_button.place(relx=0.5, rely=0.7, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", font=button_font, command=self.back_to_login_page)
        self.back_button.place(relx=0.5, rely=0.8, anchor="center")

        self.root.mainloop()

    def open_add_details_page(self):
        self.root.destroy()
        add_details_page = AddDetailsPage()

    def open_delete_details_page(self):
        self.root.destroy()
        delete_details_page = DeleteDetailsPage()

    def open_update_details_page(self):
        self.root.destroy()
        update_details_page = UpdateDetailsPage()

    def open_view_member_details_page(self):
        self.root.destroy()
        view_member_details_page = ViewMemberDetailsPage()

    def open_view_booking_details_page(self):
        self.root.destroy()
        ViewBookingDetailsPage()
        
    def back_to_login_page(self):
        self.root.destroy()
        login_page = LoginPage()



class AddDetailsPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Add Dog Details")
        self.root.geometry("1000x800")
        self.root.configure(bg="light green")

        self.conn = sqlite3.connect('dog_daycare.db')
        self.cursor = self.conn.cursor()

        heading_font = ("Helvetica", 30, "bold")
        self.heading_label = tk.Label(self.root, text="Dog Details", font=heading_font, bg="light green", fg="black")
        self.heading_label.place(relx=0.5, rely=0.05, anchor="center")

        background_image = tk.PhotoImage(file='C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\add_details-transformed.png')
        self.background_label = tk.Label(self.root, image=background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.lower()

        self.dog_id_label = tk.Label(self.root, text="Dog ID:", font=("Helvetica", 16), bg="light green", fg="black")
        self.dog_id_label.place(relx=0.3, rely=0.2, anchor="center")
        self.dog_id_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.dog_id_entry.place(relx=0.7, rely=0.2, anchor="center")

        self.dog_name_label = tk.Label(self.root, text="Dog Name:", font=("Helvetica", 16), bg="light green", fg="black")
        self.dog_name_label.place(relx=0.3, rely=0.3, anchor="center")
        self.dog_name_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.dog_name_entry.place(relx=0.7, rely=0.3, anchor="center")

        self.breed_label = tk.Label(self.root, text="Breed:", font=("Helvetica", 16), bg="light green", fg="black")
        self.breed_label.place(relx=0.3, rely=0.4, anchor="center")
        self.breed_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.breed_entry.place(relx=0.7, rely=0.4, anchor="center")

        self.age_label = tk.Label(self.root, text="Age:", font=("Helvetica", 16), bg="light green", fg="black")
        self.age_label.place(relx=0.3, rely=0.5, anchor="center")
        self.age_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.age_entry.place(relx=0.7, rely=0.5, anchor="center")

        self.owner_name_label = tk.Label(self.root, text="Owner Name:", font=("Helvetica", 16), bg="light green", fg="black")
        self.owner_name_label.place(relx=0.3, rely=0.6, anchor="center")
        self.owner_name_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.owner_name_entry.place(relx=0.7, rely=0.6, anchor="center")

        self.contact_number_label = tk.Label(self.root, text="Contact Number:", font=("Helvetica", 16), bg="light green", fg="black")
        self.contact_number_label.place(relx=0.3, rely=0.7, anchor="center")
        self.contact_number_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.contact_number_entry.place(relx=0.7, rely=0.7, anchor="center")

        self.check_in_time_label = tk.Label(self.root, text="Check-in Time:", font=("Helvetica", 16), bg="light green", fg="black")
        self.check_in_time_label.place(relx=0.3, rely=0.8, anchor="center")
        self.check_in_time_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.check_in_time_entry.place(relx=0.7, rely=0.8, anchor="center")

        button_font = ("Helvetica", 16)
        self.add_button = tk.Button(self.root, text="Add", font=button_font, command=self.add_dog_details)
        self.add_button.place(relx=0.4, rely=0.9, anchor="center")

        self.clear_button = tk.Button(self.root, text="Clear", font=button_font, command=self.clear_fields)
        self.clear_button.place(relx=0.6, rely=0.9, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", font=button_font, command=self.back_to_admin_options_page)
        self.back_button.place(relx=0.5, rely=0.95, anchor="center")

        self.root.mainloop()

    def add_dog_details(self):
        dog_id = self.dog_id_entry.get().strip()
        dog_name = self.dog_name_entry.get().strip()
        breed = self.breed_entry.get().strip()
        age = self.age_entry.get().strip()
        owner_name = self.owner_name_entry.get().strip()
        contact_number = self.contact_number_entry.get().strip()
        check_in_time = self.check_in_time_entry.get().strip()

        error_message = ""

        if not self.validate_dog_id(dog_id):
            error_message += "Dog ID must be numeric and cannot be empty.\n"
        if not self.validate_dog_name(dog_name):
            error_message += "Dog Name can only contain letters and spaces and cannot be empty.\n"
        if not self.validate_breed(breed):
            error_message += "Breed can only contain letters and spaces and cannot be empty.\n"
        if not self.validate_age(age):
            error_message += "Age must be a number and cannot be empty.\n"
        if not self.validate_owner_name(owner_name):
            error_message += "Owner Name can only contain letters and spaces and cannot be empty.\n"
        if not self.validate_contact_number(contact_number):
            error_message += "Contact Number must be numeric and cannot be empty.\n"
        if not self.validate_check_in_time(check_in_time):
            error_message += "Check-in Time must be in HH:MM format.\n"

        if error_message:
            messagebox.showerror("Error", error_message)
        else:
            query = '''INSERT INTO dog_details (dog_id, dog_name, breed, age, owner_name, contact_number, check_in_time)
                       VALUES (?, ?, ?, ?, ?, ?, ?)'''
            try:
                self.cursor.execute(query, (dog_id, dog_name, breed, age, owner_name, contact_number, check_in_time))
                self.conn.commit()
                messagebox.showinfo("Success", "Dog details added successfully!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Failed to add dog details.")

    def validate_dog_id(self, dog_id):
        return dog_id.isdigit() and bool(dog_id)

    def validate_dog_name(self, dog_name):
        return all(char.isalpha() or char.isspace() for char in dog_name) and bool(dog_name)

    def validate_breed(self, breed):
        return all(char.isalpha() or char.isspace() for char in breed) and bool(breed)

    def validate_age(self, age):
        return age.isdigit() and bool(age)

    def validate_owner_name(self, owner_name):
        return all(char.isalpha() or char.isspace() for char in owner_name) and bool(owner_name)

    def validate_contact_number(self, contact_number):
        return contact_number.isdigit() and bool(contact_number)

    def validate_check_in_time(self, check_in_time):
        try:
            datetime.strptime(check_in_time, '%H:%M')
            return True
        except ValueError:
            return False

    def clear_fields(self):
        self.dog_id_entry.delete(0, tk.END)
        self.dog_name_entry.delete(0, tk.END)
        self.breed_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.owner_name_entry.delete(0, tk.END)
        self.contact_number_entry.delete(0, tk.END)
        self.check_in_time_entry.delete(0, tk.END)

    def back_to_admin_options_page(self):
        self.root.destroy()
        admin_options_page = AdminOptionsPage()
        
class DeleteDetailsPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Delete Dog Details")
        self.root.geometry("1000x800")
        self.root.configure(bg="light yellow")  

        self.conn = sqlite3.connect('dog_daycare.db')  
        self.cursor = self.conn.cursor()

        pil_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\projectimage1.jpg') 
        pil_image = pil_image.resize((pil_image.width * 3, pil_image.height * 3))
        self.background_image = ImageTk.PhotoImage(pil_image)

        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(relx=0.5, rely=0.5, anchor="center")

        heading_font = ("Helvetica", 36, "bold")
        self.heading_label = tk.Label(self.root, text="DELETE DOG DETAILS", font=heading_font, bg="light yellow", fg="black")
        self.heading_label.place(relx=0.5, rely=0.1, anchor="center")

        self.dog_id_label = tk.Label(self.root, text="Dog ID:", font=("Helvetica", 16), bg="light yellow", fg="black")
        self.dog_id_label.place(relx=0.35, rely=0.4, anchor="center")
        self.dog_id_entry = tk.Entry(self.root, font=("Helvetica", 14), width=10)
        self.dog_id_entry.place(relx=0.65, rely=0.4, anchor="center")

        button_font = ("Helvetica", 16)
        self.delete_button = tk.Button(self.root, text="Delete", font=button_font, command=self.delete_dog_details)
        self.delete_button.place(relx=0.3, rely=0.6, anchor="center")

        self.clear_button = tk.Button(self.root, text="Clear", font=button_font, command=self.clear_fields)
        self.clear_button.place(relx=0.5, rely=0.6, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", font=button_font, command=self.back_to_admin_options_page)
        self.back_button.place(relx=0.7, rely=0.6, anchor="center")

        self.root.mainloop()

    def delete_dog_details(self):
        dog_id = self.dog_id_entry.get().strip()
        
        self.cursor.execute("SELECT * FROM dog_details WHERE dog_id=?", (dog_id,))
        result = self.cursor.fetchone()

        if result:
            self.cursor.execute("DELETE FROM dog_details WHERE dog_id=?", (dog_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Dog details deleted successfully!")
        else:
            messagebox.showerror("Error", "Invalid Dog ID")

    def clear_fields(self):
        self.dog_id_entry.delete(0, tk.END)

    def back_to_admin_options_page(self):
        self.root.destroy()
        admin_options_page = AdminOptionsPage()

class UpdateDetailsPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("UPDATE Dog Details")
        self.root.geometry("1000x400")
        self.root.configure(bg="sky blue")

        self.conn = sqlite3.connect('dog_daycare.db')
        self.cursor = self.conn.cursor()

        background_image = tk.PhotoImage(file='C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\update-transformed.png')
        background_label = tk.Label(self.root, image=background_image)
        background_label.place(relx=0.5, rely=0.5, anchor="center")

        heading_font = ("Helvetica", 20, "bold")
        self.heading_label = tk.Label(self.root, text="UPDATE DOG DETAILS", font=heading_font, bg="sky blue", fg="white")
        self.heading_label.place(relx=0.5, rely=0.1, anchor="center")

        self.dog_id_label = tk.Label(self.root, text="Dog ID:", font=("Helvetica", 12), bg="sky blue", fg="white")
        self.dog_id_label.place(relx=0.3, rely=0.2, anchor="center")
        self.dog_id_entry = tk.Entry(self.root)
        self.dog_id_entry.place(relx=0.7, rely=0.2, anchor="center")

        self.update_button = tk.Button(self.root, text="UPDATE", command=self.open_update_details_page, font=("Helvetica", 16))
        self.update_button.place(relx=0.5, rely=0.3, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", command=self.back_to_admin_options_page, font=("Helvetica", 16))
        self.back_button.place(relx=0.5, rely=0.8, anchor="center")

        self.root.mainloop()

    def open_update_details_page(self):
        self.update_details_window = tk.Toplevel(self.root)
        self.update_details_window.title("Update Details Form")
        self.update_details_window.geometry("1000x800")

        background_image = tk.PhotoImage(file='C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\update_form.png')
        background_label = tk.Label(self.update_details_window, image=background_image)
        background_label.place(relx=0.5, rely=0.5, anchor="center")

        self.update_heading_label = tk.Label(self.update_details_window, text="UPDATE DETAILS FORM", font=("Helvetica", 20, "bold"))
        self.update_heading_label.place(relx=0.5, rely=0.1, anchor="center")

        self.dog_id_label = tk.Label(self.update_details_window, text="Dog ID:", font=("Helvetica", 22))
        self.dog_id_label.place(relx=0.3, rely=0.2, anchor="center")
        self.dog_id_entry = tk.Entry(self.update_details_window)
        self.dog_id_entry.place(relx=0.5, rely=0.2, anchor="center")

        self.fetch_button = tk.Button(self.update_details_window, text="Fetch Details", command=self.fetch_details)
        self.fetch_button.place(relx=0.5, rely=0.3, anchor="center")

        self.dog_name_label = tk.Label(self.update_details_window, text="Dog Name:", font=("Helvetica", 22))
        self.dog_name_label.place(relx=0.3, rely=0.4, anchor="center")
        self.dog_name_entry = tk.Entry(self.update_details_window)
        self.dog_name_entry.place(relx=0.7, rely=0.4, anchor="center")

        self.dog_breed_label = tk.Label(self.update_details_window, text="Breed:", font=("Helvetica", 22))
        self.dog_breed_label.place(relx=0.3, rely=0.5, anchor="center")
        self.dog_breed_entry = tk.Entry(self.update_details_window)
        self.dog_breed_entry.place(relx=0.7, rely=0.5, anchor="center")

        self.dog_age_label = tk.Label(self.update_details_window, text="Age:", font=("Helvetica", 22))
        self.dog_age_label.place(relx=0.3, rely=0.6, anchor="center")
        self.dog_age_entry = tk.Entry(self.update_details_window)
        self.dog_age_entry.place(relx=0.7, rely=0.6, anchor="center")

        self.owner_name_label = tk.Label(self.update_details_window, text="Owner Name:", font=("Helvetica", 22))
        self.owner_name_label.place(relx=0.3, rely=0.7, anchor="center")
        self.owner_name_entry = tk.Entry(self.update_details_window)
        self.owner_name_entry.place(relx=0.7, rely=0.7, anchor="center")

        self.owner_contact_label = tk.Label(self.update_details_window, text="Contact Number:", font=("Helvetica", 22))
        self.owner_contact_label.place(relx=0.3, rely=0.8, anchor="center")
        self.owner_contact_entry = tk.Entry(self.update_details_window)
        self.owner_contact_entry.place(relx=0.7, rely=0.8, anchor="center")

        self.submit_button = tk.Button(self.update_details_window, text="Update Details", command=self.update_details)
        self.submit_button.place(relx=0.5, rely=0.9, anchor="center")
        
        self.clear_button = tk.Button(self.update_details_window, text="Clear", command=self.clear_fields)
        self.clear_button.place(relx=0.4, rely=0.9, anchor="center")

        self.update_details_window.mainloop()

    def clear_fields(self):
        self.dog_id_entry.delete(0, tk.END)
        self.dog_name_entry.delete(0, tk.END)
        self.dog_breed_entry.delete(0, tk.END)
        self.dog_age_entry.delete(0, tk.END)
        self.owner_name_entry.delete(0, tk.END)
        self.owner_contact_entry.delete(0, tk.END)

    def fetch_details(self):
        dog_id = self.dog_id_entry.get()
        if not self.validate_dog_id(dog_id):
            messagebox.showerror("Error", "Dog ID must be a digit.")
            return

        try:
            sql = "SELECT * FROM dog_details WHERE dog_id = ?"
            self.cursor.execute(sql, (dog_id,))
            dog_details = self.cursor.fetchone()

            if dog_details:
                self.dog_name_entry.delete(0, tk.END)
                self.dog_name_entry.insert(0, dog_details[1])
                self.dog_breed_entry.delete(0, tk.END)
                self.dog_breed_entry.insert(0, dog_details[2])
                self.dog_age_entry.delete(0, tk.END)
                self.dog_age_entry.insert(0, dog_details[3])
                self.owner_name_entry.delete(0, tk.END)
                self.owner_name_entry.insert(0, dog_details[4])
                self.owner_contact_entry.delete(0, tk.END)
                self.owner_contact_entry.insert(0, dog_details[5])
            else:
                messagebox.showerror("Error", "Dog ID not found. Please check and try again.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching details: {str(e)}")

    def update_details(self):
        dog_id = self.dog_id_entry.get()
        dog_name = self.dog_name_entry.get()
        dog_breed = self.dog_breed_entry.get()
        dog_age = self.dog_age_entry.get()
        owner_name = self.owner_name_entry.get()
        owner_contact = self.owner_contact_entry.get()

        error_messages = []
        if not self.validate_dog_id(dog_id):
            error_messages.append("Dog ID must be a digit.")
        if not self.validate_dog_name(dog_name):
            error_messages.append("Dog Name must be alphabetic and cannot be empty.")
        if not self.validate_dog_breed(dog_breed):
            error_messages.append("Breed must be alphabetic and cannot be empty.")
        if not self.validate_dog_age(dog_age):
            error_messages.append("Age must be a digit and cannot be empty.")
        if not self.validate_owner_name(owner_name):
            error_messages.append("Owner Name must be alphabetic and cannot be empty.")
        if not self.validate_contact_number(owner_contact):
            error_messages.append("Contact number must be a digit and cannot be empty.")

        if error_messages:
            messagebox.showerror("Error", "\n".join(error_messages))
            return  

        try:
            sql = "UPDATE dog_details SET dog_name = ?, breed = ?, age = ?, owner_name = ?, contact_number = ? WHERE dog_id = ?"
            data = (dog_name, dog_breed, dog_age, owner_name, owner_contact, dog_id)
            self.cursor.execute(sql, data)
            self.conn.commit()
            messagebox.showinfo("Success", "Details updated successfully.")
            self.update_details_window.destroy()  
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def validate_dog_id(self, dog_id):
        return dog_id.isdigit()

    def validate_dog_name(self, dog_name):
        return bool(dog_name) and all(char.isalpha() or char.isspace() for char in dog_name)

    def validate_dog_breed(self, dog_breed):
        return bool(dog_breed) and all(char.isalpha() or char.isspace() for char in dog_breed)

    def validate_dog_age(self, dog_age):
        return dog_age.isdigit()

    def validate_owner_name(self, owner_name):
        return bool(owner_name) and all(char.isalpha() or char.isspace() for char in owner_name)

    def validate_contact_number(self, contact_number):
        return contact_number.isdigit()

    def back_to_admin_options_page(self):
        self.root.destroy()
        admin_options_page = AdminOptionsPage()
class ViewMemberDetailsPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dog Daycare Details")
        self.root.geometry("1600x800")
        self.root.configure(bg="sky blue")
        self.conn = sqlite3.connect("dog_daycare.db")
        self.cursor = self.conn.cursor()

        pil_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\member_detail-transformed.png')
        pil_image = pil_image.resize((1600, 800), Image.NEAREST)
        self.background_image = ImageTk.PhotoImage(pil_image)
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(relx=0.5, rely=0.5, anchor="center")
        background_label.lower()

        heading_font = ("Helvetica", 36)
        self.heading_label = tk.Label(self.root, text="Dog Daycare Details", font=heading_font, bg="sky blue", fg="white")
        self.heading_label.place(relx=0.5, rely=0.1, anchor="center")

        self.member_details_label = tk.Label(self.root, text="", font=("Helvetica", 16), bg="sky blue", fg="black")
        self.member_details_label.place(relx=0.5, rely=0.4, anchor="center")

        button_font = ("Helvetica", 16)
        self.previous_button = tk.Button(self.root, text="Previous", font=button_font, command=self.show_previous_Member)
        self.previous_button.place(relx=0.3, rely=0.7, anchor="center")

        self.next_button = tk.Button(self.root, text="Next", font=button_font, command=self.show_next_Member)
        self.next_button.place(relx=0.7, rely=0.7, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", font=button_font, command=self.back_to_admin_options)
        self.back_button.place(relx=0.5, rely=0.9, anchor="center")

        self.current_member_index = 0
        self.all_members = self.fetch_all_members()
        self.show_member_details()

        self.root.mainloop()

    def fetch_all_members(self):
        query = "SELECT * FROM dog_details"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def show_member_details(self):
        if self.all_members:
            member = self.all_members[self.current_member_index]
            print("Member tuple:", member)  
            member_details_text = (f"Dog ID: {member[0]}\nName: {member[1]}\nBreed: {member[2]}"
                                   f"\nAge: {member[3]}\nOwner Name: {member[4]}\nOwner Contact: {member[5]}")
            self.member_details_label.config(text=member_details_text)
        else:
            self.member_details_label.config(text="No dog details found.")

    def show_next_Member(self):
        if self.all_members:
            self.current_member_index = (self.current_member_index + 1) % len(self.all_members)
            self.show_member_details()

    def show_previous_Member(self):
        if self.all_members:
            self.current_member_index = (self.current_member_index - 1) % len(self.all_members)
            self.show_member_details()

    def back_to_admin_options(self):
        self.root.destroy()
        admin_options_page = AdminOptionsPage()

class ViewBookingDetailsPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("View Booking Details")
        self.root.geometry("1600x800")
        self.root.configure(bg="light yellow")

        
        self.load_background_image()

        
        heading_font = ("Helvetica", 24, "bold")
        tk.Label(self.root, text="Booking Details", font=heading_font, bg="light yellow").place(relx=0.5, rely=0.05, anchor="center")

        
        instruction_label = tk.Label(self.root, text="Dog ID:", font=("Helvetica", 14), bg="light yellow")
        instruction_label.place(relx=0.35, rely=0.1, anchor="center")

        self.dog_id_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.dog_id_entry.place(relx=0.5, rely=0.1, anchor="center")

       
        submit_button = tk.Button(self.root, text="Submit", command=self.display_booking_details, font=("Helvetica", 16))
        submit_button.place(relx=0.7, rely=0.1, anchor="center")

        clear_button = tk.Button(self.root, text="Clear", command=self.clear_fields, font=("Helvetica", 16))
        clear_button.place(relx=0.8, rely=0.1, anchor="center")

        view_all_button = tk.Button(self.root, text="View All Bookings", command=self.show_all_bookings, font=("Helvetica", 16))
        view_all_button.place(relx=0.5, rely=0.2, anchor="center")

        back_button = tk.Button(self.root, text="Back", command=self.back_to_admin_options, font=("Helvetica", 16))
        back_button.place(relx=0.05, rely=0.05)

       
        self.conn = sqlite3.connect("dog_daycare.db")
        self.cursor = self.conn.cursor()

        self.details_frame = tk.Frame(self.root, bg="light yellow")
        self.details_frame.place(relx=0.5, rely=0.35, anchor="center")

        self.root.mainloop()

    def load_background_image(self):
        pil_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\add_details-transformed.png')
        pil_image = pil_image.resize((1600, 800))
        self.background_image = ImageTk.PhotoImage(pil_image)
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def fetch_booking_details(self, dog_id):
        self.cursor.execute("SELECT dog_id, dog_name, owner_name, contact_number FROM dog_details WHERE dog_id = ?", (dog_id,))
        return self.cursor.fetchone()

    def fetch_all_bookings(self):
        self.cursor.execute("SELECT dog_id, dog_name, owner_name, contact_number FROM dog_details")
        return self.cursor.fetchall()

    def display_booking_details(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        dog_id = self.dog_id_entry.get()

        if not dog_id.isdigit():
            messagebox.showerror("Error", "Dog ID must be a digit.")
            return

        booking_details = self.fetch_booking_details(dog_id)
        if booking_details:
            labels = [
                ("Dog ID: ", booking_details[0]),
                ("Dog Name: ", booking_details[1]),
                ("Owner Name: ", booking_details[2]),
                ("Contact Number: ", booking_details[3])
            ]

            for i, (text, detail) in enumerate(labels):
                tk.Label(self.details_frame, text=f"{text}{detail}", font=("Helvetica", 18), bg="light yellow").grid(row=i, column=0, padx=10, pady=10, sticky="w")

        else:
            messagebox.showerror("Error", "Dog ID not found.")

        self.dog_id_entry.delete(0, tk.END)

    def show_all_bookings(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        booking_details = self.fetch_all_bookings()
        if booking_details:
            for index, details in enumerate(booking_details):
                labels = [
                    ("Dog ID: ", details[0]),
                    ("Dog Name: ", details[1]),
                    ("Owner Name: ", details[2]),
                    ("Contact Number: ", details[3])
                ]
                for i, (text, detail) in enumerate(labels):
                    tk.Label(self.details_frame, text=f"{text}{detail}", font=("Helvetica", 14), bg="light yellow").grid(row=index, column=i, padx=10, pady=5, sticky="w")
        else:
            messagebox.showinfo("Info", "No bookings found.")

    def clear_fields(self):
        self.dog_id_entry.delete(0, tk.END)

    def back_to_admin_options(self):
        self.root.destroy()
        AdminOptionsPage()
      
        
class CustomerLoginPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Customer Login")
        self.root.geometry("1000x800")
        self.root.configure(bg="sky blue")

        heading_font = ("Helvetica", 36, "bold")
        heading_label = tk.Label(self.root, text="CUSTOMER LOGIN", font=heading_font, bg="sky blue", fg="white")
        heading_label.place(relx=0.5, rely=0.1, anchor="center")

        pil_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\customer-transformed.png')
        pil_image = pil_image.resize((pil_image.width * 3, pil_image.height * 3))
        login_image = ImageTk.PhotoImage(pil_image)
        login_image_label = tk.Label(self.root, image=login_image)
        login_image_label.place(relx=0.5, rely=0.3, anchor="center")

        self.username_label = tk.Label(self.root, text="Username:", font=("Helvetica", 20), bg="sky blue", fg="white")
        self.username_label.place(relx=0.3, rely=0.4, anchor="center")
        self.username_entry = tk.Entry(self.root, font=("Helvetica", 16), width=25)
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")

        self.password_label = tk.Label(self.root, text="Password:", font=("Helvetica", 20), bg="sky blue", fg="white")
        self.password_label.place(relx=0.3, rely=0.5, anchor="center")
        self.password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 16), width=25)
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")

        self.login_button = tk.Button(self.root, text="Login", command=self.login, font=("Helvetica", 16), width=8, height=1)
        self.login_button.place(relx=0.5, rely=0.6, anchor="center")

        self.signup_button = tk.Button(self.root, text="Sign up", command=self.open_signup_page, font=("Helvetica", 16), width=8, height=1)
        self.signup_button.place(relx=0.5, rely=0.7, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", command=self.back_to_homepage, font=("Helvetica", 16), width=8, height=1)
        self.back_button.place(relx=0.5, rely=0.8, anchor="center")

        self.root.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.validate_username(username) and self.validate_password(password):
            if username == "cust" and password == "cust@01":
                messagebox.showinfo("Success", "Logged in as customer!")
                self.root.destroy()
                CustomerOptionsPage()  
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "Invalid username or password format.")

    def validate_username(self, username):
        return username.isalnum()

    def validate_password(self, password):
        return (any(c.isalpha() for c in password) and
                any(c.isdigit() for c in password) and
                any(not c.isalnum() for c in password))

    def open_signup_page(self):
        self.root.destroy()
        SignupPage()

    def open_customer_options(self):
        self.root.destroy()
        CustomerOptionsPage(self.root)    

    def back_to_homepage(self):
     self.root.destroy()
     root = tk.Tk()
     HomePage(root)
     root.mainloop()

class SignupPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Signup")
        self.root.geometry("1000x800")
        self.root.configure(bg="sky blue")

        pil_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\sign_up-transformed.png')
        pil_image = pil_image.resize((pil_image.width * 3, pil_image.height * 3))
        login_image = ImageTk.PhotoImage(pil_image)
        login_image_label = tk.Label(self.root, image=login_image)
        login_image_label.place(relx=0.5, rely=0.3, anchor="center")

        heading_font = ("Helvetica", 36, "bold")
        heading_label = tk.Label(self.root, text="Signup", font=heading_font, bg="sky blue", fg="white")
        heading_label.place(relx=0.5, rely=0.1, anchor="center")

        self.username_label = tk.Label(self.root, text="Username:", font=("Helvetica", 22), bg="sky blue", fg="white")
        self.username_label.place(relx=0.3, rely=0.3, anchor="center")
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.place(relx=0.7, rely=0.3, anchor="center")

        self.phone_label = tk.Label(self.root, text="Phone Number:", font=("Helvetica", 22), bg="sky blue", fg="white")
        self.phone_label.place(relx=0.3, rely=0.4, anchor="center")
        self.phone_entry = tk.Entry(self.root, width=30)
        self.phone_entry.place(relx=0.7, rely=0.4, anchor="center")

        self.password_label = tk.Label(self.root, text="Password:", font=("Helvetica", 22), bg="sky blue", fg="white")
        self.password_label.place(relx=0.3, rely=0.5, anchor="center")
        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.place(relx=0.7, rely=0.5, anchor="center")

        self.retype_password_label = tk.Label(self.root, text="Retype Password:", font=("Helvetica", 22), bg="sky blue", fg="white")
        self.retype_password_label.place(relx=0.3, rely=0.6, anchor="center")
        self.retype_password_entry = tk.Entry(self.root, show="*", width=30)
        self.retype_password_entry.place(relx=0.7, rely=0.6, anchor="center")

        self.signup_button = tk.Button(self.root, text="Signup", command=self.signup, width=20, height=2)
        self.signup_button.place(relx=0.5, rely=0.7, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", command=self.open_customer_login, width=20, height=2)
        self.back_button.place(relx=0.5, rely=0.8, anchor="center")

        self.root.mainloop()

    def open_customer_login(self):
        self.root.destroy()
        CustomerLoginPage()

    def signup(self):
        username = self.username_entry.get()
        phone_number = self.phone_entry.get()
        password = self.password_entry.get()
        retype_password = self.retype_password_entry.get()

        if (self.validate_username(username) and
                self.validate_phone_number(phone_number) and
                self.validate_password(password) and
                self.validate_retype_password(password, retype_password)):
            self.save_to_database(username, phone_number, password)
            messagebox.showinfo("Success", "Signup successful!")
            self.open_customer_login()
        else:
            messagebox.showerror("Error", "Invalid input or passwords do not match.")

    def validate_username(self, username):
        return username.isalnum()

    def validate_phone_number(self, phone_number):
        return (phone_number.isdigit() and
                len(phone_number) == 10 and
                phone_number[0] in ['7', '8', '9'])

    def validate_password(self, password):
        return (len(password) >= 8 and
                any(c.isalpha() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in "!@#$%^&*()-_+=" for c in password))

    def validate_retype_password(self, password, retype_password):
        return password == retype_password

    def save_to_database(self, username, phone_number, password):
        try:
            conn = sqlite3.connect('dog_daycare.db')  
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS customer_details 
                           (username TEXT PRIMARY KEY, phone_number TEXT, password TEXT)''')
            cur.execute("INSERT INTO customer_details (username, phone_number, password) VALUES (?, ?, ?)",
                        (username, phone_number, password))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def back_to_homepage(self):
        self.root.destroy()
        HomePage()
      

class CustomerOptionsPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Customer Options")
        self.root.geometry("1000x800")
        self.root.configure(bg="sky blue")

        
        bg_image_path = r'C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\customer_options-transformed.png'
        bg_image = Image.open(bg_image_path)
        resized_bg_image = bg_image.resize((1000, 800), Image.NEAREST)
        self.background_image = ImageTk.PhotoImage(resized_bg_image)
        
        
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.image = self.background_image  
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        heading_font = ("Helvetica", 36, "bold")
        heading_label = tk.Label(self.root, text="Customer Options", font=heading_font, bg="sky blue", fg="white")
        heading_label.place(relx=0.5, rely=0.1, anchor="center")

        self.conn, self.cur = self.connect_to_database()

        self.dog_service_button = tk.Button(self.root, text="Dog Service", command=self.open_dog_service_page, font=("Helvetica", 16))
        self.dog_service_button.place(relx=0.5, rely=0.2, anchor="center")

        self.view_dogs_button = tk.Button(self.root, text="View Dogs", command=self.view_dogs, font=("Helvetica", 20))
        self.view_dogs_button.place(relx=0.5, rely=0.3, anchor="center")

        self.search_dogs_button = tk.Button(self.root, text="Search Page", command=self.open_search_page, font=("Helvetica", 20))
        self.search_dogs_button.place(relx=0.5, rely=0.4, anchor="center")

        self.view_registration_button = tk.Button(self.root, text="Member Detail Page", command=self.open_registration_page, font=("Helvetica", 20))
        self.view_registration_button.place(relx=0.5, rely=0.5, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", command=self.back_to_login, font=("Helvetica", 20))
        self.back_button.place(relx=0.5, rely=0.6, anchor="center")

    def connect_to_database(self):
        try:
            conn = sqlite3.connect('dog_daycare.db')
            cur = conn.cursor()
            return conn, cur
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Unable to connect to the database: {e}")
            return None, None

    def open_dog_service_page(self):
         new_window = tk.Toplevel(self.root)
         DogServicePage(new_window)

    def view_dogs(self):
         new_window = tk.Toplevel(self.root)
         viewDogsPage(new_window, self.conn, self.cur)

    def open_search_page(self):
         new_window = tk.Toplevel(self.root)
         SearchPage(new_window)

    def open_registration_page(self):
        new_window = tk.Toplevel(self.root)
        MemberDetailPage(new_window)

    
    def back_to_login(self):
        self.root.destroy()
        CustomerLoginPage()    
        

  


class DogServicePage:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(self.parent)
        self.root.title("Dog Service")
        self.root.geometry("1000x800")
        self.root.configure(bg="sky blue")

        bg_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\service type.png')
        resized_bg_image = bg_image.resize((1000, 800), Image.NEAREST)
        self.background_image = ImageTk.PhotoImage(resized_bg_image)
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        heading_font = ("Helvetica", 24, "bold")
        heading_label = tk.Label(self.root, text="Dog Service", font=heading_font, bg="sky blue", fg="black")
        heading_label.pack(pady=20)

        self.conn, self.cur = self.connect_to_database()

        
        self.dog_id_label = tk.Label(self.root, text="Dog ID:", font=("Helvetica", 16), bg="sky blue")
        self.dog_id_label.pack(pady=5)
        self.dog_id_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.dog_id_entry.pack(pady=5)

       
        self.member_id_label = tk.Label(self.root, text="Member ID:", font=("Helvetica", 16), bg="sky blue")
        self.member_id_label.pack(pady=5)
        self.member_id_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.member_id_entry.pack(pady=5)

        
        self.service_id_label = tk.Label(self.root, text="Service ID:", font=("Helvetica", 16), bg="sky blue")
        self.service_id_label.pack(pady=5)
        self.service_id_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.service_id_entry.pack(pady=5)

        
        self.service_label = tk.Label(self.root, text="Service Type:", font=("Helvetica", 16), bg="sky blue")
        self.service_label.pack(pady=5)
        self.service_type = tk.StringVar(self.root)
        self.service_type.set("Select Service")  
        self.service_options = ["Grooming", "Training", "Daycare", "Walking"]
        self.service_menu = tk.OptionMenu(self.root, self.service_type, *self.service_options)
        self.service_menu.pack(pady=5)

        
        self.register_service_button = tk.Button(self.root, text="Book Service", command=self.book_service, font=("Helvetica", 16))
        self.register_service_button.pack(pady=10)

       
        self.back_button = tk.Button(self.root, text="Back", command=self.go_back, font=("Helvetica", 16))
        self.back_button.pack(pady=10)

    def connect_to_database(self):
        try:
            conn = sqlite3.connect('dog_daycare.db')
            cur = conn.cursor()
            return conn, cur
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Unable to connect to the database: {e}")
            return None, None

    def book_service(self):
        dog_id = self.dog_id_entry.get()
        member_id = self.member_id_entry.get()
        service_id = self.service_id_entry.get()
        service = self.service_type.get()

        if not dog_id.isdigit():
            messagebox.showerror("Error", "Dog ID must be numeric")
            return

        if not member_id.isdigit():
            messagebox.showerror("Error", "Member ID must be numeric")
            return

        if not service_id.isdigit():
            messagebox.showerror("Error", "Service ID must be numeric")
            return

        if service == "Select Service":
            messagebox.showerror("Error", "Please select a service")
            return

        try:
            query = '''INSERT INTO dog_services (service_id, dog_id, member_id, service_type) VALUES (?, ?, ?, ?)'''
            self.cur.execute(query, (service_id, dog_id, member_id, service))
            self.conn.commit()
            messagebox.showinfo("Success", "Service booked successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error booking service: {e}")

    def go_back(self):
        self.root.destroy()
        CustomerOptionsPage()        

class viewDogsPage:
    def __init__(self, parent, conn, cur):
        self.parent = parent
        self.conn = conn
        self.cur = cur
        self.current_dog_index = 0
        self.root = tk.Toplevel(self.parent)
        self.root.title("Show Dogs in Daycare")
        self.root.geometry("1000x800")
        self.root.configure(bg="sky blue")

        
        bg_image_path = "C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\4dog.jpeg\welcome.png"
        bg_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\searchbyid-transformed.png')
        resized_bg_image = bg_image.resize((1000, 800), Image.NEAREST)  
        self.background_image = ImageTk.PhotoImage(resized_bg_image)
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.dog_text = tk.Text(self.root, font=("Helvetica", 12), height=15, width=70)
        self.dog_text.place(relx=0.5, rely=0.5, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", command=self.go_back, font=("Helvetica", 16))
        self.back_button.place(relx=0.1, rely=0.9)

        self.next_button = tk.Button(self.root, text="Next", command=self.view_next_dog, font=("Helvetica", 16))
        self.next_button.place(relx=0.5, rely=0.9)

        self.previous_button = tk.Button(self.root, text="Previous", command=self.view_previous_dog, font=("Helvetica", 16))
        self.previous_button.place(relx=0.3, rely=0.9)

        self.view_dogs()

    def view_dogs(self):
        if self.cur:
            self.cur.execute("SELECT * FROM dog_details")  
            self.dogs = self.cur.fetchall()
            self.view_current_dog()

    def view_current_dog(self):
        if self.dogs:
            dog = self.dogs[self.current_dog_index]
            self.dog_text.delete(1.0, tk.END)
            self.dog_text.insert(tk.END, f"Dog ID: {dog[0]}\n")
            self.dog_text.insert(tk.END, f"Name: {dog[1]}\n")
            self.dog_text.insert(tk.END, f"Breed: {dog[2]}\n")
            self.dog_text.insert(tk.END, f"Age: {dog[3]}\n")
            self.dog_text.insert(tk.END, f"owner_name: {dog[4]}\n")
            self.dog_text.insert(tk.END, f"contact_number: {dog[5]}\n\n")
            self.dog_text.insert(tk.END, f"check_in_time: {dog[6]}\n\n")
        else:
            self.dog_text.delete(1.0, tk.END)
            self.dog_text.insert(tk.END, "No dogs available.")

    def view_next_dog(self):
        if self.dogs:
            self.current_dog_index = (self.current_dog_index + 1) % len(self.dogs)
            self.view_current_dog()

    def view_previous_dog(self):
        if self.dogs:
            self.current_dog_index = (self.current_dog_index - 1) % len(self.dogs)
            self.view_current_dog()

    def go_back(self):
        self.root.destroy()
        CustomerOptionsPage()


        
class SearchPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Search Dog Daycare Information")
        self.root.geometry("1000x800")
        self.root.configure(bg="sky blue")

        
        bg_image_path = r'C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\search_page-transformed.png'
        bg_image = Image.open(bg_image_path)
        resized_bg_image = bg_image.resize((1000, 800), Image.NEAREST)
        self.background_image = ImageTk.PhotoImage(resized_bg_image)
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.search_by_id_button = tk.Button(self.root, text="Search Dog by ID", command=self.go_to_search_by_id_page, font=("Helvetica", 16))
        self.search_by_id_button.place(relx=0.5, rely=0.3, anchor="center")

        self.search_by_name_button = tk.Button(self.root, text="Search Dog by Name", command=self.go_to_search_by_name_page, font=("Helvetica", 16))
        self.search_by_name_button.place(relx=0.5, rely=0.4, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", command=self.go_back_to_previous_page, font=("Helvetica", 16))
        self.back_button.place(relx=0.5, rely=0.6, anchor="center")

    def open_new_window(self, PageClass):
        new_window = Toplevel(self.root)
        PageClass(new_window)

    def go_to_search_by_id_page(self):
        self.open_new_window(SearchByIDPage)

    def go_to_search_by_name_page(self):
        self.open_new_window(SearchByNamePage)

    def go_back_to_previous_page(self):
        self.root.withdraw()

class SearchByIDPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Search Dog by ID")
        self.root.geometry("1000x800")
        self.root.configure(bg="sky blue")

        
        bg_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\member_details.png')
        resized_bg_image = bg_image.resize((1000, 800), Image.NEAREST)
        self.background_image = ImageTk.PhotoImage(resized_bg_image)
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.dog_id_label = tk.Label(self.root, text="Dog ID:", font=("Helvetica", 16), bg="sky blue", fg="black")
        self.dog_id_label.place(relx=0.2, rely=0.3, anchor="center")
        self.dog_id_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.dog_id_entry.place(relx=0.5, rely=0.3, anchor="center")

        self.search_button = tk.Button(self.root, text="Search", command=self.search_dog_by_id, font=("Helvetica", 16))
        self.search_button.place(relx=0.5, rely=0.5, anchor="center")

        self.result_text = tk.Text(self.root, font=("Helvetica", 12), height=10, width=50)
        self.result_text.place(relx=0.5, rely=0.7, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", command=self.go_back, font=("Helvetica", 16))
        self.back_button.place(relx=0.1, rely=0.9)

    def search_dog_by_id(self):
        dog_id = self.dog_id_entry.get()
        self.result_text.delete(1.0, tk.END)
        conn = sqlite3.connect('dog_daycare.db')  
        cur = conn.cursor()
        cur.execute("SELECT * FROM dog_details WHERE dog_id=?", (dog_id,))
        results = cur.fetchall()
        if results:
            for result in results:
                self.result_text.insert(tk.END, f"Dog ID: {result[0]}\n")
                self.result_text.insert(tk.END, f"Dog Name: {result[1]}\n")
                self.result_text.insert(tk.END, f"Breed: {result[2]}\n")
                self.result_text.insert(tk.END, f"Age: {result[3]}\n")
                self.result_text.insert(tk.END, f"Owner Name: {result[4]}\n")  
                self.result_text.insert(tk.END, f"Contact Number: {result[5]}\n\n")
                self.result_text.insert(tk.END, f"Check-in Time: {result[6]}\n\n")
        else:
            self.result_text.insert(tk.END, "No dogs found with the given ID.\n\n")
        conn.close()

    def go_back(self):
        self.root.destroy()


class SearchByNamePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Search Dog by Name")
        self.root.geometry("1000x800")
        self.root.configure(bg="sky blue")

        
        bg_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\member_details.png')
        resized_bg_image = bg_image.resize((1000, 800), Image.NEAREST)
        self.background_image = ImageTk.PhotoImage(resized_bg_image)
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.dog_name_label = tk.Label(self.root, text="Dog Name:", font=("Helvetica", 16), bg="sky blue", fg="black")
        self.dog_name_label.place(relx=0.2, rely=0.3, anchor="center")
        self.dog_name_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.dog_name_entry.place(relx=0.5, rely=0.3, anchor="center")

        self.search_button = tk.Button(self.root, text="Search", command=self.search_dog_by_name, font=("Helvetica", 16))
        self.search_button.place(relx=0.5, rely=0.5, anchor="center")

        self.result_text = tk.Text(self.root, font=("Helvetica", 12), height=10, width=50)
        self.result_text.place(relx=0.5, rely=0.7, anchor="center")

        self.back_button = tk.Button(self.root, text="Back", command=self.go_back, font=("Helvetica", 16))
        self.back_button.place(relx=0.1, rely=0.9)

    def search_dog_by_name(self):
        dog_name = self.dog_name_entry.get()
        self.result_text.delete(1.0, tk.END)
        conn = sqlite3.connect('dog_daycare.db')  
        cur = conn.cursor()
        cur.execute("SELECT * FROM dog_details WHERE dog_name=?", (dog_name,))
        results = cur.fetchall()
        if results:
            for result in results:
                self.result_text.insert(tk.END, f"Dog ID: {result[0]}\n")
                self.result_text.insert(tk.END, f"Dog Name: {result[1]}\n")
                self.result_text.insert(tk.END, f"Breed: {result[2]}\n")
                self.result_text.insert(tk.END, f"Age: {result[3]}\n")
                self.result_text.insert(tk.END, f"Owner Name: {result[4]}\n")  
                self.result_text.insert(tk.END, f"Contact Number: {result[5]}\n\n")
                self.result_text.insert(tk.END, f"Check-in Time: {result[6]}\n\n")
        else:
            self.result_text.insert(tk.END, "No dogs found with the given name.\n\n")
        conn.close()

    def go_back(self):
        self.root.destroy()

    def open_search_page():
        root = tk.Tk()
        app = SearchPage(root)
        root.mainloop()    

class MemberDetailPage:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(self.parent)  
        self.root.title("Register Dog")
        self.root.geometry("1600x800")
        self.root.configure(bg="sky blue")

        
        pil_image = Image.open('C:\\Users\\Aditya\\OneDrive\\Desktop\\PROJECT IMAGES\\dddd2.png')
        resized_image = pil_image.resize((1600, 800), Image.NEAREST)
        self.background_image = ImageTk.PhotoImage(resized_image)

        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        heading_font = ("Helvetica", 24, "bold")
        heading_label = tk.Label(self.root, text="Register Dog", font=heading_font, bg="sky blue", fg="black")
        heading_label.pack(pady=20)

        self.conn, self.cur = self.connect_to_database()

        
        self.dog_id_label = tk.Label(self.root, text="Dog ID:", font=("Helvetica", 16), bg="sky blue")
        self.dog_id_label.pack(pady=5)
        self.dog_id_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.dog_id_entry.pack(pady=5)

        self.fetch_dog_details_button = tk.Button(self.root, text="Fetch Dog Details", command=self.fetch_dog_details, font=("Helvetica", 16))
        self.fetch_dog_details_button.pack(pady=20)

       
        self.dog_name_label = tk.Label(self.root, text="Dog Name:", font=("Helvetica", 16), bg="sky blue")
        self.dog_name_label.pack(pady=5)
        self.dog_name_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.dog_name_entry.pack(pady=5)

        self.breed_label = tk.Label(self.root, text="Breed:", font=("Helvetica", 16), bg="sky blue")
        self.breed_label.pack(pady=5)
        self.breed_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.breed_entry.pack(pady=5)

        self.age_label = tk.Label(self.root, text="Age (in years):", font=("Helvetica", 16), bg="sky blue")
        self.age_label.pack(pady=5)
        self.age_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.age_entry.pack(pady=5)

        
        self.member_id_label = tk.Label(self.root, text="Member ID:", font=("Helvetica", 16), bg="sky blue")
        self.member_id_label.pack(pady=5)
        self.member_id_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.member_id_entry.pack(pady=5)

        self.member_name_label = tk.Label(self.root, text="Member Name:", font=("Helvetica", 16), bg="sky blue")
        self.member_name_label.pack(pady=5)
        self.member_name_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.member_name_entry.pack(pady=5)

        self.member_age_label = tk.Label(self.root, text="Member Age:", font=("Helvetica", 16), bg="sky blue")
        self.member_age_label.pack(pady=5)
        self.member_age_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.member_age_entry.pack(pady=5)

        self.member_contact_number_label = tk.Label(self.root, text="Member Contact Number:", font=("Helvetica", 16), bg="sky blue")
        self.member_contact_number_label.pack(pady=5)
        self.member_contact_number_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.member_contact_number_entry.pack(pady=5)

        
        self.register_button = tk.Button(self.root, text="Register Dog", command=self.register_dog, font=("Helvetica", 16))
        self.register_button.place(x=1400, y=10)  

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_fields, font=("Helvetica", 16))
        self.clear_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Back", command=self.go_back, font=("Helvetica", 16))
        self.back_button.place(x=1400, y=60)  

    def connect_to_database(self):
        try:
            conn = sqlite3.connect('dog_daycare.db') 
            cur = conn.cursor()
            return conn, cur
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Unable to connect to the database: {e}")
            return None, None

    def fetch_dog_details(self):
        dog_id = self.dog_id_entry.get()
        if not dog_id.isdigit():
            messagebox.showerror("Error", "Dog ID must be numeric")
            return
        try:
            query = '''SELECT dog_name, breed, age FROM dog_details WHERE dog_id=?'''
            self.cur.execute(query, (dog_id,))
            result = self.cur.fetchone()
            if result:
                self.dog_name_entry.delete(0, tk.END)
                self.dog_name_entry.insert(0, result[0])
                self.breed_entry.delete(0, tk.END)
                self.breed_entry.insert(0, result[1])
                self.age_entry.delete(0, tk.END)
                self.age_entry.insert(0, result[2])
            else:
                messagebox.showerror("Error", "Dog ID not found")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching dog details: {e}")

    def register_dog(self):
        dog_id = self.dog_id_entry.get()
        dog_name = self.dog_name_entry.get()
        breed = self.breed_entry.get()
        age = self.age_entry.get()
        member_id = self.member_id_entry.get()
        member_name = self.member_name_entry.get()
        member_age = self.member_age_entry.get()
        member_contact_number = self.member_contact_number_entry.get()

        if not dog_id.isdigit():
            messagebox.showerror("Error", "Dog ID must be numeric")
            return

        if not member_id.isdigit():
            messagebox.showerror("Error", "Member ID must be numeric")
            return

        if not member_name.isalpha():
            messagebox.showerror("Error", "Member name must be alphabetic")
            return

        if not member_age.isdigit() or not (18 <= int(member_age) <= 100):
            messagebox.showerror("Error", "Member age must be a positive integer between 18 and 100")
            return

        if not (member_contact_number.isdigit() and len(member_contact_number) == 10 and member_contact_number[0] in '789'):
            messagebox.showerror("Error", "Contact number must be a 10-digit number starting with 7, 8, or 9")
            return

        try:
            query_member = '''INSERT INTO member_details (member_id, member_name, member_age, member_contact_number, dog_id) VALUES (?, ?, ?, ?, ?)'''
            self.cur.execute(query_member, (member_id, member_name, member_age, member_contact_number, dog_id))

            query_dog = '''INSERT INTO dog_details (dog_id, dog_name, breed, age) VALUES (?, ?, ?, ?)'''
            self.cur.execute(query_dog, (dog_id, dog_name, breed, age))

            self.conn.commit()
            messagebox.showinfo("Success", "Member and Dog registered successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error registering member or dog: {e}")

    def clear_fields(self):
        self.dog_id_entry.delete(0, tk.END)
        self.dog_name_entry.delete(0, tk.END)
        self.breed_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.member_id_entry.delete(0, tk.END)
        self.member_name_entry.delete(0, tk.END)
        self.member_age_entry.delete(0, tk.END)
        self.member_contact_number_entry.delete(0, tk.END)

    def go_back(self):
        self.root.destroy()
        HomePage()

if __name__ == "__main__":
    root = tk.Tk()
    app = HomePage(root)
    root.mainloop()
