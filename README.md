# Package Delivery Route Planner

## Overview

Package Delivery Route Planner is a Python-based delivery routing simulation that uses custom data structures and route planning logic to manage package deliveries across multiple trucks.

The program loads package and distance data from CSV files, assigns packages to trucks, simulates delivery progress throughout the day, and allows users to check package status at a specific time.

The project demonstrates practical use of data structures, algorithmic route planning, CSV data processing, and delivery status tracking.

## Project Purpose

The purpose of this project is to simulate a package delivery operation where multiple trucks must deliver packages efficiently while meeting delivery constraints.

The system is designed to:

* Load package and distance data from CSV files
* Store package information in a custom hash table
* Assign packages to delivery trucks
* Plan delivery routes using a nearest-neighbor approach
* Track delivery status over time
* Calculate total mileage traveled
* Provide an interactive status lookup by time

## Features

* Loads package data from CSV files
* Loads distance and address data from CSV files
* Stores package records using a custom hash table
* Simulates delivery using multiple trucks
* Tracks package status throughout the day
* Tracks truck assignment and delivery time
* Handles delayed packages
* Handles corrected address information
* Handles packages with truck-specific requirements
* Accounts for a limited number of available drivers
* Calculates total mileage traveled by all trucks
* Provides an interactive command-line interface
* Allows users to check all package statuses at a selected time
* Prioritizes packages with earlier delivery deadlines during route planning

## Technologies Used

* Python 3
* CSV file processing
* Custom hash table
* Nearest Neighbor Algorithm
* Command-line interface
* Git
* GitHub

## Project Structure

```text
package-delivery-route-planner/
├── data/
│   ├── distance_table.csv
│   └── package_file.csv
│
├── src/
│   ├── main.py
│   └── additional source files
│
├── README.md
├── commit_history.txt
└── .gitignore
```

The exact file names may vary depending on the current version of the project.

## How the Program Works

The program follows this general process:

1. Load package data from the package CSV file.
2. Load address and distance data from the distance CSV file.
3. Store package records in a custom hash table.
4. Assign packages to trucks based on delivery requirements and constraints.
5. Use a nearest-neighbor routing approach to determine delivery order.
6. Simulate truck travel and package delivery times.
7. Update each package status throughout the simulation.
8. Display total mileage after all packages are delivered.
9. Allow the user to enter a time and view package statuses at that moment.

## Algorithm Used

### Nearest Neighbor Algorithm

The project uses a nearest-neighbor approach to select the next delivery location.

At each step, the truck chooses the closest available delivery address from its current location. This process repeats until the truck has delivered all assigned packages.

This approach is not guaranteed to produce the mathematically optimal route in every case, but it provides a practical and efficient solution for this type of delivery simulation.

## Data Structure Used

### Custom Hash Table

A custom hash table is used to store and manage package data.

Package IDs are used as keys, allowing the program to quickly retrieve, update, and display package information.

The hash table supports efficient package lookup and status updates during the delivery simulation.

Average lookup complexity:

```text
O(1)
```

## Delivery Status Tracking

Each package can have a status such as:

* At hub
* En route
* Delivered

The program updates package statuses based on the simulated delivery timeline. Users can enter a specific time and view the status of each package at that time.

## Delivery Constraints

The simulation accounts for several delivery constraints, including:

* Package delivery deadlines
* Delayed package availability
* Corrected address information
* Required truck assignments
* Limited driver availability
* Truck capacity limits
* Multi-truck routing
* Total mileage calculation

## Assumptions

The simulation uses the following assumptions:

* Each truck has a maximum package capacity.
* Trucks travel at a fixed average speed.
* Multiple trucks are available.
* Driver availability may limit when certain trucks can depart.
* Drivers remain with their assigned truck.
* Loading and handoff times are treated as instantaneous.
* Distance values are treated as symmetric.
* The simulation ends when all packages are delivered.

## Running the Project

From the project root directory, run:

```bash
python src/main.py
```

Depending on your Python environment, you may need to use:

```bash
python3 src/main.py
```

## Interactive Time Lookup

When prompted, enter a time in `HH:MM` format.

Example:

```text
09:00
```

The program will display the package status information for that selected time.

To exit the program, enter:

```text
exit
```

## Example Output

The program may display information such as:

```text
Package ID: 1
Address: 195 W Oakland Ave
Status: Delivered
Delivery Time: 09:35
Truck: 1
```

It may also display the total mileage traveled by all trucks after the simulation is complete.

## Portfolio Highlights

This project demonstrates experience with:

* Python programming
* Custom data structures
* Hash table implementation
* Route planning logic
* CSV file parsing
* Delivery simulation
* Algorithmic problem solving
* Time-based status tracking
* Command-line interaction
* Git and GitHub version control

## Future Enhancements

Possible future improvements include:

* Add a graphical route visualization
* Add a web-based dashboard
* Add support for uploading new package and distance files
* Add additional routing algorithms for comparison
* Add automated tests for package lookup and delivery logic
* Add mileage comparison between different algorithms
* Add database storage for package and route data
* Add a REST API for package status queries
* Add Docker support
* Add improved reporting and analytics

## Academic and Portfolio Note

This project was created for academic learning and portfolio development. It demonstrates data structures, algorithm design, routing logic, and Python-based simulation.

## Author

Drum Holliday

## License

This project is currently for educational and portfolio purposes. A formal license can be added later if the project is prepared for public reuse.
