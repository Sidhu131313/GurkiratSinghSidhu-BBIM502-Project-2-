# File name: lhms.py
# Student name: YOUR NAME HERE
# Description: Console-based LANGHAM Hotel Management System (LHMS).
#              Adds, deletes, displays, allocates and bills rooms,
#              and saves room allocations to a text file.
# Date: 06/10/2026

import datetime

FILE_NAME = "LHMS_STUDENTID.txt"
GST_RATE = 0.15

# Global data: each room is a dictionary
rooms = [
    {"room_no": 101, "room_type": "Single", "price_per_night": 150.0, "status": "Available", "allocated_to": ""},
    {"room_no": 102, "room_type": "Double", "price_per_night": 220.0, "status": "Available", "allocated_to": ""},
    {"room_no": 201, "room_type": "Suite", "price_per_night": 400.0, "status": "Available", "allocated_to": ""},
]


def find_room(room_no):
    """Return the room with this number, or None if it is not in the list."""
    for room in rooms:
        if room["room_no"] == room_no:
            return room
    return None


def add_room():
    """Add one or more new rooms to the rooms list."""
    count = int(input("How many rooms do you want to add? "))

    for i in range(count):
        print(f"\nRoom {i + 1} of {count}")
        room_no = int(input("Room number: "))

        if find_room(room_no) is not None:
            print("That room number already exists.")
            continue

        room_type = input("Room type (Single/Double/Suite): ")
        price = float(input("Price per night: "))

        new_room = {
            "room_no": room_no,
            "room_type": room_type,
            "price_per_night": price,
            "status": "Available",
            "allocated_to": "",
        }
        rooms.append(new_room)
        print(f"Room {room_no} added.")


def delete_room():
    """Delete a room from the list."""
    room_no = int(input("Enter the room number to delete: "))
    room = find_room(room_no)

    if room is None:
        print("Room not found.")
    elif room["status"] == "Allocated":
        # A booked room cannot be removed until the guest checks out
        print("This room is allocated. Bill and de-allocate it first.")
    else:
        rooms.remove(room)
        print(f"Room {room_no} deleted.")


def display_rooms():
    """Show the details of every room."""
    if len(rooms) == 0:
        print("There are no rooms in the system.")
        return

    print(f"\n{'Room':<8}{'Type':<10}{'Price/Night':<14}{'Status':<12}")
    print("-" * 44)
    for room in rooms:
        price = f"${room['price_per_night']:.2f}"
        print(f"{room['room_no']:<8}{room['room_type']:<10}{price:<14}{room['status']:<12}")


def allocate_room():
    """Book an available room for a customer."""
    room_no = int(input("Enter the room number to allocate: "))
    room = find_room(room_no)

    if room is None:
        print("Room not found.")
    elif room["status"] == "Allocated":
        print(f"Room {room_no} is already allocated to {room['allocated_to']}.")
    else:
        customer = input("Customer name: ")
        room["status"] = "Allocated"
        room["allocated_to"] = customer
        print(f"Room {room_no} allocated to {customer}.")


def display_allocations():
    """Show the rooms that are currently allocated."""
    found = False

    print(f"\n{'Room':<8}{'Type':<10}{'Price/Night':<14}{'Customer':<20}")
    print("-" * 52)
    for room in rooms:
        if room["status"] == "Allocated":
            price = f"${room['price_per_night']:.2f}"
            print(f"{room['room_no']:<8}{room['room_type']:<10}{price:<14}{room['allocated_to']:<20}")
            found = True

    if not found:
        print("No rooms are allocated right now.")


def billing_and_deallocation():
    """Create the bill for an allocated room and release the room."""
    room_no = int(input("Enter the room number to bill: "))
    room = find_room(room_no)

    if room is None:
        print("Room not found.")
        return
    if room["status"] != "Allocated":
        print("This room is not allocated, so there is nothing to bill.")
        return

    nights = int(input("Number of nights stayed: "))
    subtotal = room["price_per_night"] * nights
    gst = subtotal * GST_RATE
    total = subtotal + gst

    print("\n----- LANGHAM HOTELS BILL -----")
    print(f"Customer : {room['allocated_to']}")
    print(f"Room     : {room['room_no']} ({room['room_type']})")
    print(f"Nights   : {nights} x ${room['price_per_night']:.2f}")
    print(f"Subtotal : ${subtotal:.2f}")
    print(f"GST (15%): ${gst:.2f}")
    print(f"Total    : ${total:.2f}")
    print("-------------------------------")

    # Release the room so it can be booked again
    room["status"] = "Available"
    room["allocated_to"] = ""
    print(f"Room {room_no} is now available.")


def save_to_file():
    """Save the allocated rooms to the allocation file."""
    allocated = []
    for room in rooms:
        if room["status"] == "Allocated":
            allocated.append(room)

    if len(allocated) == 0:
        print("There are no allocated rooms to save.")
        return

    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    """
    Mode "a" creates the file if it does not exist yet.
    It also keeps older saves, so option 9 always has
    real data to back up.
    """
    file = open(FILE_NAME, "a")
    file.write("Saved on " + now + "\n")
    for room in allocated:
        line = f"{room['room_no']} | {room['room_type']} | ${room['price_per_night']:.2f} | {room['allocated_to']}"
        file.write(line + "\n")
    file.write("\n")
    file.close()
    print(f"{len(allocated)} allocation(s) saved to {FILE_NAME}.")


def show_from_file():
    """Read the allocation file and display it on the screen."""
    file = open(FILE_NAME, "r")
    content = file.read()
    file.close()

    if content == "":
        print("The file is empty.")
    else:
        print("\n--- Room Allocations Saved in File ---")
        print(content)


def backup_and_clear():
    """Copy the allocation file into a backup file, then clear it."""
    file = open(FILE_NAME, "r")
    content = file.read()
    file.close()

    if content == "":
        print("Nothing to back up, the file is already empty.")
        return

    # Colons are not allowed in Windows file names, so the time uses dashes
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = "LHMS_STUDENTID_Backup_" + stamp + ".txt"

    backup = open(backup_name, "a")
    backup.write(content)
    backup.close()

    # Mode "w" wipes the old content, so this clears the file
    file = open(FILE_NAME, "w")
    file.close()
    print(f"Backup saved as {backup_name} and {FILE_NAME} has been cleared.")


def exit_app():
    """Say goodbye before the program closes."""
    print("Thank you for using the LANGHAM Hotel Management System. Goodbye!")


def main():
    """Show the menu and run the chosen option until the user exits."""
    while True:
        print("\n" + "*" * 60)
        print("            LANGHAM HOTEL MANAGEMENT SYSTEM")
        print("                        MENU")
        print("*" * 60)
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
        print("*" * 60)
        choice = input("Enter Your Choice Number Here: ")

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
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")


main()