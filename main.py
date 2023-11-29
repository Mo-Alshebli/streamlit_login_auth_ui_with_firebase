from streamlit_login_auth_ui_with_firebase.widgets import __login__

import streamlit as st
from streamlit_login_auth_ui_with_firebase.widgets import __login__

__login__obj = __login__(auth_token = "pk_prod_D73N19AVYQ4X7RHWZ477B0Y5SRWM",
                    company_name = "Shims",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = True,
                    hide_footer_bool = False,
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:

    st.text("Your Streamlit Application Begins here!")