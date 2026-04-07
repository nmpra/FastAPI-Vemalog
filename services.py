# Service

class GarageServices:
    
    def __init__(self):
        self.gid = 1
        self._vehicles = {}
        self.capacity = 5

    def find_vehicle(self, id):
        return self._vehicles.get(id)

    def get_all_veh(self):
        if not self._vehicles:
            raise ValueError("You don't have any vehicles in your garage.")
        return list(self._vehicles.values())

    def add_vehicle(self, new_vehicle):
        if len(self._vehicles) >= self.capacity:
            raise RuntimeError("You don't have any more slots in the garage.")
        new_vehicle.id = self.gid
        self._vehicles[new_vehicle.id] = new_vehicle
        self.gid += 1
        return new_vehicle

    def remove_vehicle(self, id):
        if id not in self._vehicles:
            raise KeyError(f"Vehicle with ID {id} could not be found.")
        del self._vehicles[id]


class MaintenanceLogic:

    def mileage_update(vehicle, new_mileage):
        vehicle._prev_mileage = vehicle._mileage
        if new_mileage < vehicle._mileage:
            raise ValueError("The new mileage cannot be less than the old mileage!")
        vehicle._mileage = new_mileage
        return vehicle._prev_mileage, vehicle._mileage

    def oil_update(vehicle):
        vehicle._last_oil_mileage = vehicle._mileage
        return vehicle._last_oil_mileage

    def oil_status(vehicle):
        if (
            vehicle._mileage - vehicle._last_oil_mileage
        ) >= vehicle._oil_change_interval:
            return False, None
        else:
            remaining_mileage = vehicle._oil_change_interval - (
                vehicle._mileage - vehicle._last_oil_mileage
            )
            return True, remaining_mileage

    def maintenance_update(vehicle):
        vehicle._last_maintenance_mileage = vehicle._mileage
        return vehicle._last_maintenance_mileage

    def maintenance_status(vehicle):
        if (
            vehicle._mileage - vehicle._last_maintenance_mileage
        ) >= vehicle.maintenance_interval:
            return False, None
        else:
            remaining_mileage = vehicle.maintenance_interval - (
                vehicle._mileage - vehicle._last_maintenance_mileage
            )
            return True, remaining_mileage
