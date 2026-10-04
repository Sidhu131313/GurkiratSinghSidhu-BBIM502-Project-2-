
# Global data: list of dictionaries, one dictionary for each room
rooms = [
    {"room_no": 101, "room_type": "Single", "price_per_night": 120.00,
     "status": "Available", "allocated_to": ""},
    {"room_no": 102, "room_type": "Double", "price_per_night": 180.00,
     "status": "Available", "allocated_to": ""},
    {"room_no": 201, "room_type": "Suite", "price_per_night": 350.00,
     "status": "Available", "allocated_to": ""},
]


def show_menu():
    """Print the LHMS application menu."""
    print("\n==== LANGHAM Hotel Management System ====")
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


# ---- Placeholder functions (real code will be added in later stages) ----

def add_room():
    """Add a new room to the rooms list."""
    print("add_room() not written yet")


def delete_room():
    """Delete a room from the rooms list."""
    print("delete_room() not written yet")


def display_rooms():
    """Show the details of all rooms."""
    print("display_rooms() not written yet")


def allocate_room():
    """Book an available room for a customer."""
    print("allocate_room() not written yet")


def display_allocations():
    """Show the rooms that are currently allocated."""
    print("display_allocations() not written yet")


def billing_and_deallocation():
    """Create the bill and release the room."""
    print("billing_and_deallocation() not written yet")


def save_to_file():
    """Save the room allocation data to the text file."""
    print("save_to_file() not written yet")


def show_from_file():
    """Read the text file and display its content."""
    print("show_from_file() not written yet")


def backup_and_clear():
    """Copy the data file to a backup file, then clear the data file."""
    print("backup_and_clear() not written yet")


def exit_app():
    """Say goodbye before the program closes."""
    print("Thank you for using LHMS. Goodbye!")


def main():
    """Run the main menu loop until the user chooses 0."""
    running = True

    # Keep showing the menu until the user chooses to exit
    while running:
        show_menu()
        choice = input("Enter your choice (0-9): ").strip()

        # Call the function that matches the menu option
        if choice == "1":
            add_room()
        elif choice == "2":
            delete_room()
        elif choice == "3":
            display_rooms()
        elif choice == "4":
            allocate_room()
        elif choice == "5":
            display_allocations()
        elif choice == "6":
            billing_and_deallocation()
        elif choice == "7":
            save_to_file()
        elif choice == "8":
            show_from_file()
        elif choice == "9":
            backup_and_clear()
        elif choice == "0":
            exit_app()
            running = False   # stops the while loop
        else:
            print("Invalid choice. Please enter a number from 0 to 9.")

main()