# Models


class Vehicle:
    def __init__(self, id, name, cc, license_plate, vehicle_type):
        self.id = id
        self.name = name
        self.cc = cc
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self._mileage = 0
        self._last_oil_mileage = 0
        self._oil_change_interval = 0
        self._last_maintenance_mileage = 0
        self._maintenance_interval = 0
    
    def get_info(self):
        return f"{self.name} {self.cc}cc | {self.license_plate}"
    
    def mileage_update(self, new_mileage):
        self._prev_mileage = self._mileage
        if new_mileage < self._mileage:
            raise ValueError("The new mileage cannot be less than the old mileage!")
        self._mileage = new_mileage
        return self

    def oil_update(self):
        self._last_oil_mileage = self._mileage
        return self._last_oil_mileage

    def oil_status(self):
        if (
            self._mileage - self._last_oil_mileage
        ) >= self._oil_change_interval:
            return False, None
        else:
            remaining_mileage = self._oil_change_interval - (
                self._mileage - self._last_oil_mileage
            )
            return True, remaining_mileage

    def maintenance_update(self):
        self._last_maintenance_mileage = self._mileage
        return self._last_maintenance_mileage

    def maintenance_status(self):
        if (
            self._mileage - self._last_maintenance_mileage
        ) >= self._maintenance_interval:
            return False, None
        else:
            remaining_mileage = self._maintenance_interval - (
                self._mileage - self._last_maintenance_mileage
            )
            return True, remaining_mileage



class Motorcycle(Vehicle):
    def __init__(self, id, name, cc, license_plate, transmission):
        super().__init__(id, name, cc, license_plate, vehicle_type="Motorcycle")
        self.transmission = transmission
        self._oil_change_interval = 2000
        self._maintenance_interval = 5000


class Car(Vehicle):
    def __init__(self, id, name, cc, license_plate, transmission):
        super().__init__(id, name, cc, license_plate, vehicle_type="Car")
        self.transmission = transmission
        self._oil_change_interval = 5000
        self._maintenance_interval = 10000



