import bcrypt;

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

user_data = {
    "mlandes": User("mlandes", Credential("test"))
}

def get_user(username: str) -> User | None:
    return user_data.get(username)
