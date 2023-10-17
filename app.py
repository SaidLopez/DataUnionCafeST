from yaml.loader import SafeLoader
import yaml
import streamlit as st
import streamlit_authenticator as stauth
from utils import *

st.set_page_config(layout="wide")


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


def main():
    # Register your pages
    pages = {
        "Log in": logIn,
        "Register": register,
    }

    st.sidebar.title("What would you like to do today?")

    # Widget to select your page, you can choose between radio buttons or a selectbox
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))
    # page = st.sidebar.selectbox("Select your page", tuple(pages.keys()))

    # Display the selected page
    pages[page]()


def userviews():
    # Register your pages
    pages = {
        "Price Comparison": priceComparison,
        "Who holds my data?": whoHoldsMyData,
    }

    st.sidebar.title("User options")

    # Widget to select your page, you can choose between radio buttons or a selectbox
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))
    # page = st.sidebar.selectbox("Select your page", tuple(pages.keys()))

    # Display the selected page
    pages[page]()


def priceComparison():
    st.title("Your data says...")
    option = st.selectbox("What would you like to see?", [
                          "Top 20 items bought", "Top money spent on...", 'Your basket over the years...'])

    if option == "Top 20 items bought":
        st.pyplot(most_consumed_items())
        st.write('Looking at that graph... perhaps you like Tea a bit too much?')

    elif option == "Top money spent on...":
        st.pyplot(most_money_spent())
        st.write('Electric cars are on the rise... aren\'t they?')

    elif option == "Your basket over the years...":
        st.pyplot(basket_price())


def whoHoldsMyData():
    st.title("Who holds my data?")
    st.write("Your data is currently being hold by... Tesco Ltd.")
    st.dataframe(data=your_tesco_data())

    remove_data = st.checkbox('Request my data to be removed')

    if remove_data:
        st.write(
            'Great! We have requested your data to be removed. You will receive a confimation by email.')


def logIn():
    name, authentication_status, username = authenticator.login(
        'Login', 'main')
    if authentication_status:
        authenticator.logout('Logout', 'main')
        if username == 'charlieg':
            st.write(f'Welcome *{name}*')

        elif username == 'rbriggs':
            st.write(f'Welcome *{name}*')
            st.title('Application 2')
        userviews()

    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')


def register():

    ptext1 = st.empty()
    ptext2 = st.empty()
    placeholder = st.empty()

    if "first_form_clicked" not in st.session_state:
        st.session_state["first_form_clicked"] = False

    if "second_form_clicked" not in st.session_state:
        st.session_state["second_form_clicked"] = False

    if "third_form_clicked" not in st.session_state:
        st.session_state["third_form_clicked"] = False

    if "fourth_form_clicked" not in st.session_state:
        st.session_state["fourth_form_clicked"] = False

    if "fifth_form_clicked" not in st.session_state:
        st.session_state["fifth_form_clicked"] = False

    if not st.session_state["first_form_clicked"]:
        ptext1.title("Create your account")
        ptext2.write("So we can keep your data safe")
        try:
            with placeholder.form("registration_form1"):
                st.write("Step 1")
                st.session_state["username"] = st.text_input('Username')
                st.session_state["password"] = st.text_input(
                    'Password', type='password')
                st.session_state["confirm_password"] = st.text_input(
                    'Retype your password', type='password')
                st.session_state["email"] = st.text_input(
                    'Email')
                st.session_state["MFAOption"] = st.selectbox(
                    "To use Beanies you have to enable 2 Factor Authentication", ['Phone', "Email"])
                if st.session_state["password"] != st.session_state["confirm_password"]:
                    st.write("Passwords don't match")
                st.form_submit_button(
                    label="Continue", on_click=callback, args=['first_form_clicked'])
        except Exception as e:
            st.error(e)

    if st.session_state["first_form_clicked"]:
        try:
            with placeholder.form("registration_form2"):
                st.write("Step 2")
                st.session_state['MFAanswer'] = st.text_input(
                    f'Introduce the code sent to your {st.session_state["MFAOption"]}')
                st.form_submit_button(
                    label="Continue", on_click=callback, args=['second_form_clicked'])
        except Exception as e:
            st.error(e)

    if st.session_state["second_form_clicked"]:
        ptext1.title("Read & Agree T&Cs")
        ptext2.write("So we are all on the same page")
        try:
            with placeholder.form("registration_form3"):
                st.write("Step 3")
                """Read and understand the Data Union Cafe's T&Cs"""
                with st.expander("T&Cs"):
                    """Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                     Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
                     Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
                     Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
                st.session_state["T&C"] = st.checkbox(
                    "I accept the terms and conditions")
                st.form_submit_button(
                    label="Continue", on_click=callback, args=['third_form_clicked'])
        except Exception as e:
            st.error(e)

    if st.session_state["third_form_clicked"]:
        ptext1.title("Now for the fun bit.")
        ptext2.write("We will help you fetch your loyalty data.")
        try:
            with placeholder.form("registration_form4"):
                st.write("Step 4")
                """We made it! Let's start with which loyalty programs you are a member of and we will show you how to get your data from them."""

                st.write("*your loyalty card programs*")
                st.session_state["tescoProgram"] = st.checkbox(
                    "Tesco Clubcard")
                st.session_state["MorrisonsProgram"] = st.checkbox(
                    "Morrisons Clubcard")
                st.session_state["SainsburysProgram"] = st.checkbox(
                    "Sainsburys Clubcard")
                st.form_submit_button(
                    label="Continue", on_click=callback, args=['fourth_form_clicked'])
        except Exception as e:
            st.error(e)

    if st.session_state["fourth_form_clicked"]:

        try:
            with placeholder.form("registration_form5"):
                st.write("Step 4")
                """Send this email template along with a picture of your *photo ID* and
                *proof of addres to the following email addresses."""

                with st.expander("Legal GDPR template"):
                    """Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                     Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
                     Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
                     Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

                c1, c2 = st.columns(2)
                with c1:
                    """"""
                    """"""
                    """"""
                    """"""
                    st.markdown(
                        "<span style='background-color: green; font-size: xx-large; margin: auto; width: 50%;border: 3px solid red ;padding: 10px;'>30 days</span>", unsafe_allow_html=True)
                with c2:
                    """Once you have your data upload it below and let us show you some great analytics"""
                    st.file_uploader("Files, JSON", accept_multiple_files=True)

                """"""
                """"""
                st.form_submit_button(
                    label="Submit", on_click=callback, args=['fifth_form_clicked'])

        except Exception as e:
            st.error(e)

    if st.session_state["fifth_form_clicked"]:
        st.title('Perfect, you can login and view your data')


def callback(value):
    st.session_state[value] = True


if __name__ == "__main__":
    main()
