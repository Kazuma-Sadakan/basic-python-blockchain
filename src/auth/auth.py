from src import login_manager
from flask_login import UserMixin
from src.wallet.wallet import Wallet

HOST = "localhost"
PORT = 3000
URL = f"{HOST}:{PORT}"

class User(UserMixin):
    def __init__(self, private_key, public_key, address):
        self.id = private_key
        self.private_key = private_key 
        self.public_key = public_key 
        self.address = address
        self.authenticated = False 

    def is_active(self):
        return self.is_active()

    def is_anonymous(self):
        return False 

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True 

    def get_id(self):
        return  self.id

@login_manager.user_loader 
def load_user(_private_key):
    try:
        wallet = Wallet(URL, _private_key)
        return User(**wallet.get())
    except Exception as e:
        print(f"Error: {e}")
        return None

