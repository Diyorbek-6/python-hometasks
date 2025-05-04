from datetime import datetime, timedelta, date
from abc import ABC, abstractmethod
from collections import defaultdict

# ------------------------ Room Class ------------------------
class Room:
    def __init__(self, room_id, room_type, price, amenities, location):
        self.room_id = room_id
        self.room_type = room_type
        self.price = price
        self.amenities = amenities
        self.location = location
        self.booked_dates = []

    def is_available(self, start_date, end_date):
        for date_check in self.booked_dates:
            if start_date <= date_check <= end_date:
                return False
        return True

# ------------------------ Customer Class ------------------------
class Customer:
    def __init__(self, name, is_vip=False):
        self.name = name
        self.is_vip = is_vip

# ------------------------ Booking Class ------------------------
class Booking:
    def __init__(self, customer, room, start_date, end_date, discount=0.0):
        self.customer = customer
        self.room = room
        self.start_date = start_date
        self.end_date = end_date
        self.discount = discount
        self.total_days = (end_date - start_date).days + 1
        self.total_price = self.calculate_price()
        self.log_booking()
        for i in range(self.total_days):
            self.room.booked_dates.append(start_date + timedelta(days=i))

    def calculate_price(self):
        base_price = self.room.price * self.total_days
        return base_price * (1 - self.discount)

    def cancel_booking(self, cancel_percent=0.8):
        refund = self.total_price * cancel_percent
        return refund

    def log_booking(self):
        with open("booking_log.txt", "a") as file:
            file.write(f"{datetime.now()}: {self.customer.name} booked Room {self.room.room_id} "
                       f"from {self.start_date} to {self.end_date}, Total: {self.total_price}\n")

# ------------------------ Hotel Class ------------------------
class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.bookings = []

    def add_room(self, room):
        self.rooms.append(room)

    def filter_rooms(self, price=None, amenities=None, location=None):
        result = self.rooms
        if price is not None:
            result = [r for r in result if r.price <= price]
        if amenities:
            result = [r for r in result if set(amenities).issubset(set(r.amenities))]
        if location:
            result = [r for r in result if r.location == location]
        return result

    def revenue_report(self):
        report = defaultdict(float)
        for b in self.bookings:
            key = b.start_date.strftime("%Y-%m-%d")
            report[key] += b.total_price
        return dict(report)

# ------------------------ VIP Discount Decorator ------------------------
def vip_discount_decorator(func):
    def wrapper(customer, room, start_date, end_date):
        discount = 0.2 if customer.is_vip else 0.0
        return func(customer, room, start_date, end_date, discount)
    return wrapper

# ------------------------ Booking Creation Function ------------------------
@vip_discount_decorator
def create_booking(customer, room, start_date, end_date, discount=0.0):
    if room.is_available(start_date, end_date):
        booking = Booking(customer, room, start_date, end_date, discount)
        return booking
    else:
        print("Room is not available for the selected dates.")
        return None

# ------------------------ View Booking Logs ------------------------
def view_logs():
    with open("booking_log.txt", "r") as file:
        logs = file.read()
    print(logs)

# ------------------------ Sample Usage ------------------------
if __name__ == "__main__":
    hotel = Hotel("Hilton")
    r1 = Room(101, "Standard", 100, ["TV", "AC"], "Tashkent")
    r2 = Room(102, "Deluxe", 200, ["TV", "AC", "Mini Bar"], "Tashkent")
    hotel.add_room(r1)
    hotel.add_room(r2)

    c1 = Customer("Ali", is_vip=True)
    c2 = Customer("Vali", is_vip=False)

    booking1 = create_booking(c1, r1, date(2025, 5, 10), date(2025, 5, 12))
    booking2 = create_booking(c2, r2, date(2025, 5, 11), date(2025, 5, 12))

    if booking1:
        hotel.bookings.append(booking1)
    if booking2:
        hotel.bookings.append(booking2)

    print("Refund on cancel:", booking1.cancel_booking())
    print("Revenue Report:", hotel.revenue_report())
    print("Filtered Rooms:", hotel.filter_rooms(price=150, amenities=["AC"]))
    view_logs()
