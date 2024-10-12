import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

class CarRental:
    def __init__(self, page):
        self.page = page
        self.page.title('Car Rental System')
        self.page.geometry("800x600")

        self.conn = sqlite3.connect('Car_Rental.db', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.notebook = ttk.Notebook(self.page)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.admin_frame = ttk.Frame(self.notebook)
        self.reservation_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.admin_frame, text='Admin View')
        self.notebook.add(self.reservation_frame, text="Reservation Form")

        self.drivers = self.load_drivers()

        self.setup_admin_view()
        self.setup_reservation_form()

    def setup_admin_view(self):
        columns = ('Reservation ID', 'Driver', 'Car', 'Checkout', 'Return', 'Price')
        self.tree = ttk.Treeview(self.admin_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(expand=1, fill="both")

        button_frame = ttk.Frame(self.admin_frame)
        button_frame.pack(fill='x', padx=5, pady=5)

        refresh_button = ttk.Button(button_frame, text='Refresh', command=self.refresh_reservations)
        refresh_button.pack(side='left', padx=5)

        cleanup_button = ttk.Button(button_frame, text="Clean All Reservations", command=self.cleanup_reservations)
        cleanup_button.pack(side='left', padx=5)

        self.refresh_reservations()

    def setup_reservation_form(self):
        fields = [
            ("driver_id", "Driver ID:", self.drivers),
            ("car_type", "Car Type:", ['sedan', 'SUV', 'Coupe', 'Truck']),
            ("checkout_time", "Checkout Time (YYYY-MM-DD HH:MM):", None),
            ("return_time", "Return Time (YYYY-MM-DD HH:MM):", None)
        ]

        self.entries = {}
        for i, (key, label, values) in enumerate(fields):
            ttk.Label(self.reservation_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            if values:
                entry = ttk.Combobox(self.reservation_frame, values=values)
            else:
                entry = ttk.Entry(self.reservation_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='we')
            self.entries[key] = entry

        submit_button = ttk.Button(self.reservation_frame, text="Submit Reservation", command=self.submit_reservation)
        submit_button.grid(row=len(fields), column=1, padx=5, pady=5)

        self.reservation_frame.columnconfigure(1, weight=1)

    def load_drivers(self):
        self.cursor.execute("SELECT Driver_id FROM Drivers")
        return [row[0] for row in self.cursor.fetchall()]

    def refresh_reservations(self):
        self.tree.delete(*self.tree.get_children())
        query = """
        SELECT r.Reservation_id, d.Driver_Name, c.Car_id, r.Checkout_time, r.Return_time, r.Price
        FROM Reservations r
        JOIN Drivers d ON r.Driver_id = d.Driver_id
        JOIN Cars c ON r.Car_id = c.Car_id
        """
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            self.tree.insert('', 'end', values=tuple(row))

    def submit_reservation(self):
        data = {key: entry.get() for key, entry in self.entries.items()}

        if not all(data.values()):
            messagebox.showerror('Error', 'All fields need to be filled.')
            return
        
        try:
            checkout = datetime.strptime(data['checkout_time'], "%Y-%m-%d %H:%M")
            if checkout < datetime.now() + timedelta(hours=24):
                messagebox.showerror("Error", "Reservation has to be booked 24hrs prior.")
                return
        except ValueError:
            messagebox.showerror('Error', "Invalid format of Date and Time.")
            return

        self.cursor.execute("SELECT Car_id FROM Cars WHERE Car_size_type = ? AND Car_reserved IS NULL LIMIT 1", (data['car_type'],))
        available_car = self.cursor.fetchone()

        if not available_car:
            messagebox.showerror('Error', "No available car.")
            return

        car_id = available_car[0]

        duration = datetime.strptime(data['return_time'], "%Y-%m-%d %H:%M") - checkout
        price = duration.days * 100 + duration.seconds // 3600 * 5

        reservation_id = f"RES{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        try:
            self.cursor.execute("""
            INSERT INTO Reservations (Reservation_id, Driver_id, Car_id, Size, Checkout_time, Return_time, Price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (reservation_id, data['driver_id'], car_id, data['car_type'], data['checkout_time'], data['return_time'], str(price)))
            
            self.cursor.execute("UPDATE Cars SET Car_reserved = 'Yes' WHERE Car_id = ?", (car_id,))
            
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            return

        messagebox.showinfo("Success", "Reservation made successfully.")
        self.refresh_reservations()

    def cleanup_reservations(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all reservations?"):
            try:
                self.cursor.execute("DELETE FROM Reservations")
                self.cursor.execute("UPDATE Cars SET Car_reserved = NULL")
                self.conn.commit()
                messagebox.showinfo("Success", "All reservations have been deleted")
                self.refresh_reservations()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = CarRental(root)
    root.mainloop()