import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

class CarRental:
    def __init__(self,page):
        self.page = page
        self.page.title ('Reservation')
        self.page.geometry("800x600")

    self.conn = sqlite3.connect ('Car_Rental.db')

    self.notebook =ttk.Notebook (self.page1)
    self.page.pack (expand=1,fill ='both')

    self.admin_frame = ttk.Frame (self.notebook)
    self.reservation_frame = ttk.Frame (self.notebook)

    self.notebook.add (self.admin_frame, text = 'Admin Form')
    self.notebook.add (self.reservation_frame, text ="Reservation Form")

    self.setup_admin_view()
    self.setup_reservation_form()


def setup_admin_form (self):
    self.tree = ttk.Treeview (self.admin_frame, columns = ('Reservation ID','Driver', 'Car', 'Checkout', 'Return', 'Price'), show='headings')
    self.tree.heading('Reservation ID', text='Reservation ID')
    self.tree.heading('Driver', text='Driver')
    self.tree.heading('Car', text='Car')
    self.tree.heading('Checkout', text='Checkout Time')
    self.tree.heading('Return', text='Return Time')
    self.tree.heading('Price', text='Price')
    self.tree.pack(expand=1, fill="both")

    refresh_button = ttk.Button (self.admin_frame, text ='Refresh', command= self.refresh_reservations)
    refresh_button.pack()

    self.refresh_reservations()


def setup_reservation_form(self):
        ytk.Label(self.reservation_frame, text="Driver ID:").grid(row=0, column=0, padx=5, pady=5)
        self.driver_id = ttk.Combobox(self.reservation_frame)
        self.driver_id.grid(row=0, column=1, padx=5, pady=5)
        self.load_drivers()

        ttk.Label(self.reservation_frame, text="Car Type:").grid(row=1, column=0, padx=5, pady=5)
        self.car_size = ttk.Combobox(self.reservation_frame, values=['sedan', 'SUV', 'Coupe', 'Truck'])
        self.car_size.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.reservation_frame, text="Checkout Time (YYYY-MM-DD HH:MM):").grid(row=2, column=0, padx=5, pady=5)
        self.checkout_time = ttk.Entry(self.reservation_frame)
        self.checkout_time.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.reservation_frame, text="Return Time (YYYY-MM-DD HH:MM):").grid(row=3, column=0, padx=5, pady=5)
        self.return_time = ttk.Entry(self.reservation_frame)
        self.return_time.grid(row=3, column=1, padx=5, pady=5)

        submit_button = ttk.Button(self.reservation_frame, text="Submit Reservation", command=self.submit_reservation)
        submit_button.grid(row=4, column=1, padx=5, pady=5)

def load_drivers(self):
     cursor = self.conn.cursor()
     cursor.execute ("Select Driver_id FROM Drivers")
     driver= [row[0] for row in cursor.fetchall()]
     self.driver_id['values'] = drivers 

def refresh_reservations(self):
    for i in self.tree.get_children():
         self.tree.delete(i)

    cursor = self.conn.cursor()
    cursor.execute("""
    SELECT r.Reservation_id, d.Driver_Name, c.Car_id, r.Checkout_time, r.Return_time, r.Price
    FROM Reservations r
    JOIN Drivers d ON r.Driver_id = d.Driver_id
    JOIN Cars c ON r.Car_id = c.Car_id
    """)
    for row in cursor.fetchall():
         self.tree.insert('','end',values=row)

def submot_reservation(self):
    driver_id = self.driver.id.get()
    car_size = self.car_size.get()
    checkout_time = self.checkout_time.get()
    return_time = self.return_time.get()

    if not all ([driver_id,car_size,checkout_time,return_time]):
        messagebox.showerror('Error','All fields need to be filled.')
        return
    
    try:
        checkout= datetime.strptime(checkout_time, "%Y-%m-%D %H:%M")
        if checkout < datetime.now() +timedelta(hours=24):
            messagebox.showerror("Error","Reservation has to be book 24hrs prior.")
            return
    except ValueError:
         messagebox.showerror('Error',"Invalid format of Date and Time.")
         return

    cursor = self.conn.cursor()


    cursor.execute("SELECT Car_id FROM Cars WHERE Car_size_type = ? AND Car_reserved IS NULL LIMIT 1", (car_size,))
    available_car = cursor.fetchone()

    if not available_car:
         messagebox.showerror('Error',"No available car.")

    car_id = available_car[0]

    #price calculation
    duration = datetime.strptime(return_time, "%Y-%m-%d %H:%M") - checkout
    price = duration.days*100 + duration.seconds //3600*5
    #Daily rate-100. Hourly rate -5.

    #Submit Reservation
    reservation_id =f"RES{datetime.now().strftime('%Y%m%d%H%M%S')}"
    cursor.execute("""
    INSERT INTO Reservations (Reservation_id, Driver_id, Car_id, Size, Checkout_time, Return_time, Price)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (reservation_id, driver_id, car_id, car_size,checkout_time, return_time, str(price)))
        
    #status
    cursor.execute("UPDATE Cars SET Car_reserved = 'Yes' WHERE Car_id = ?", (car_id,))
        
    self.conn.commit()

    messagebox.showinfo("Done","Reservation made.")
    self.refresh_reservations()
    

if __name__ == "__main__":
     root = tk.Tk()
     app = CarRental(root)
     root.mainloop()