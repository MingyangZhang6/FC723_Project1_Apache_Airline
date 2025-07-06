"""
Booking_System_v2 – FC723  |  Author: P460084
Part B upgrade:
  1. Generates a unique 8-character alphanumeric reference.
  2. Stores / removes traveller details in a local SQLite DB (airline.db).
"""

import random
import string
import sqlite3

# ── Re-use core objects from Part A script ────────────────────────────────────
from Booking_System import (
    seat_map,        # {(row, col): 'F' | 'R' | 'X' | 'S'}
    seat_key,        # "12B" → (12, "B")   + validation
    print_seat_map,  # prints the full seat map
    available_seats, # list of free seats
    check_seat       # check one seat
)

DB_NAME = "airline.db"

# ── 1. Set-up / open database ────────────────────────────────────────────────
def init_db() -> None:
    """Create table <bookings> if it does not exist."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS bookings (
                   ref        TEXT PRIMARY KEY,
                   passport   TEXT,
                   first_name TEXT,
                   last_name  TEXT,
                   seat_row   INTEGER,
                   seat_col   TEXT
               );"""
        )

# ── 2. Unique 8-char booking reference ──────────────────────────────────────
def existing_refs() -> set[str]:
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("SELECT ref FROM bookings")
        return {row[0] for row in rows}

def new_ref() -> str:
    chars = string.ascii_uppercase + string.digits
    used  = existing_refs()
    while True:
        ref = "".join(random.choices(chars, k=8))
        if ref not in used:
            return ref

# ── 3. Book and cancel seats (DB aware) ──────────────────────────────────────
def book_seat_db() -> None:
    code = input("Enter seat code to book (e.g. 12B): ").strip().upper()
    try:
        key = seat_key(code)
    except ValueError as err:
        print(err); return

    if seat_map[key] != "F":
        print("That seat is not free."); return

    passport = input("Passport number : ").strip()
    first    = input("First name      : ").strip()
    last     = input("Last  name      : ").strip()
    ref      = new_ref()

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO bookings VALUES (?,?,?,?,?,?)",
            (ref, passport, first, last, key[0], key[1])
        )

    seat_map[key] = "R"
    print(f"Seat {code} booked successfully.  Booking reference: {ref}")

def free_seat_db() -> None:
    code = input("Enter seat code to cancel: ").strip().upper()
    try:
        key = seat_key(code)
    except ValueError as err:
        print(err); return

    if seat_map[key] != "R":
        print("That seat is not currently reserved."); return

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "DELETE FROM bookings WHERE seat_row=? AND seat_col=?",
            (key[0], key[1])
        )

    seat_map[key] = "F"
    print(f"Seat {code} is now free.")

# ── 4. Main loop ─────────────────────────────────────────────────────────────
def main() -> None:
    init_db()
    MENU = """
============ Apache Airlines Seat-Booking (DB) ============
1  Check availability of a seat
2  Book a seat   (stores reference + passenger info)
3  Free a seat   (removes DB record)
4  Show full seat map
5  Show ALL available seats
6  Exit
===========================================================
"""
    while True:
        print(MENU)
        choice = input("Choose option 1-6: ").strip()
        if   choice == "1": check_seat()
        elif choice == "2": book_seat_db()
        elif choice == "3": free_seat_db()
        elif choice == "4": print_seat_map()
        elif choice == "5":
            free_list = available_seats()
            print(f"\nTotal free seats: {len(free_list)}")
            print(", ".join(free_list) or "None")
        elif choice == "6":
            print("Good-bye!"); break
        else:
            print("Invalid choice, please enter 1-6.")

if __name__ == "__main__":
    main()