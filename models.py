# Import biar gaperlu make quotes di relationship dan biar python ga protes nyari referensinya
from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))

    # Relationship One to Many ke Vehicle karena make list
    vehicles: Mapped[list[Vehicle]] = relationship(back_populates="user")
    # Buat password hash
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)

    # FK buat nyambungin ke tabel user sebagai child table
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Relationship Many to One ke User dan ga make list karena satu kendaraan hanya boleh punya satu owner
    user: Mapped[User] = relationship(back_populates="vehicles")

    brand: Mapped[str] = mapped_column(String(15))
    model: Mapped[str] = mapped_column(String(15))
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

    @property
    def remaining_oil(self) -> int:
        used = self.current_mileage - self.last_oil_change
        return max(0, self.oil_change_interval - used)

    @property
    def remaining_maint(self) -> int:
        used = self.current_mileage - self.last_maintenance
        return max(0, self.maintenance_interval - used)
