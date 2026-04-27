import csv
from hash_table import HashTable
from package import Package
from distance import DistanceTable

def load_packages(file_path, hash_table):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if not row or not row[0].isdigit():
                continue

            package_id = int(row[0])
            address = row[1]
            city = row[2]
            zip_code = row[4]
            deadline = row[5]
            weight = row[6]
            notes = row[7]

            package = Package(package_id, address, city, zip_code, deadline, weight, notes)

            hash_table.insert(package_id, package)

def main():
    package_table = HashTable()

    load_packages("../data/WGUPS Package File CLEAN 2.csv", package_table)

    # TEST 1: print all packages
    for package in package_table.get_all():
        print(package)

    # TEST 2: Print Look-Up
    print("\nTEST LOOKUP:")
    print(package_table.lookup(1))

    # TEST 3:  distance table
    distance_table = DistanceTable()
    distance_table.load_data("../data/WGUPS Distance Table CLEAN 2.csv")

    print("\nTEST DISTANCE:")
    print(distance_table.get_distance("4001 South 700 East", "195 W Oakland Ave"))

if __name__ == "__main__":
    main()