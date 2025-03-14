from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base, SessionLocal
from datetime import datetime

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
    def create(cls, renter_name, vehicle):
        db = SessionLocal()
        rental = cls(renter_name=renter_name, vehicle_id=vehicle.id)
        db.add(rental)
        db.commit()
        db.refresh(rental)
        db.close()
        return rental

    @classmethod
    def find_by_id(cls, rental_id):
        db = SessionLocal()
        rental = db.query(cls).filter_by(id=rental_id).first()
        db.close()
        return rental

    @classmethod
    def list_all_rentals(cls):
        db = SessionLocal()
        rentals = db.query(cls).all()
        db.close()
        return rentals

    def return_vehicle(self, rental_hours):
        from .vehicle import Vehicle  # Import here to avoid circular import
        self.return_date = datetime.utcnow()
        self.total_cost = rental_hours * 5  # Example: $5 per hour
