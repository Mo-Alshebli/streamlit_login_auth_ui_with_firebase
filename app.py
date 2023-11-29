import streamlit as st

from streamlit_login_auth_ui_with_firebase.utils import initialize_firebase
from streamlit_login_auth_ui_with_firebase.widgets import __login__
initialize_firebase("https://chatapp-83af0-default-rtdb.firebaseio.com/","chatapp-83af0-firebase-adminsdk-ekpcr-759b8357f2.json")
__login__obj = __login__(auth_token = "pk_prod_D73N19AVYQ4X7RHWZ477B0Y5SRWM",
                    company_name = "Shims",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,)

LOGGED_IN= __login__obj.build_login_ui()
username= __login__obj.get_username()

if LOGGED_IN == True:

   st.markdown("Your Streamlit Application Begins here!")
   st.write(username)
                                      
