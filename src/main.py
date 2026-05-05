# Kevin Drum Holliday
# Student ID 011288233
# WGUPS Routing Program

import csv

from distance import DistanceTable
from hash_table import HashTable
from package import Package, format_time
from truck import Truck


# Load package data from CSV
def load_packages(file_path, hash_table):
    # Open the CSV file and read line by line
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            # Skip empty rows or header rows (non-numeric IDs)
            if not row or not row[0].isdigit():
                continue
            # Extract each field from the CSV row
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            zip_code = row[4]
            deadline = row[5]
            weight = row[6]
            notes = row[7]

            # Create a Package object using extracted data
            package = Package(package_id, address, city, zip_code, deadline, weight, notes)
            # Insert package into hash table using package_id as key
            # This allows fast lookup later (O(1) average time)
            hash_table.insert(package_id, package)


# Deliver packages using Nearest Neighbor Algorithm
def deliver_truck(truck, package_table, distance_table):
    # Continue until all packages on the truck are delivered
    while truck.packages:
        closest_package = None
        # Start with a very large distance (inf) = infinity
        closest_distance = float('inf')
        # Check all valid packages currently on the truck and iterate through remaining packages.
        for package_id in truck.packages:
            package = package_table.lookup(package_id)

            # EDITED
            # CREATE A RULE for Package #9 which is the wrong address until 10:20 AM
            # It can't be delivered before 10:20 AM
            # At 10:20 AM (10.33 decimal), the address is corrected
            if package.package_id == 9:
                # This package cannot be delivered until 10:20 AM
                if truck.time < 10.33:
                    # Skip this package for now
                    continue
                else:
                    # At 10:20 AM, correct the address
                    package.address = "410 S State St"

            # EDITED
            # CREATE A RULE for Delayed packages (6, 25, 28, 32)
            # These packages aren't available until 9:05 AM
            # The truck skips these packages until then
            if "Delayed" in package.notes:
                # Skip until package arrives at hub
                if truck.time < 9.05:
                    continue

            # Calculate distance from current location to package address
            distance = distance_table.get_distance(
                truck.current_location,
                package.address
            )
            # Keep track of the closest package
            if distance < closest_distance:
                closest_distance = distance
                closest_package = package

        # If no valid package is available (due to delay rules), advance time slightly
        # This happens when all packages are skipped (e.g., delays or rules)
        if closest_package is None:
            truck.time += 0.01
            continue

        # Update location by moving truck to the closest package location
        truck.current_location = closest_package.address
        # Update mileage by adding distance traveled to total mileage
        truck.mileage += closest_distance
        # Update time based on distance (using speed = 18 mph)
        # time = distance / speed
        truck.time += closest_distance / 18

        # Mark package as delivered
        closest_package.status = "Delivered"
        closest_package.delivery_time = truck.time

        # Remove package from the truck
        truck.remove_package(closest_package.package_id)

    # FINAL PASS Cleaned Up To Guarantee Nothing Is Left Behind
    for package_id in list(truck.packages):
        package = package_table.lookup(package_id)

        distance = distance_table.get_distance(
            truck.current_location,
            package.address
        )

        truck.current_location = package.address
        truck.mileage += distance
        truck.time += distance / 18

        package.status = "Delivered"
        package.delivery_time = truck.time

        truck.remove_package(package.package_id)
        # End While Loop


# Show the package status at different times
# EDITED
def check_status_at_time(check_time, package_table, truck3_start_time):
    # Display the time being checked (in decimal format)
    print(f"\nSTATUS AT TIME: {check_time:.2f}\n")

    # Loop through all packages stored in the hash table
    for package in package_table.get_all():

        # Delayed packages (not at hub until 9:05 AM)
        if "Delayed" in package.notes and check_time < 9.05:
            status = "Delayed (Flight)"

        # Before deliveries begin
        elif check_time < 8.0 or package.truck_id is None:
            status = "At Hub"

        # If package has not been delivered yet OR delivery time is in the future
        # If it hasn’t been delivered yet, it must still be in transit so "is None" must mean En Route
        elif package.delivery_time is None or check_time < package.delivery_time:
            # EDITED TRUCK 3 should not be En Route Before it Starts
            # Status = "En Route"
            if package.truck_id == 3 and check_time < truck3_start_time:
                status = "At Hub"
            else:
                status = "En Route"
        # If package has already been delivered
        else:
            status = f"Delivered at {format_time(package.delivery_time)}"
        # Print package ID, address, status, deadline, and truck_id
        print(
            f"Package {package.package_id} | "
            f"{package.address} | "
            f"{status} | "
            f"{package.deadline} | "
            f"Truck {package.truck_id}"
        )


# EDITED
# Added a helper function to convert user input time from HH:MM format into decimal format.
# Splits the input string into hours and minutes, validates correct format,
# Converts the values into a single decimal number for time-based comparisons (e.g., 09:30 → 9.5).
def convert_time_to_decimal(time_str):
    parts = time_str.split(":")
    if len(parts) != 2:
        raise ValueError("Invalid time format")

    hours = int(parts[0])
    minutes = int(parts[1])

    return hours + minutes / 60


# Main program execution
def main():
    # Create hash table to store all packages
    package_table = HashTable()

    # Load package data from CSV into hash table
    load_packages("../data/WGUPS Package File Final Edit2.csv", package_table)

    # Create Trucks with assigned packages and set time to 8am in decimal time
    truck1 = Truck(1, 8.0)
    truck2 = Truck(2, 8.0)
    truck3 = Truck(3, 8.0)

    # Get all packages from hash table
    all_packages = package_table.get_all()

    # EDITED
    # Required Delivery Constraints
    # These packages must be on specific trucks per assignment rules

    # Truck 1 required packages must be delivered together
    truck1_required = [13, 14, 15, 16, 19, 20]

    # Truck 2 required packages
    truck2_required = [3, 18, 36, 38]

    # EDITED
    # STEP 1 - Load required packages onto truck 1 first
    # This guarantees constraint satisfaction before loading other packages.
    for package in all_packages:
        if package.package_id in truck1_required:
            truck1.load_package(package.package_id)
            package.truck_id = 1
    # EDITED
    # STEP 2 - Load required packages onto truck 2
    # These need to be assigned before loading
    for package in all_packages:
        if package.package_id in truck2_required:
            truck2.load_package(package.package_id)
            package.truck_id = 2

    # EDITED
    # STEP 3 - Load all remaining packages
    # Packages not already assigned are put on trucks
    # Based on available capacity (Max 16 per truck)
    for package in all_packages:
        if package.truck_id is None:
            if truck1.load_package(package.package_id):
                package.truck_id = 1
            elif truck2.load_package(package.package_id):
                package.truck_id = 2
            else:
                truck3.load_package(package.package_id)
                package.truck_id = 3

        # EDITED
        # Set initial status after they are assigned
        package.status = "En Route"

    # Load the Distance Table used for route calculation
    # This provides distances between all delivery locations
    distance_table = DistanceTable()
    distance_table.load_data("../data/WGUPS Distance Table CLEAN 2.csv")

    # Deliver first two trucks (2 drivers available)
    deliver_truck(truck1, package_table, distance_table)
    deliver_truck(truck2, package_table, distance_table)

    # EDITED
    # Driver Constraint (Only 2 drivers are available)
    # Truck 1 and 2 leave at 8:00 AM
    # Set Truck 3 start time when one driver becomes available
    # Ensures only two trucks are delivering at a time
    truck3.time = min(truck1.time, truck2.time)

    # EDITED
    # Record Truck 3 start time after constraint is applied
    truck3_start_time = truck3.time

    # EDITED Now truck 3 begins deliveries
    deliver_truck(truck3, package_table, distance_table)

    # EDITED
    # Added print before the UI Loop
    # Print mileage BEFORE UI loop
    print("\nTOTAL MILEAGE:")
    print(f"Truck 1: {truck1.mileage:.2f}")
    print(f"Truck 2: {truck2.mileage:.2f}")
    print(f"Truck 3: {truck3.mileage:.2f}")
    print(f"Total: {(truck1.mileage + truck2.mileage + truck3.mileage):.2f}")

    # EDITED
    # Created an interactive UI loop
    # Prompts the user to enter a time in HH:MM format to check package delivery status
    # Converts the input to decimal time for internal processing
    # Validates that the time is within delivery hours (after 8:00 AM).
    # Calls the status function to display all package information at the requested time.
    # Allows the user to exit the program by typing 'exit'.
    # Handles invalid input formats to prevent runtime errors.
    while True:
        try:
            time_input = input("\nEnter time (HH:MM, e.g., 09:00) or 'exit': ")

            if time_input.lower() == "exit":
                print("Exiting program...")
                break

            user_time = convert_time_to_decimal(time_input)

            if user_time < 8.0:
                print("Time must be 08:00 or later (deliveries start at 8:00 AM)")
                continue

            check_status_at_time(user_time, package_table, truck3_start_time)

        except ValueError:
            print("Invalid format. Please use HH:MM (e.g., 09:00)")


# Run the program
if __name__ == "__main__":
    main()
