import bcrypt;
from datetime import datetime

class Credential:
    def __init__(self, password: str):
        bpassword = password.encode()
        self.secret = bcrypt.hashpw(bpassword, bcrypt.gensalt())

    def check_password(self, password: str):
        bpassword = password.encode()
        return bcrypt.checkpw(bpassword, self.secret)

class User:
    def __init__(self, username: str, credential: Credential):
        self.username = username
        self.credential = credential

class Reservation:
    def __init__(self, datetime: datetime):
        self.datetime = datetime

user_data = {
    "mlandes": User("mlandes", Credential("mtest")),
    "rlandes": User("rlandes", Credential("rtest"))
}

reservation_data = {
    "mlandes": [
        Reservation(datetime.fromisoformat("2023-12-01T05:00:00")),
        Reservation(datetime.fromisoformat("2023-12-04T10:00:00")),
        Reservation(datetime.fromisoformat("2023-12-05T10:30:00"))
    ],
    "rlandes": [
        Reservation(datetime.fromisoformat("2023-12-01T05:30:00")),
        Reservation(datetime.fromisoformat("2023-12-03T10:00:00"))
    ]
}

def get_user(username: str):
    return user_data.get(username)

def get_reservations(username: str):
    return reservation_data.get(username, [])

def get_all_reservation_times():
    result: set[datetime] = set()
    for reservations in reservation_data.values():
        times = [r.datetime for r in reservations]
        result.update(times)

    return list(result)

def add_reservation(username: str, time: datetime):
    reservation = Reservation(time)
    reservation_data.get(username, []).append(reservation)