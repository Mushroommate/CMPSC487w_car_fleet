import mysql.connector
from tkinter import *
from tkinter import messagebox

def database_carfleet():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password ="nyanchan22",
        database = "Car_Fleet"

    )
    return connection

def add_to_reservation (driver_id,car_type,check_time,return_time):
    connection = database_carfleet()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Reservation (Reservation_id, Driver_id,Size, Car_id,Checkout_time, Return_time) VALUES (%s, %s, %s, %s,%s,%s,%s)",
                       (Reservationid, Driverid,size_1, Carid,Checkouttime, Returntime))
        connection.commit()
        messagebox.showinfo ("Reservation made. Don't Forget to pick it up.")
    except mysql.connector.Error as err:
        messagebox.showerror("Not found. Try again later.")
    finally:
        cursor.close()
        connection.close()
