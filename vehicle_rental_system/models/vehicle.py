from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from .database import Base, SessionLocal
from .rental import Rental  # Import Rental

class Vehicle(Base):
    __tablename__ = "vehicles"


    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    available = Column(Boolean, default=True)


    @classmethod
    def create(cls, type, brand):
        db = SessionLocal()
        vehicle = cls(type=type, brand=brand)
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        db.close()
        return vehicle

    @classmethod
    def list_all(cls):
        db = SessionLocal()
        vehicles = db.query(cls).filter_by(available=True).all()
        db.close()
        return vehicles

    @classmethod
    def find_by_id(cls, vehicle_id):
        db = SessionLocal()
        vehicle = db.query(cls).filter_by(id=vehicle_id).first()
        db.close()
        return vehicle

    def rent(self, renter_name):
        db = SessionLocal()  # Define db session here
        if not self.available:
            print("❌ Vehicle is already rented.")
            db.close()  # Ensure to close the session
            return None

        self.available = False
        rental = Rental.create(renter_name, self)  # Now Rental is defined
        db.commit()
        db.close()
        return rental

    def return_vehicle(self, rental_id, rental_hours):
        db = SessionLocal()
        rental = db.query(Rental).filter_by(id=rental_id, return_date=None).first()
        if not rental:
            print("❌ Rental record not found.")
            db.close()
            return None
        
        rental.return_vehicle(rental_hours)
        self.available = True
        db.commit()
        db.close()
        return rental.total_cost
