import streamlit as st
import streamlit_authenticator as stauth
import yaml


def authenticator():
    names = ['Costantino Terranova','user2']
    usernames = ['costa','12']
    passwords = ['123','456']


    hashed_passwords = stauth.Hasher(passwords).generate()

    authenticator = stauth.Authenticate(usernames=usernames,
        names=names,
        passwords=hashed_passwords, 
        cookie_name='some_cookie_name',
        key='some_signature_key',
        cookie_expiry_days=1)


    authentication_status = authenticator.login('Login','main')


    if authentication_status == False:
        st.write('Welcome *%s*' )
    # your application
    elif None in authentication_status:
        st.warning('Please enter your username and password')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
    else:
        return True
        
