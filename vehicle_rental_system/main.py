from models.database import Base, engine, SessionLocal  # Import SessionLocal
from models.vehicle import Vehicle
from models.rental import Rental
from services.vehicle_service import add_vehicle  # Import the add_vehicle function
from colorama import Fore, Style, init
from sqlalchemy.orm import joinedload  # Import joinedload
from services.rental_service import rent_vehicle  # Import the rent_vehicle function

init(autoreset=True)

# database tables
Base.metadata.create_all(bind=engine)

def list_rented_vehicles():
    rented_vehicles = Rental.list_all_rentals()  # Ensure to load vehicles eagerly
    if rented_vehicles:
        print("\n🚗 Rented Vehicles 📋")
        for rental in rented_vehicles:
            vehicle = Vehicle.find_by_id(rental.vehicle_id)  # Load vehicle explicitly
            if not vehicle:
                print("❌ Rental record not found.")
                return
            print(f"{rental.id}: {vehicle.brand} ({vehicle.type}) - Rented by {rental.renter_name} on {rental.rental_date}")


    else:
        print("✅ No vehicles are currently rented.")

def list_vehicles():
    available_vehicles = Vehicle.list_all()
    if available_vehicles:
        print("\n🚗 Available Vehicles 📋")
        for vehicle in available_vehicles:
            print(f"{vehicle.id}: {vehicle.brand} ({vehicle.type}) - Available: {vehicle.available}")
    else:
        print("✅ No vehicles are currently available.")

def handle_rent_vehicle():
    vehicle_id = input("Enter the vehicle ID to rent: ")
    try:
        vehicle_id = int(vehicle_id)  # Convert to integer
    except ValueError:
        print("❌ Invalid vehicle ID. Please enter a valid number.")
        return
    renter_name = input("Enter your name: ")
    is_vip = input("Are you a VIP customer? (yes/no): ").strip().lower() == 'yes'
    
    rental = rent_vehicle(vehicle_id, renter_name, is_vip)  #
    if rental is None:
        print("❌ Rental failed. Please check the vehicle ID and availability.")
        return
    rental.vehicle = Vehicle.find_by_id(rental.vehicle_id)  # Load vehicle explicitly
    if rental:
        print(f"✅ Successfully rented {rental.vehicle.brand} ({rental.vehicle.type}) to {renter_name}.")
    else:
        print("❌ Rental failed. Please check the vehicle ID and availability.")

def return_vehicle():
    rental_id = input("Enter the rental ID to return: ")
    try:
        rental_id = int(rental_id)  # Convert to integer
    except ValueError:
        print("❌ Invalid rental ID. Please enter a valid number.")
        return
    except ValueError:
        print("❌ Invalid rental ID. Please enter a valid number.")
        return
    rental_hours = input("Enter the number of hours the vehicle was rented: ")
    try:
        rental_hours = int(rental_hours)  # Convert to integer
    except ValueError:
        print("❌ Invalid number of hours. Please enter a valid number.")
        return
    
    db = SessionLocal()  # Create a new session
    rental = db.query(Rental).options(joinedload(Rental.vehicle)).filter_by(id=rental_id).first()  # Eager load vehicle
    if rental:
        total_cost = rental.return_vehicle(rental_hours)  # Call return_vehicle on rental
        vehicle = Vehicle.find_by_id(rental.vehicle_id)  # Load vehicle explicitly
        print(f"✅ Successfully returned {vehicle.brand} ({vehicle.type}). Total cost: ${total_cost}.")
    else:
        print("❌ Rental record not found.")
    db.close()

def main():
    while True:
        print(Fore.BLUE + "Welcome to inno_lyrico Vehicle Rental System!" + Style.RESET_ALL)
        
        print("1. Add Vehicle")
        print("2. List Vehicles")
        print("3. Rent Vehicle")
        print("4. Return Vehicle")
        print("5. List Rented Vehicles")  
        print("00. Exit")

        choice = input("Select an option: ")
        if choice == "1":
            vehicle_type = input("Enter the vehicle type. e.g. 'Car', 'Motorcycle', 'Truck': ")
            vehicle_brand = input("Enter the vehicle brand: ")
            vehicle_year_of_manufacturer = input("Enter the vehicle year of manufacturer: ")
            vehicle_color = input("Enter the vehicle color: ")
            if add_vehicle(vehicle_type, vehicle_brand):
                print("✅ Vehicle added successfully.")
        elif choice == "2":
            list_vehicles()  # Call the new function
        elif choice == "3":
            handle_rent_vehicle()  # Call the handle_rent_vehicle function
        elif choice == "4":
            return_vehicle()  # Call the return_vehicle function
        elif choice == "5":
            list_rented_vehicles()  # Call function
        elif choice == "00":
            print("👋 Goodbye Welcome Back Again!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
