import streamlit as st
import streamlit_authenticator as stauth
from utils import *

import yaml
from yaml.loader import SafeLoader
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
        st.write('Electric cars are on the rise... aren\'t they?. I like cats too.')

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
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
            with open('../config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)
##
    # ...


if __name__ == "__main__":
    main()
