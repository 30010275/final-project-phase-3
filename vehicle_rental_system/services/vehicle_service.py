from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.vehicle import Vehicle
from models.rental import Rental

def list_vehicles():  
    # Function to list all available vehicles
    db = SessionLocal()
    vehicles = db.query(Vehicle).all()
    db.close()
    
    vehicle_list = []
    for vehicle in vehicles:
        # Check if the vehicle is currently rented
        rental_status = "Available" if vehicle.available else "Not Available (Rented)"
        vehicle_list.append(f"{vehicle.id}: {vehicle.brand} ({vehicle.type}) - {rental_status}")
    
    return vehicle_list
def add_vehicle(type, brand):
    db = SessionLocal()
    vehicle = Vehicle.create(type=type, brand=brand)
    db.close()
    return vehicle
