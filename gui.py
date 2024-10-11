#• Graphic User Interface (GUI) is required.
# Interface Page 1: Mr. Johnson can see the list of people and reservation details. 
# Interface Page 2: Any drivers can fill up a reservation form.
from tkinter import *
from tkinter import messagebox


def resservation_list():
    root= Tk()
    root.title("Page 1: The list of Reservation")

    Label(root, text ='Reservation ID').grid (row=0,column=0)
    Label(root, text = 'Driver ID').grid (row=1,column =0)
    Label(root, text = 'Car Type').grid (row=2,column =0)
    Label(root, text = 'Car ID').grid (row=3,column =0)
    Label(root, text = 'Checkout Time').grid (row=4,column =0)
    Label(root, text = 'Return Time').grid (row=5,column =0)

    Reservationid = Entry(root)
    Driverid = Entry(root)
    size_1 = Entry(root) 
    Carid= Entry(root)
    Checkouttime= Entry(root) 
    Returntime= Entry(root)

    Reservationid.grid(row=0, column =1)
    Driverid.grid(row=1, column =1)
    size_1.grid(row=2, column =1)
    Carid.grid(row=3, column =1)
    Checkouttime.grid(row=4, column =1)
    Returntime.grid(row=5, column =1)

    def reservation_made():
        add_to_reservation(Reservationid.get(),Driverid.get(),size_1.get(),
            Carid.get(),Checkouttime.get(),Returntime.get())
    
    Button(root, text="Submit", command=reservation_made).grid(row=6, column=0, columnspan=2)

    root.mainloop()



    

resservation_list()


#list



#form waiting to be fill up by drivers.