# WGUPS Routing Program

## Overview
This project implements a package delivery system for the Western Governors University Parcel Service (WGUPS). The goal is to deliver all packages efficiently while meeting delivery constraints and minimizing total mileage.

The program uses the **Nearest Neighbor Algorithm** to determine delivery routes and a **custom hash table** to store and manage package data.

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
    - Delayed packages
    - Incorrect address (Package #9)
- Calculates total mileage traveled by all trucks
- Provides status checks at specific times

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
````
---
## Algorithm Used

### Nearest Neighbor Algorithm
The program selects the closest next delivery location at each step. While not always globally optimal, it provides efficient and practical routing for this scenario.

---

## Data Structure Used

### Hash Table
A custom hash table is used to store package data using the package ID as the key. This allows fast lookup and updates during delivery simulation.

---

## Author
Drum Holliday

---

## Notes
This project was completed as part of WGU coursework for Data Structures and Algorithms II.