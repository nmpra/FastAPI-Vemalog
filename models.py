from database import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

class Vehicle(Base):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15))
    cc: Mapped[int] = mapped_column(Integer) 
    license_plate: Mapped[str] = mapped_column(String(10))
    vehicle_type: Mapped[str] = mapped_column(String(20))
    transmission: Mapped[str] = mapped_column(String(20))
    current_mileage: Mapped[int] = mapped_column(Integer, default=0)
    last_oil_change: Mapped[int] = mapped_column(Integer, default=0)
    last_maintenance: Mapped[int] = mapped_column(Integer, default=0)

    @property
    def oil_change_interval(self):
        return 2000 if self.vehicle_type == "Motorcycle" else 5000
    
    @property
    def maintenance_interval(self):
        return 5000 if self.vehicle_type == "Motorcycle" else 10000
    
    def update_mileage(self, new_mileage: int):
        if new_mileage <= self.current_mileage:
            raise ValueError("Mileage baru gak boleh lebih kecil/sama, Nat!")
        self.current_mileage = new_mileage

    @property
    def remaining_oil(self) -> int:
        used = self.current_mileage - self.last_oil_change
        return max(0, self.oil_change_interval - used)

    @property
    def remaining_maint(self) -> int:
        used = self.current_mileage - self.last_maintenance
        return max(0, self.maintenance_interval - used)
    
class Motorcycle(Vehicle):
    pass

class Car(Vehicle):
    pass