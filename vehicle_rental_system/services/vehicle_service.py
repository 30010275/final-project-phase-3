from models.vehicle import Vehicle

def add_vehicle(type, brand):
    vehicle = Vehicle.create(type, brand)
    return vehicle

def list_vehicles():
    return Vehicle.list_all()

def delete_vehicle(vehicle_id):
    # Logic to delete a vehicle by ID
    pass
