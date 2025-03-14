from models.rental import Rental
from models.vehicle import Vehicle

def rent_vehicle(vehicle_id, renter_name):
    
    vehicle = Vehicle.find_by_id(vehicle_id)
    if vehicle:
        return vehicle.rent(renter_name)
    return None

def list_rented_cars():
    rentals = Rental.list_all_rentals()
    rented_cars = []
    for rental in rentals:
        rented_cars.append({
            "renter_name": rental.renter_name,
            "vehicle_id": rental.vehicle_id,
            "rental_date": rental.rental_date,
            "return_date": rental.return_date,
            "total_cost": rental.total_cost
        })
    return rented_cars

def return_vehicle(rental_id, rental_hours):
    rental = Rental.find_by_id(rental_id)
    if rental:
        return rental.return_vehicle(rental_hours)
    return None
