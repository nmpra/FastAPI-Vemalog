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
