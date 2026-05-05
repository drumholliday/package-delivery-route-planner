# Helper function to format time correctly since it is in decimal time.
def format_time(decimal_time):
    total_minutes = int(decimal_time * 60 + 0.5)

    hours = total_minutes // 60
    minutes = total_minutes % 60

    suffix = "AM" if hours < 12 else "PM"

    display_hour = hours % 12
    if display_hour == 0:
        display_hour = 12

    return f"{display_hour}:{minutes:02d} {suffix}"


# This method defines how a Package object is displayed when printed
def __str__(self):
    # Return a formatted string showing all important package details
    return (
        # Display package ID and current delivery status (At Hub, En Route, Delivered)
        f"Package {self.package_id} | {self.status} | "
        # Display delivery address and deadline
        f"Address: {self.address} | Deadline: {self.deadline} | "
        # Display city and zip code for location reference
        f"City: {self.city} | Zip: {self.zip_code} | "
        # Display package weight
        f"Weight: {self.weight} | "
        # Display delivery time (formatted if delivered, otherwise None)
        f"{format_time(self.delivery_time) if self.delivery_time is not None else 'Not Delivered'}"
        # Display which truck handled the delivery
        f"Truck: {self.truck_id}"
    )


# Package class represents each delivery item in the system
class Package:
    # Constructor initializes all package attributes from the CSV file
    def __init__(self, package_id, address, city, zip_code, deadline, weight, notes):
        # Unique identifier for each package (used as key in hash table)
        self.package_id = int(package_id)
        # Delivery address information
        self.address = address
        self.city = city
        self.zip_code = zip_code
        # Delivery deadline (e.g., "10:30 AM" or "EOD")
        self.deadline = deadline
        # Package weight
        self.weight = weight
        # Special notes (constraints like delayed, truck restrictions, etc.)
        self.notes = notes

        # Required fields for Task 2

        # Current delivery status (starts at hub, then changes during simulation)
        self.status = "At Hub"
        # Time the package was delivered (None until delivery occurs)
        self.delivery_time = None
        # ID of the truck assigned to deliver this package
        self.truck_id = None

    # Defines how the package object is printed (used in output and screenshots)
    def __str__(self):
        return (
            f"Package {self.package_id} | "
            f"{self.status} | "
            f"Address: {self.address} | "
            f"Deadline: {self.deadline} | "
            f"City: {self.city} | "
            f"Zip: {self.zip_code} | "
            f"Weight: {self.weight} | "
            f"Delivered at: {format_time(self.delivery_time) if self.delivery_time else None} | "
            f"Truck: {self.truck_id}"
        )
