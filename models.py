# Models


class Vehicle:
    def __init__(self, id, name, cc, license_plate, vehicle_type):
        self.id = id
        self.name = name
        self.cc = cc
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
    
    def get_info(self):
        return f"{self.name} {self.cc}cc | {self.license_plate}"


class Motorcycle(Vehicle):
    def __init__(self, id, name, cc, license_plate, transmission):
        super().__init__(id, name, cc, license_plate, vehicle_type="Motorcycle")
        self.transmission = transmission
        self._mileage = 0
        self._last_oil_mileage = 0
        self._oil_change_interval = 2000
        self._last_maintenance_mileage = 0
        self._maintenance_interval = 5000


class Car(Vehicle):
    def __init__(self, id, name, cc, license_plate, transmission):
        super().__init__(id, name, cc, license_plate, vehicle_type="Car")
        self.transmission = transmission
        self._mileage = 0
        self._last_oil_mileage = 0
        self._oil_change_interval = 5000
        self._last_maintenance_mileage = 0
        self._maintenance_interval = 10000



