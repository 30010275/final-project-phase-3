from models.database import Base, engine
from models.vehicle import Vehicle
from models.rental import Rental
from colorama import Fore, Style, init

init(autoreset=True)


#  database tables
Base.metadata.create_all(engine)

def add_vehicle():

    type = input("Enter vehicle type (Car/Bike/Truck): ").strip()
    brand = input("Enter vehicle brand: ").strip()
    
    vehicle = Vehicle.create(type, brand)
    if vehicle:
        print(f"{Fore.GREEN}✅ Added {vehicle.brand} ({vehicle.type}){Style.RESET_ALL}")

def list_vehicles():
    vehicles = Vehicle.list_all()
    if vehicles:
        print("\n🚗 Available Vehicles 🚗")
        for v in vehicles:
            print(f"{v.id}: {v.brand} ({v.type})")
    else:
        print("❌ No vehicles available.")

def rent_vehicle():
    
    list_vehicles()
    vehicle_id = input("Enter vehicle ID to rent: ").strip()
    
    vehicle = Vehicle.find_by_id(vehicle_id)
    if not vehicle:
        print(f"{Fore.RED}❌ Vehicle not found.{Style.RESET_ALL}")
        return

    renter_name = input("Enter your name: ").strip()
    rental = vehicle.rent(renter_name)
    
    if rental:
        print(f"{Fore.GREEN}✅ {renter_name} rented {vehicle.brand} ({vehicle.type}){Style.RESET_ALL}")

def return_vehicle():
    rental_id = input("Enter rental ID to return: ").strip()
    rental_hours = input("Enter rental duration (hours): ").strip()

    rental = Rental.find_by_id(rental_id)
    if not rental:
        print("❌ Rental record not found.")
        return

    cost = rental.return_vehicle(rental_hours)
    if cost is not None:
        print(f"{Fore.GREEN}✅ Vehicle returned. Total Cost: ${cost}{Style.RESET_ALL}")

def main():
    while True:
        print("\n🚗 Vehicle Rental System 🚗")
        print("1. Add Vehicle")
        print("2. List Vehicles")
        print("3. Rent Vehicle")
        print("4. Return Vehicle")
        print("5. Exit")
        
        choice = input("Select an option: ")
        if choice == "1":
            add_vehicle()
        elif choice == "2":
            list_vehicles()
        elif choice == "3":
            rent_vehicle()
        elif choice == "4":
            return_vehicle()
        elif choice == "5":
            print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
