class Package:
    def __init__(self, package_id, address, city, zip_code, deadline, weight, notes):
        self.package_id = int(package_id)
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes

        # Required fields for Task 2
        self.status = "At Hub"
        self.delivery_time = None
        self.truck_id = None

    def __str__(self):
        return (f"Package {self.package_id} | "
                f"{self.status} | "
                f"Address: {self.address} | "
                f"Deadline: {self.deadline} | "
                f"City: {self.city} | "
                f"Zip: {self.zip_code} | "
                f"Weight: {self.weight} | "
                f"Delivered at: {self.delivery_time} | "
                f"Truck: {self.truck_id}")