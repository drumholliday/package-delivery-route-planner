import csv


class DistanceTable:
    def __init__(self):
        self.addresses = []
        self.distance_data = []

    def load_data(self, file_path):
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

            # Clean and load addresses (skip first blank cell)
            self.addresses = [
                addr.replace('\n', ' ').replace('"', '').strip()
                for addr in rows[0][1:]
                if addr.strip() != ""
            ]

            # Load and clean distance matrix
            for row in rows[1:]:
                row_data = []

                for value in row[1:]:
                    cleaned = value.replace('\n', '').replace('"', '').strip()

                    if cleaned == "":
                        row_data.append(None)
                    else:
                        row_data.append(float(cleaned))

                self.distance_data.append(row_data)

    def get_distance(self, address1, address2):
        # Clean input just in case
        address1 = address1.strip()
        address2 = address2.strip()

        i = self.addresses.index(address1)
        j = self.addresses.index(address2)

        distance = self.distance_data[i][j]

        # Use symmetric value if empty
        if distance is None:
            distance = self.distance_data[j][i]

        return distance

# class DistanceTable:
#     def __init__(self):
#         self.addresses = []
#         self.distances = []
#
#     def load_data(self, file_path):
#         with open(file_path, newline='') as csvfile:
#             reader = csv.reader(csvfile)
#
#             for i, row in enumerate(reader):
#                 if i == 0:
#                     continue  # skip header
#
#                 # first column = address
#                 address = row[0]
#                 self.addresses.append(address)
#
#                 # rest = distances
#                 self.distances.append(row[1:])

# class DistanceTable:
#     def __init__(self):
#         self.addresses = []
#         self.distances = []
#
#     def load_data(self, file_path):
#         with open(file_path, newline='') as csvfile:
#             reader = csv.reader(csvfile)
#
#             for i, row in enumerate(reader):
#                 if i == 0:
#                     # First row is column headers (addresses)
#                     self.addresses = row[1:]
#                 else:
#                     # First column is row label (address), rest are distances
#                     self.distances.append(row[1:])