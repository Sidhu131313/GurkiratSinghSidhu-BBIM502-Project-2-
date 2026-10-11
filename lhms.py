# File name: lhms.py
# Student name: GURKIRAT SINGH
# Student ID: 850009367
# Description: Console-based LANGHAM Hotel Management System (LHMS). It adds, deletes,
#              allocates and bills rooms, and saves room allocations to a text file.
# Date: 11/10/2026

try:
    import datetime
except ImportError:  # Handles ImportError
    print("The datetime module is missing, so LHMS cannot start.")
    exit()

"""
Room rules used in this program:
- status is either "Available" or "Allocated"
- allocated_to holds the customer name, or an empty string when the room is free
- a bill adds 15% GST after the discount is taken off
"""

FILE_NAME = "LHMS_850009367.txt"
BACKUP_PREFIX = "LHMS_850009367_Backup_"
GST_RATE = 0.15

rooms = [
    {"room_no": 101, "room_type": "Single", "price_per_night": 150.0, "status": "Available", "allocated_to": ""},
    {"room_no": 102, "room_type": "Double", "price_per_night": 220.0, "status": "Available", "allocated_to": ""},
    {"room_no": 201, "room_type": "Suite", "price_per_night": 400.0, "status": "Available", "allocated_to": ""},
]


def add_room():
    """Add a new room to the rooms list."""
    try:
        room_no = int(input("Room number: "))
        room_type = input("Room type (Single/Double/Suite): ").capitalize()
        price = float(input("Price per night: "))
    except ValueError:  # Handles ValueError
        print("Room number and price must be numbers.")
        return

    if price < 0:
        print("Price must be more than 0.")
        return

    for room in rooms:
        if room["room_no"] == room_no:
            print("That room number already exists.")
            return

    rooms.append({"room_no": room_no, "room_type": room_type, "price_per_night": price,
                  "status": "Available", "allocated_to": ""})
    print("Room " + str(room_no) + " added.")


def delete_room():
    """Delete a room from the rooms list using its list number."""
    if len(rooms) == 0:
        print("There are no rooms to delete.")
        return

    display_rooms()
    try:
        choice = int(input("Enter the list number of the room to delete: "))
    except ValueError:  # Handles ValueError
        print("Please enter a whole number.")
        return

    # A negative index would count from the end of the list and delete the wrong room
    if choice < 1:
        print("The list number must be 1 or more.")
        return

    try:
        room = rooms[choice - 1]
    except IndexError:  # Handles IndexError
        print("There is no room with that list number.")
        return

    if room["status"] == "Allocated":
        print("This room is allocated. Bill and de-allocate it first.")
        return

    rooms.remove(room)
    print("Room " + str(room["room_no"]) + " deleted.")


def display_rooms():
    """Show all rooms and the average price per night."""
    total_price = 0
    for room in rooms:
        total_price += room["price_per_night"]

    try:
        average_price = total_price / len(rooms)
    except ZeroDivisionError:  # Handles ZeroDivisionError
        print("No rooms have been added yet.")
        return

    print(f"{'No.':<5}{'Room':<8}{'Type':<10}{'Price':<10}{'Status':<10}")
    for i in range(len(rooms)):
        room = rooms[i]
        print(f"{i + 1:<5}{room['room_no']:<8}{room['room_type']:<10}"
              f"${room['price_per_night']:<9.2f}{room['status']:<10}")
    print(f"Average price per night: ${average_price:.2f}")


def allocate_room():
    """Allocate an available room to a customer."""
    try:
        room_no = int(input("Room number to allocate: "))
    except ValueError:  # Handles ValueError
        print("Room number must be a whole number.")
        return

    for room in rooms:
        if room["room_no"] == room_no:
            if room["status"] == "Allocated":
                print("That room is already allocated.")
                return
            customer = input("Customer name: ")
            room["status"] = "Allocated"
            room["allocated_to"] = customer
            print("Room " + str(room_no) + " allocated to " + customer + ".")
            return

    print("Room number not found.")


def display_allocations():
    """Show all rooms that are currently allocated."""
    count = 0
    print(f"{'Room':<8}{'Type':<10}{'Customer':<20}")
    for room in rooms:
        if room["status"] == "Allocated":
            print(f"{room['room_no']:<8}{room['room_type']:<10}{room['allocated_to']:<20}")
            count += 1

    if count == 0:
        print("No rooms are allocated right now.")


def billing_and_deallocation():
    """Create the bill for an allocated room and release the room."""
    try:
        room_no = int(input("Room number to bill: "))
    except ValueError:  # Handles ValueError
        print("Room number must be a whole number.")
        return

    for r in rooms:
        if r["room_no"] == room_no:
            room = r
            break

    # room only exists if the loop above found the room number
    try:
        status = room["status"]
    except NameError:  # Handles NameError
        print("Room number not found.")
        return

    if status != "Allocated":
        print("This room is not allocated, so there is nothing to bill.")
        return

    try:
        nights = int(input("Number of nights stayed: "))
    except ValueError:  # Handles ValueError
        print("Nights must be a whole number.")
        return

    if nights < 1:
        print("Nights must be at least 1.")
        return

    # eval lets the clerk type a sum such as 20+10 (fine for a local pilot, not for a real system)
    try:
        discount = eval(input("Discount in dollars (0 for none, sums like 20+10 allowed): "))
    except SyntaxError:  # Handles SyntaxError
        print("The discount is not written correctly.")
        return
    except (NameError, ZeroDivisionError):
        print("The discount must be numbers only, for example 20+10.")
        return

    try:
        subtotal = room["price_per_night"] * nights
        if discount < 0 or discount > subtotal:
            print("The discount must be between 0 and the subtotal.")
            return
        gst = (subtotal - discount) * GST_RATE
        total = subtotal - discount + gst
    except TypeError:  # Handles TypeError
        print("A value in the bill is not a number, so the bill cannot be worked out.")
        return
    except OverflowError:  # Handles OverflowError
        print("The number of nights is too large to work out a bill.")
        return

    today = datetime.datetime.now().strftime("%d/%m/%Y")
    print("----- LANGHAM Hotels Bill -----")
    print("Date: " + today)
    print("Customer: " + room["allocated_to"])
    print(f"Room: {room['room_no']} ({room['room_type']})")
    print(f"Nights: {nights} x ${room['price_per_night']:.2f}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Discount: ${discount:.2f}")
    print(f"GST (15%): ${gst:.2f}")
    print(f"Total: ${total:.2f}")

    # Release the room for the next booking
    room["status"] = "Available"
    room["allocated_to"] = ""
    print("Room " + str(room["room_no"]) + " is now available.")


def save_to_file():
    """Save the current room allocations to the text file."""
    allocated = []
    for room in rooms:
        if room["status"] == "Allocated":
            allocated.append(room)

    if len(allocated) == 0:
        print("There are no allocations to save.")
        return

    try:
        file = open(FILE_NAME, "a")
        stamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        file.write("Saved on " + stamp + "\n")
        for room in allocated:
            file.write(f"Room {room['room_no']}, {room['room_type']}, "
                       f"${room['price_per_night']:.2f}, {room['allocated_to']}\n")
        file.close()
        print("Allocations saved to " + FILE_NAME + ".")
    except IOError:  # Handles IOError
        print("The file could not be opened or written.")


def show_from_file():
    """Display everything saved in the allocation file."""
    try:
        file = open(FILE_NAME, "r")
        content = file.read()
        file.close()
    except FileNotFoundError:  # Handles FileNotFoundError
        print("No file found yet. Use option 7 to save allocations first.")
        return

    if content == "":
        print("The file is empty.")
    else:
        print(content)


def backup_and_clear():
    """Copy the allocation file into a dated backup file, then clear it."""
    try:
        file = open(FILE_NAME, "r")
        content = file.read()
        file.close()

        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = BACKUP_PREFIX + stamp + ".txt"
        backup = open(backup_name, "a")
        backup.write(content)
        backup.close()

        # Opening in write mode empties the original file
        file = open(FILE_NAME, "w")
        file.close()
        print("Backed up to " + backup_name + " and cleared " + FILE_NAME + ".")
    except FileNotFoundError:  # Handles FileNotFoundError
        print("There is no file to back up yet.")
    except IOError:  # Handles IOError
        print("The backup could not be completed.")


def exit_app():
    """Say goodbye and close the program."""
    print("Thank you for using LHMS. Goodbye!")
    exit()


def main():
    """Show the menu and run the chosen option until the user exits."""
    while True:
        print("\n===== LANGHAM Hotel Management System =====")
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

        try:
            choice = input("Enter your choice (0-9): ")
        except EOFError:  # Handles EOFError
            print("\nInput ended. Closing LHMS.")
            exit_app()

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
        else:
            print("Invalid choice. Please enter a number from 0 to 9.")


main()