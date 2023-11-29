import re
import json
import re
import firebase_admin
from firebase_admin import credentials, db
from trycourier import Courier
import secrets
from argon2 import PasswordHasher
import requests
import streamlit as st

from firebase_admin import credentials, db

# Function to initialize Firebase
def initialize_firebase(url,json_auth):
    try:
        # Try to retrieve an existing app
        firebase_admin.get_app()
    except ValueError:
        # If the app doesn't exist, initialize it
        cred = credentials.Certificate(json_auth)
        firebase_admin.initialize_app(cred, {
            'databaseURL': url
        })

# Call the function to ensure Firebase is initialized
# Initialize PasswordHasher
ph = PasswordHasher()

@st.cache_data(ttl=None, show_spinner=True)
def check_usr_pass(username: str, password: str) -> bool:
    ref = db.reference('users')
    users = ref.get()
    for uid, user_details in users.items():
        if user_details['username'] == username:
            try:
                return ph.verify(user_details['password'], password)
            except:
                pass
    return False

@st.cache_data(ttl=None, show_spinner=True)
def load_lottieurl(url: str) -> str:
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        pass
        pass

def check_valid_name(name_sign_up: str) -> bool:
    return bool(re.search(r'^[A-Za-z_][A-Za-z0-9_]*', name_sign_up))



def check_valid_email(email_sign_up: str) -> bool:
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return bool(re.fullmatch(regex, email_sign_up))


@st.cache_data(ttl=None, show_spinner=True)
def check_unique_email(email_sign_up: str) -> bool:
    ref = db.reference('users')
    users = ref.get()
    return all(user['email'] != email_sign_up for user in users.values())


def non_empty_str_check(username_sign_up: str) -> bool:
    return bool(username_sign_up and not username_sign_up.isspace())

def check_unique_usr(username_sign_up: str):
    ref = db.reference('users')
    users = ref.get()
    if username_sign_up in (user['username'] for user in users.values()):
        return False
    return non_empty_str_check(username_sign_up)


@st.cache_data(ttl=None, show_spinner=True)
def register_new_usr(name_sign_up: str, email_sign_up: str, username_sign_up: str, password_sign_up: str) -> None:
    new_usr_data = {'username': username_sign_up, 'name': name_sign_up, 'email': email_sign_up, 'password': ph.hash(password_sign_up)}
    db.reference('users').push(new_usr_data)


@st.cache_data(ttl=None, show_spinner=True)
def change_passwd(email_: str, random_password: str) -> None:
    ref = db.reference('users')
    users = ref.get()
    for uid, user_details in users.items():
        if user_details['email'] == email_:
            user_details['password'] = ph.hash(random_password)
            ref.child(uid).update(user_details)
            break
        
@st.cache_data(ttl=None, show_spinner=True)
def check_email_exists(email_forgot_passwd: str):
    """
    Checks if the email entered is present in the Firebase database.
    """
    ref = db.reference('users')
    users = ref.get()

    for uid, user_details in users.items():
        if user_details['email'] == email_forgot_passwd:
            return True, user_details['username']
    return False, None


@st.cache_data(ttl=None, show_spinner=True)
def generate_random_passwd() -> str:
    """
    Generates a random password to be sent in email.
    """
    password_length = 10
    return secrets.token_urlsafe(password_length)


def send_passwd_in_email(auth_token: str, username_forgot_passwd: str, email_forgot_passwd: str, company_name: str, random_password: str) -> None:
    """
    Triggers an email to the user containing the randomly generated password.
    """
    client = Courier(auth_token = auth_token)

    resp = client.send_message(
    message={
        "to": {
        "email": email_forgot_passwd
        },
        "content": {
        "title": company_name + ": Login Password!",
        "body": "مرحبا! " + username_forgot_passwd + "," + "\n" + "\n" + "كلمة المرور الافتراضية الخاصة فيك هي : " + random_password  + "\n" + "\n" + "{{info}}"
        },
        "data":{
        "info": "يرجى إعادة تعيين كلمة المرور الخاصة بك في أقرب وقت ممكن لأسباب أمنية."
        }
    }
    )


@st.cache_data(ttl=None, show_spinner=True)
def change_passwd(email_: str, random_password: str) -> None:
    """
    Replaces the old password with the newly generated password in Firebase.
    """
    ref = db.reference('users')
    users = ref.get()

    for uid, user_details in users.items():
        if user_details['email'] == email_:
            user_details['password'] = ph.hash(random_password)
            ref.child(uid).update(user_details)
            break


@st.cache_data(ttl=None, show_spinner=True)
def check_current_passwd(email_reset_passwd: str, current_passwd: str) -> bool:
    ref = db.reference('users')
    users = ref.get()
    for uid, user_details in users.items():
        if user_details['email'] == email_reset_passwd:
            try:
                return ph.verify(user_details['password'], current_passwd)
            except:
                pass
    return False

# Author: Gauri Prabhakar
# GitHub: https://github.com/GauriSP10/streamlit_login_auth_ui
