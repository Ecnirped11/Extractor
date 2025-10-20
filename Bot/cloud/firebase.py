import os
import firebase_admin
from firebase_admin import credentials, db

class SenderMailDatabaseManager:

    def __init__(self, sender_email: str, sender_username: str):
        # Make sure Python can find the JSON no matter 
        self.sender_email = sender_email
        self.sender_username = sender_username

        script_dir = os.path.dirname(os.path.abspath(__file__))
        auth_file = os.path.join(script_dir, "serviceAccountKey.json")

        if not os.path.exists(auth_file):
            raise FileNotFoundError(f"Cannot find {auth_file}!")
        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(auth_file)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://data-67a98-default-rtdb.firebaseio.com/'
            })
        # Only now get a reference to the database
        self.ref = db.reference("user-data")
        self.data = self.ref.get()
    def is_exist(self) -> bool:
        for key, user_data in self.data.items():
            if self.sender_username == user_data["username"]:
                user_mail = user_data["email"]
                return (
                    f"\n\n<b>STATUS</b>: found!\n\n"
                    f"<b>USERNAME</b>: {self.sender_username}\n\n"
                    f"<b>EMAIL: </b> [<i>{user_mail}</i>]\n\n"
                )
            else:
                return (
                    f"\n\n<b>STATUS</b>: not found!\n\n"
                    f"<b>MESSAGE</b>:couldn't found user [{self.sender_username}] data.\n\n"
                )
            
    def check_stored_mail_length(self) -> str:
        mail = [mail for key, mail in self.data.items()]
        return len(mail)

    def extract_user_mail(self) -> str:
        mail  = [mail["email"] for key, mail in self.data.items() if self.sender_username == mail["username"]]
        return mail[0]

    def check_existing_data(self) -> list:
        return [ prev_data["email"] for key, prev_data in self.data.items()]
    
    def push_data_information(self) -> None:
        self.ref.push({"username" : self.sender_username,"email": self.sender_email})
