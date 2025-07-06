"""
Apache Airlines – Burak757 Seat-Booking System  (Part A version)

Menu:
1. Check availability of seat
2. Book a seat
3. Free a seat
4. Show booking status (full seat map)
5. Show all available seats             ← Extra requirement
6. Exit program

Author: P460084  •  Module: FC723  •  Tutor: Sophie Norman
"""

# ---------------------- 1 Generate initial seat map -------------------------- #
ROWS = list(range(1, 81))               # 1-80
SEAT_LETTERS = ["A", "B", "C", "D", "E", "F"]

# Build dictionary {(row, col): status}
#  status: 'F' free  •  'R' reserved  •  'X' aisle  •  'S' storage
seat_map = {}

for row in ROWS:
    for col in SEAT_LETTERS:
        # Aisle between C and D is marked later when printing – we still store seats.
        status = "F"

        # Storage rows: 77-78 on D/E/F per brief
        if row in (77, 78) and col in ("D", "E", "F"):
            status = "S"
        seat_map[(row, col)] = status

# ---------------------- 2 Helper functions ----------------------------------- #
def seat_key(seat_code: str):
    """
    Convert '12B' -> (12, 'B'); raises ValueError on invalid code.
    """
    try:
        row = int(''.join(filter(str.isdigit, seat_code)))
        col = ''.join(filter(str.isalpha, seat_code)).upper()
        if row not in ROWS or col not in SEAT_LETTERS:
            raise ValueError
    except ValueError:
        raise ValueError("Seat code must be like '12B' in valid range 1-80 and A-F.")
    return row, col


def print_seat_map():
    """
    Pretty-prints the whole seat map in 3-3 layout with aisle.
    """
    print("\n=== Burak757 Seat Map (F = Free, R = Reserved, X = Aisle, S = Storage) ===")
    header = "Row |  A  B  C   |   D  E  F"
    print(header)
    print("-" * len(header))
    for r in ROWS:
        left = "  ".join(seat_map[(r, c)] for c in ("A", "B", "C"))
        right = "  ".join(
            seat_map[(r, c)] if seat_map[(r, c)] != "F" else "F" for c in ("D", "E", "F")
        )
        row_str = f"{r:>3} |  {left}  |   {right}"
        print(row_str)
    print()


def available_seats():
    """
    Return list of seat codes that are free.
    """
    return [f"{row}{col}" for (row, col), status in seat_map.items() if status == "F"]


# ---------------------- 3 Core menu functions -------------------------------- #
def check_seat():
    code = input("Enter seat code (e.g. 12B): ").strip()
    try:
        key = seat_key(code)
    except ValueError as e:
        print(e)
        return
    status = seat_map[key]
    if status == "F":
        print(f"Seat {code.upper()} is FREE.")
    elif status == "R":
        print(f"Seat {code.upper()} is already RESERVED.")
    elif status in ("X", "S"):
        print(f"Seat {code.upper()} cannot be booked – it is {status}.")
    else:
        print(f"Seat {code.upper()} has unknown status!")


def book_seat():
    code = input("Enter seat code to book: ").strip()
    try:
        key = seat_key(code)
    except ValueError as e:
        print(e)
        return
    if seat_map[key] == "F":
        seat_map[key] = "R"
        print(f"Seat {code.upper()} successfully booked.")
    else:
        print(f"Seat {code.upper()} cannot be booked (status: {seat_map[key]}).")


def free_seat():
    code = input("Enter seat code to free: ").strip()
    try:
        key = seat_key(code)
    except ValueError as e:
        print(e)
        return
    if seat_map[key] == "R":
        seat_map[key] = "F"
        print(f"Seat {code.upper()} is now FREE.")
    else:
        print(f"Seat {code.upper()} is not currently reserved (status: {seat_map[key]}).")


# ---------------------- 4 Main loop ------------------------------------------ #
def main():
    MENU = """
================ Seat-Booking Menu ================
1  Check availability of seat
2  Book a seat
3  Free a seat
4  Show full booking status
5  Show ALL available seats           (extra)
6  Exit program
===================================================
"""
    while True:
        print(MENU)
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            check_seat()
        elif choice == "2":
            book_seat()
        elif choice == "3":
            free_seat()
        elif choice == "4":
            print_seat_map()
        elif choice == "5":
            free_list = available_seats()
            print(f"\nTotal free seats: {len(free_list)}")
            print(", ".join(free_list) if free_list else "None")
        elif choice == "6":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1-6.")

# ---------------------- 5 Entry point ---------------------------------------- #
if __name__ == "__main__":
    main()