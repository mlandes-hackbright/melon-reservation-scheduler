class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

user_data = {
    "mlandes": User("mlandes", "test")
}

def get_user(username):
    return user_data.get(username)
