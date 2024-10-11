CREATE DATABASE Car_Rental;

USE Car_Rental;

CREATE TABLE Cars(
	Car_id VARCHAR(10) PRIMARY KEY,
    Car_color VARCHAR(20),
    Car_size_type VARCHAR(20),
    Car_reserved Boolean
    
);

INSERT INTO Cars ( Car_id, Car_color, Car_size_type, Car_reserved) VALUES
('AA001', 'White', 'sedan', NULL),
('AA002', 'Black', 'SUV', NULL),
('AA003', 'Green', 'Coupe', NULL),
('AA004', 'Yellow', 'SUV', NULL),
('AA005', 'White', 'Truck', NULL),
('AA006', 'White', 'Sedan', NULL),
('AA007', 'Black', 'Truck', NULL),
('AA008', 'Black', 'Sedan', NULL);

CREATE TABLE  Drivers (
    Driver_id VARCHAR(10) PRIMARY KEY,
    Driver_Name VARCHAR(50),
    Driver_License_id VARCHAR(20)
);

INSERT INTO Drivers (Driver_id, Driver_Name, Driver_License_id) VALUES
('Driver1', 'John', '10001'),
('Driver2', 'Sam', '10002'),
('Driver3', 'Noah', '10003'),
('Driver4', 'Tom', '10004'),
('Driver5', 'Ann', '10005');

CREATE TABLE Reservation (
    Reservation_id VARCHAR(45) PRIMARY KEY,
    Driver_id VARCHAR(10),
	Car_id VARCHAR(10),
    Size VARCHAR(5),
    Checkout_time DATETIME,
    Return_time DATETIME,
    Price VARCHAR(45),
    FOREIGN KEY (Driver_id) REFERENCES Drivers(Driver_id),
    FOREIGN KEY (Car_id) REFERENCES Cars(Car_id)
);

INSERT INTO Reservation (Reservation_id, Driver_id, Car_id, Size, Checkout_time, Return_time, Price) VALUES
('RES001', 'Driver1', 'AA001', 'sedan', '2024-03-15 10:00:00', '2024-03-17 10:00:00', '200.00'),
('RES002', 'Driver2', 'AA002', 'SUV', '2024-03-16 14:00:00', '2024-03-18 14:00:00', '300.00'),
('RES003', 'Driver3', 'AA005', 'Truck', '2024-03-17 09:00:00', '2024-03-19 09:00:00', '350.00');
