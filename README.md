# WGUPS Routing Program

## Overview

This project implements a package delivery system for the Western Governors University Parcel Service (WGUPS). The goal
is to deliver all packages efficiently while meeting delivery constraints and minimizing total mileage.

The program uses the **Nearest Neighbor Algorithm** to determine delivery routes and a **custom hash table** to store
and manage package data.

---

## Features

- Loads package data from CSV file
- Stores package data using a custom hash table
- Simulates delivery using multiple trucks
- Tracks:
    - Delivery status (At Hub, En Route, Delivered)
    - Delivery time
    - Truck assignment
- Handles special constraints:
    - Delayed packages (not available until 9:05 AM)
    - Incorrect address (Package #9 corrected at 10:20 AM)
    - Required truck assignments for specific packages
    - Two-driver constraint (Truck 3 starts only after a driver becomes available)
- Calculates total mileage traveled by all trucks
- Provides an **interactive user interface** to check package status at any time

---

## Technologies Used

- Python 3
- CSV file processing
- Custom data structures (Hash Table)
- Nearest Neighbor Algorithm

---

## How to Run

1. Navigate to the project directory
2. Run the program:

```bash
python src/main.py
```

3. When prompted, enter a time in **HH:MM format**:

Example:
`Enter time (HH:MM, e.g., 09:00):`

4. The program will display the status of all packages at that time.

5. To exit the program, type:

`exit`

---

## Algorithm Used

### Nearest Neighbor Algorithm

The program selects the closest next delivery location at each step. While not always globally optimal, it provides an
efficient and practical routing solution for this scenario.

---

## Data Structure Used

### Hash Table

A custom hash table is used to store package data using the package ID as the key. This allows fast lookup and updates
during delivery simulation (average O(1) time complexity).

---

## Assumptions

- Each truck can carry a maximum of 16 packages
- Trucks travel at an average speed of 18 miles per hour
- There are three trucks and two drivers available
- Drivers remain with their assigned truck
- Truck 3 begins delivery only after one driver becomes available
- Delivery and loading times are considered instantaneous
- Distances are symmetric (same in both directions)
- The day ends when all 40 packages are delivered

---

## Author

Drum Holliday

---

## Notes

This project was completed as part of WGU coursework for Data Structures and Algorithms II.