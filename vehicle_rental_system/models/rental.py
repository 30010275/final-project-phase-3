from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, joinedload
from .database import Base, SessionLocal
from datetime import datetime, timedelta  # Added timedelta import
from .vehicle import Vehicle  # Import Vehicle model

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    renter_name = Column(String)
    rental_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    total_cost = Column(Integer, nullable=True)

    vehicle = relationship("Vehicle")

    @classmethod
    def create(cls, renter_name, vehicle, total_cost):
        db = SessionLocal()
        rental = cls(renter_name=renter_name, vehicle_id=vehicle.id, total_cost=total_cost)  # Set total_cost
        db.add(rental)
        db.commit()
        db.refresh(rental)
        db.close()
        return rental

    @classmethod
    def find_by_id(cls, rental_id):
        db = SessionLocal()
        rental = db.query(cls).options(joinedload(Rental.vehicle)).filter_by(id=rental_id).first()  # Eager load vehicle
        db.close()
        return rental

    @classmethod
    def list_all_rentals(cls):
        db = SessionLocal()
        rentals = db.query(cls).options(joinedload(Rental.vehicle)).all()  # Eager load vehicle
        db.close()
        return rentals

    def return_vehicle(self, rental_hours):
        self.return_date = datetime.utcnow()
        self.total_cost = rental_hours * 500  # Assuming a rate of 500 ksh per hour
        if self.return_date > self.rental_date + timedelta(hours=rental_hours):
            late_hours = (self.return_date - (self.rental_date + timedelta(hours=rental_hours))).total_seconds() / 3600
            late_fee = late_hours * 5  # Assuming a fixed late fee rate
            self.total_cost += late_fee  # Add late fee to total cost
        
        # Update vehicle availability
        vehicle = Vehicle.find_by_id(self.vehicle_id)  # Load vehicle explicitly
        if vehicle:
            vehicle.available = True  # Mark vehicle as available
            db = SessionLocal()
            db.add(vehicle)  # Update vehicle status in the database
            db.commit()
            db.close()
        
        return self.total_cost  # Return total cost
