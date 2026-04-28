class Truck:
    def __init__(self, truck_id, start_time):
        self.truck_id = truck_id
        self.packages = []              # list of package IDs
        self.mileage = 0.0
        self.current_location = "4001 South 700 East"
        self.time = start_time

    # Load package if capacity allows
    def load_package(self, package_id):
        # Max of 16 packages allowed on a truck
        if len(self.packages) < 16:
            self.packages.append(package_id)
            return True
        else:
            return False
    # Remove a package from the truck after it's delivered and keep track of remaining deliveries.
    def remove_package(self, package_id):
        if package_id in self.packages:
            self.packages.remove(package_id)