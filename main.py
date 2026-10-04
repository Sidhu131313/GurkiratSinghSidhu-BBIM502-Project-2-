
# Constants 
STATUS_AVAILABLE = "Available"   # status text for a free room
STATUS_OCCUPIED = "Occupied"     # status text for a booked room
ROOM_TYPES = ["Single", "Double", "Deluxe", "Suite"]   # allowed room types


"""
Each room is one dictionary with five keys:
    room_no         : whole number, must be unique (for example 101)
    room_type       : one of the words in ROOM_TYPES
    price_per_night : price in NZD, stored as a float (for example 150.0)
    status          : STATUS_AVAILABLE or STATUS_OCCUPIED
    allocated_to    : guest name, or "" when nobody is staying
All room dictionaries are kept together in the list called rooms.
"""
rooms = [
    {"room_no": 101, "room_type": "Single", "price_per_night": 150.0,
     "status": STATUS_AVAILABLE, "allocated_to": ""},
    {"room_no": 102, "room_type": "Double", "price_per_night": 220.0,
     "status": STATUS_OCCUPIED, "allocated_to": "Aroha Smith"},
    {"room_no": 201, "room_type": "Deluxe", "price_per_night": 320.0,
     "status": STATUS_AVAILABLE, "allocated_to": ""},
    {"room_no": 202, "room_type": "Suite", "price_per_night": 480.0,
     "status": STATUS_AVAILABLE, "allocated_to": ""},
]


#Helper functions
def show_menu():
    """Print the main menu of the system."""
    print()
    print("*" * 50)
    print("LANGHAM HOTEL MANAGEMENT SYSTEM MENU")
    print("*" * 50)
    print("1. Add Rooms")
    print("2. Delete Room")
    print("3. Display Rooms Details")
    print("4. Allocate Rooms")
    print("5. Display Room Allocation Details")
    print("6. Billing & De-Allocation")
    print("7. Save Room Allocation to File")
    print("8. Show Room Allocation from File")
    print("9. Backup & Clear File")
    print("0. Exit")
    print("*" * 50)


def print_heading(title):
    """Print a title between two lines of stars."""
    print()
    print("*" * 50)
    print(title.center(50))
    print("*" * 50)


def find_room(room_no):
    """Return the dictionary of the room with this room number, or None if there is no such room."""
    for room in rooms:
        if room["room_no"] == room_no:
            return room
    return None


def print_room_table(room_list):
    """Print the rooms in room_list as a table with one row per room."""
    print(f"{'Room No':<10}{'Type':<12}{'Price (NZD)':>12}   {'Status':<12}{'Allocated To'}")
    print("-" * 50)
    for room in room_list:
        # Read the five values of this room
        room_no = room["room_no"]
        room_type = room["room_type"]
        price = room["price_per_night"]
        status = room["status"]
        guest = room["allocated_to"]

        # Show a dash when nobody is staying in the room
        if guest == "":
            guest = "-"

        # :<10 means left align in 10 spaces, :>12.2f means right align with 2 decimals
        print(f"{room_no:<10}{room_type:<12}{price:>12.2f}   {status:<12}{guest}")
    print("-" * 50)


# ---------- Part A: menu option functions ----------
def add_room():
    """Option 1: add one or more new rooms to the rooms list."""
    print_heading("ADD ROOM")

    # Build the room types text once, for example "Single/Double/Deluxe/Suite"
    types_text = "/".join(ROOM_TYPES)

    add_more = True
    while add_more:
        # Read the details of the new room as text first
        room_no_text = input("Enter room number (for example 301): ").strip()
        room_type = input(f"Enter room type ({types_text}): ").strip().title()
        price_text = input("Enter price per night in NZD (for example 250 or 250.50): ").strip()

        # Check the inputs one by one, the first problem found is reported
        if not room_no_text.isdigit():
            print("Error: room number must be a whole number (digits only).")
        elif int(room_no_text) == 0:
            print("Error: room number must be greater than zero.")
        elif find_room(int(room_no_text)) is not None:
            print(f"Error: room {int(room_no_text)} already exists.")
        elif room_type not in ROOM_TYPES:
            print(f"Error: room type must be one of {types_text}.")
        elif not price_text.replace(".", "", 1).isdigit():
            # replace() removes one dot so that 250.50 still counts as a number
            print("Error: price must be a number such as 250 or 250.50.")
        elif float(price_text) <= 0:
            print("Error: price must be greater than zero.")
        else:
            # All checks passed, so build the room dictionary and add it to the list
            new_room = {
                "room_no": int(room_no_text),
                "room_type": room_type,
                "price_per_night": float(price_text),
                "status": STATUS_AVAILABLE,
                "allocated_to": ""
            }
            # No "global" keyword is needed because append() changes the list, it does not replace it
            rooms.append(new_room)
            print(f"Room {new_room['room_no']} ({room_type}) added successfully.")

        # Keep looping only if the user types y
        answer = input("Do you want to enter another room? (y/n): ").strip().lower()
        if answer != "y":
            add_more = False


def delete_room():
    """Option 2: delete one or more rooms from the rooms list."""
    print_heading("DELETE ROOM")

    # Nothing to do when the list is empty
    if len(rooms) == 0:
        print("There are no rooms to delete.")
        return

    delete_more = True
    while delete_more:
        # Show the rooms first so the user can see which room numbers exist
        print_room_table(rooms)
        room_no_text = input("Enter the room number to delete: ").strip()

        # Look for the room, but only when the text is a number
        room = None
        if room_no_text.isdigit():
            room = find_room(int(room_no_text))

        if room is None:
            print(f"Error: room {room_no_text} was not found.")
        elif room["status"] == STATUS_OCCUPIED:
            # A room with a guest in it must not be deleted
            print(f"Error: room {room_no_text} is occupied. De-allocate it first (option 6).")
        else:
            confirm = input(f"Delete room {room_no_text}? (y/n): ").strip().lower()
            if confirm == "y":
                rooms.remove(room)
                print(f"Room {room_no_text} deleted successfully.")
            else:
                print("Delete cancelled.")

        # Ask again only if there are still rooms left in the list
        if len(rooms) == 0:
            print("There are no rooms left in the list.")
            delete_more = False
        else:
            answer = input("Do you want to delete another room? (y/n): ").strip().lower()
            if answer != "y":
                delete_more = False


def display_rooms():
    """Option 3: show the details of every room (type, price and status) before booking."""
    print_heading("ROOM DETAILS")

    # Stop early when there are no rooms
    if len(rooms) == 0:
        print("No rooms found. Use option 1 to add a room.")
        return

    print_room_table(rooms)

    # Count the free rooms, the rest must be occupied
    available_count = 0
    for room in rooms:
        if room["status"] == STATUS_AVAILABLE:
            available_count += 1
    occupied_count = len(rooms) - available_count

    print(f"Total rooms: {len(rooms)} | Available: {available_count} | Occupied: {occupied_count}")


# ---------- Main program ----------
def main():
    """Show the menu again and again until the user chooses 0 to exit."""
    running = True

    # The WHILE loop keeps the program open until the user chooses to exit
    while running:
        show_menu()
        choice = input("Enter Your Choice Number Here: ").strip()

        # Call the function that matches the menu choice
        if choice == "1":
            add_room()
        elif choice == "2":
            delete_room()
        elif choice == "3":
            display_rooms()
        elif choice in ["4", "5", "6", "7", "8", "9"]:
            # TEMPORARY: these options are added in later stages
            print(f"Option {choice} is not built yet.")
        elif choice == "0":
            # TEMPORARY: this will be replaced by exit_app() in a later stage
            print("Goodbye!")
            running = False
        else:
            print("Invalid choice. Please enter a number from 0 to 9.")


# Run main() only when this file is started directly
if __name__ == "__main__":
    main()