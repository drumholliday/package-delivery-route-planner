# Kevin Drum Holliday
# Student ID 011288233
# WGUPS Routing Program

import csv

from distance import DistanceTable
from hash_table import HashTable
from package import Package, format_time
from truck import Truck

# EDITED TO FIX DELIVERY DEADLINE ISSUES
# Created constants for exact time comparisons (in decimal hours).
# Prevents floating-point errors and ensures correct handling of
# delayed packages (9:05 AM) and package #9 address update (10:20 AM).
NINE_FIVE = 9 + 5 / 60  # 9:05 AM
TEN_TWENTY = 10 + 20 / 60  # 10:20 AM


# Load package data from CSV
def load_packages(file_path, hash_table):
    # Open the CSV file and read line by line
    with open(file_path, newline="") as csvfile:
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
            package = Package(
                package_id, address, city, zip_code, deadline, weight, notes
            )
            # Insert package into hash table using package_id as key
            # This allows fast lookup later (O(1) average time)
            hash_table.insert(package_id, package)


# EDITED TO FIX DELIVERY DEADLINE ISSUES
# Helper function
# Convert delivery deadlines into numeric values for comparison during routing.
# Earlier deadlines are prioritized (e.g., 9:00 AM before 10:30 AM),
# while "EOD" is treated as infinity so it is selected last.
# These values are used by the routing algorithm to determine delivery order.
def get_deadline_value(deadline):
    if deadline == "EOD":
        return float("inf")
    elif deadline == "9:00 AM":
        return 9.0
    elif deadline == "10:30 AM":
        return 10.5
    return float("inf")


# Deliver packages using Nearest Neighbor Algorithm
def deliver_truck(truck, package_table, distance_table):
    # Continue until all packages on the truck are delivered
    while truck.packages:
        closest_package = None
        # Start with a very large distance (inf) = infinity
        closest_distance = float("inf")
        # Check all valid packages currently on the truck and iterate through remaining packages.
        for package_id in truck.packages:
            package = package_table.lookup(package_id)

            # EDITED
            # CREATE A RULE for Package #9 which is the wrong address until 10:20 AM
            # It can't be delivered before 10:20 AM
            # At 10:20 AM the address is corrected
            if package.package_id == 9:
                # This package cannot be delivered until 10:20 AM
                # EDIT TO THE CONSTANT CREATED FOR 10:20 AM
                if truck.time < TEN_TWENTY:
                    # Skip this package for now
                    continue
                else:
                    # At 10:20 AM, correct the address
                    package.address = "410 S State St"

            # EDITED TO FIX DELIVERY DEADLINE ISSUES
            # Enforce delayed package constraint: packages 6, 25, 28, and 32
            # are not available for delivery until 9:05 AM. Skip them during
            # route selection until the current truck time reaches that threshold.
            if package.package_id in [6, 25, 28, 32] and truck.time < NINE_FIVE:
                continue
            # Calculate distance from current location to package address
            distance = distance_table.get_distance(
                truck.current_location, package.address
            )

            # EDITED TO FIX THE DELIVERY DEADLINE ISSUES
            # Convert the package deadline into numeric values
            # so deadlines can be evaluated during route selection
            current_deadline = get_deadline_value(package.deadline)

            # If this is the first valid package checked, set it as the current best option
            if closest_package is None:
                closest_package = package
                closest_distance = distance
                # EDITED TO FIX DELIVERY DEADLINE ISSUES
            else:
                # Get the deadline value of the currently selected best package
                selected_deadline = get_deadline_value(closest_package.deadline)

                # PRIORITY RULE:
                # Select the package with the earlier deadline (e.g., 9:00 AM before 10:30 AM, before EOD)
                # This ensures time-sensitive deliveries are handled first
                if current_deadline < selected_deadline:
                    closest_package = package
                    closest_distance = distance

                # If both packages have the same deadline, fall back to nearest neighbor logic
                # to minimize travel distance and improve efficiency
                elif current_deadline == selected_deadline:
                    if distance < closest_distance:
                        closest_package = package
                        closest_distance = distance

        # If no valid package is available (due to delay rules), advance time slightly
        # This happens when all packages are skipped (e.g., delays or rules)
        if closest_package is None:
            truck.time += 0.01
            continue
        # Deliver package
        truck.current_location = closest_package.address
        truck.mileage += closest_distance
        truck.time += closest_distance / 18

        closest_package.status = "Delivered"
        closest_package.delivery_time = truck.time

        truck.remove_package(closest_package.package_id)


# Show the package status at different times
# EDITED 3rd Time
def check_status_at_time(check_time, package_table, truck3_start_time):
    print(f"\nSTATUS AT TIME: {format_time(check_time)}\n")

    for package in package_table.get_all():

        # Package 9 address logic
        if package.package_id == 9:
            # Before 10:20 AM → incorrect address
            if check_time < TEN_TWENTY:
                display_address = "300 State St"
                # EDITED - After 10:20 AM Package 9 should show the correct address
            else:
                display_address = "410 S State St"
        else:
            display_address = package.address

        # Status logic
        # EDITED
        # Determine package status based on the requested time.
        # Delayed packages (6, 25, 28, 32) must be handled first,
        # since they are not available until 9:05 AM and override all other states.
        if package.package_id in [6, 25, 28, 32] and check_time < NINE_FIVE:
            status = "Delayed (Flight)"

        elif check_time < 8.0 or package.truck_id is None:
            status = "At Hub"

        # Truck 3 must stay at hub until it starts
        elif package.truck_id == 3 and check_time < truck3_start_time:
            status = "At Hub"

        # EDITED
        # Adjust comparison to account for floating-point precision issues when using decimal time.
        # Ensures packages are marked as delivered at the exact intended delivery time.
        elif package.delivery_time is not None and check_time >= (
            package.delivery_time - 0.01
        ):
            status = f"Delivered at {format_time(package.delivery_time)}"

        # Otherwise still being delivered
        else:
            status = "En Route"

        # Display complete package information for the selected time
        # including package ID, address, deadline, assigned truck, and current delivery status
        print(
            f"Package {package.package_id} | "
            f"Address: {display_address} | "
            f"Deadline: {package.deadline} | "
            f"Truck: {package.truck_id} | "
            f"Status: {status}"
        )


# EDITED
# Added a helper function to convert user input time from HH:MM format into decimal format.
def convert_time_to_decimal(time_str):
    parts = time_str.strip().split(":")

    if len(parts) != 2:
        raise ValueError("Invalid time format")

    hours = int(parts[0])
    minutes = int(parts[1])

    # Convert afternoon inputs like 1:00 to 13:00
    # Normalize user input into the delivery time window.
    # Times before 8 are treated as afternoon (PM), since deliveries occur after 8:00 AM.
    if hours < 8:
        hours += 12

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

    # EDITED TO FIX DELIVERY DEADLINE ISSUES
    # Pre-assigned truck groupings to satisfy delivery constraints and ensure
    # efficient routing. These assignments represent one valid configuration
    # that meets all deadline and delivery requirements.
    # Truck 1 required packages
    truck1_required = [13, 14, 15, 16, 19, 20, 30, 31]
    # Truck 2 required packages
    truck2_required = [3, 18, 36, 38, 34, 37]

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
