import csv
from hash_table import HashTable
from package import Package


def load_packages(file_path, hash_table):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)

        next(reader)  # skip header row

        for row in reader:
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]  # not used, but included
            zip_code = row[4]
            deadline = row[5]
            weight = row[6]
            notes = row[7]

            package = Package(package_id, address, city, zip_code, deadline, weight, notes)

            hash_table.insert(package_id, package)


def main():
    package_table = HashTable()

    load_packages("../data/WGUPS Package File.csv", package_table)

    # TEST: print all packages
    for package in package_table.get_all():
        print(package)


if __name__ == "__main__":
    main()