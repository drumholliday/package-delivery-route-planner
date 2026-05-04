# Kevin Drum Holliday
# ID 011288233

import csv
from hash_table import HashTable
from package import Package, format_time
from distance import DistanceTable
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

            # CREATE A RULE for Package #9 which is the wrong address
            if package.package_id == 9:
                # This package cannot be delivered until 10:20 AM
                if truck.time < 10.33:
                    # Skip this package for now
                    continue
                else:
                    # At 10:20 AM, correct the address
                    package.address = "410 S State St"

            # CREATE A RULE for Delayed packages
            # Some packages are not available until 9:05 AM
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

        # EDGE CASE: No valid package foundIf no valid package was found (all skipped), advance time and retry
        # This happens when all packages are skipped (e.g., delays or rules)
        # if closest_package is None:
        #     # Move time forward slightly and try again
        #     truck.time += 0.01
        #     continue
        if closest_package is None:
            truck.time += 0.01
            continue
        # Update location by moving truck to the closest package location
        truck.current_location = closest_package.address
        # Update mileage ny adding distance traveled to total mileage
        truck.mileage += closest_distance
        # Update time based on distance (using speed = 18 mph)
        # time = distance / speed
        truck.time += closest_distance / 18

        # Mark package as delivered
        closest_package.status = "Delivered"
        closest_package.delivery_time = truck.time

        # Remove package from the truck
        truck.remove_package(closest_package.package_id)

    # FINAL PASS CLEANED UP TO GUARANTEE NOTHING LEFT BEHIND
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
        # END OF WHILE LOOP

# Show the package status at different times
def check_status_at_time(check_time, package_table):
    # Display the time being checked (in decimal format)
    print(f"\nSTATUS AT TIME: {check_time:.2f}\n")

    # Loop through all packages stored in the hash table
    for package in package_table.get_all():

        # Determine package status based on time

        # # Before deliveries begin (before 8:00 AM)
        # if check_time < 8.0 or package.truck_id is None:
        #     status = "At Hub"

        # Delayed packages (not at hub until 9:05 AM)
        if "Delayed" in package.notes and check_time < 9.05:
            status = "Delayed (Flight)"

        # Before deliveries begin
        elif check_time < 8.0 or package.truck_id is None:
            status = "At Hub"

        # If package has not been delivered yet OR delivery time is in the future
        # If it hasn’t been delivered yet, it must still be in transit so "is None" must mean En Route
        elif package.delivery_time is None or check_time < package.delivery_time:
            status = "En Route"
        # If package has already been delivered
        else:
            status = f"Delivered at {format_time(package.delivery_time)}"
        # Print package ID, status, and assigned truck
        print(f"Package {package.package_id} | {status} | Truck {package.truck_id}")

# Main program execution
def main():

    # Create hash table to store all packages
    package_table = HashTable()

    # Load package data from CSV into hash table
    load_packages("../data/WGUPS Package File Final Edit2.csv", package_table)

    # Create Trucks with assigned packages and set time to 8am in decimal time
    truck1 = Truck(1, 8.0)
    truck2 = Truck(2, 8.0)
    # CHANGE TIME TO 10.2 (10:12) so TRUCKS 1 and 2 RUN FIRST, ONE DRIVER RETURNS THEN 3 STARTS
    truck3 = Truck(3, 10.2)

    # Get all packages from hash table
    all_packages = package_table.get_all()

    # Load packages onto trucks
    # If truck one is full (max 16) then put on truck 2 etc.
    # Packages are assigned sequentially
    # for package in all_packages:
    #     if truck1.load_package(package.package_id):
    #         # Update the status of the truck assignment
    #         package.status = "En Route"
    #         # Assign the truck number
    #         package.truck_id = 1
    #         continue
    #     elif truck2.load_package(package.package_id):
    #         package.status = "En Route"
    #         package.truck_id = 2
    #         continue
    #     elif truck3.load_package(package.package_id):
    #         package.status = "En Route"
    #         package.truck_id = 3
    #         continue

    # Required package assignments based on constraints
    truck1_required = [13, 14, 15, 16, 19, 20]
    truck2_required = [3, 18, 36, 38]

    for package in all_packages:

        if package.package_id in truck1_required:
            if truck1.load_package(package.package_id):
                package.truck_id = 1
            else:
                truck3.load_package(package.package_id)
                package.truck_id = 3

        elif package.package_id in truck2_required:
            if truck2.load_package(package.package_id):
                package.truck_id = 2
            else:
                truck3.load_package(package.package_id)
                package.truck_id = 3
        else:
            if truck1.load_package(package.package_id):
                package.truck_id = 1
            elif truck2.load_package(package.package_id):
                package.truck_id = 2
            else:
                truck3.load_package(package.package_id)
                package.truck_id = 3

        # Set initial status
        package.status = "En Route"

    # DEBUGGING
    # Print Truck Contents
    print("\nTRUCK 1 PACKAGES:", truck1.packages)
    print("TRUCK 2 PACKAGES:", truck2.packages)
    print("TRUCK 3 PACKAGES:", truck3.packages)

    # TEST 1: Print all Packages
    for package in package_table.get_all():
        print(package)

    # TEST 2: Test the Hash Table Lookup
    print("\nTEST LOOKUP:")
    print(package_table.lookup(1))

    # TEST 3:  Load the Distance Table
    distance_table = DistanceTable()
    distance_table.load_data("../data/WGUPS Distance Table CLEAN 2.csv")

    # # Loop through each truck to deliver packages
    # deliver_truck(truck1, package_table, distance_table)
    # deliver_truck(truck2, package_table, distance_table)
    # deliver_truck(truck3, package_table, distance_table)

    # Deliver first two trucks (2 drivers available)
    deliver_truck(truck1, package_table, distance_table)
    deliver_truck(truck2, package_table, distance_table)

    # Truck 3 starts after one driver becomes available
    truck3.time = min(truck1.time, truck2.time)
    deliver_truck(truck3, package_table, distance_table)

    # STATUS CHECKS
    # D1 (between 8:35–9:25)
    check_status_at_time(9.0, package_table)

    # D2 (between 9:35–10:25)
    check_status_at_time(10.0, package_table)

    # D3 (between 12:03–1:12)
    check_status_at_time(12.5, package_table)

    # Test the distance loop
    print("\nTEST DISTANCE:")
    print(distance_table.get_distance("4001 South 700 East", "195 W Oakland Ave"))

    #Final Output Delivery Results
    print("\nFINAL DELIVERY STATUS:")

    for package in package_table.get_all():
        print(package)

    # Print mileage with rounded decimal
    print("\nTOTAL MILEAGE:")
    print(f"Truck 1: {truck1.mileage:.2f}")
    print(f"Truck 2: {truck2.mileage:.2f}")
    print(f"Truck 3: {truck3.mileage:.2f}")
    # Return total truck mileage
    print(f"Total: {(truck1.mileage + truck2.mileage + truck3.mileage):.2f}")

# Run the program
if __name__ == "__main__":
    main()