import streamlit as st
import basic_functions as bf
from datetime import datetime, timedelta, date
from authenticator import authenticator

st.title('BF 66 RECALL')

if authenticator():

    all_friends = bf.all_friends_reader()
    sessiondata = bf.session_data_reader()
    future = bf.future_week_reader()
    ### BULK
    name_to_write, surname_to_write = bf.person_to_write_calculator(
        sessiondata,
        all_friends,
        future)

    if st.checkbox(f'Write to {name_to_write.title()} {surname_to_write.title()}'): # , value=False inherit from future
        st.write('goodboy')
        # fai partire qui una funzione che mette nel session data che gli hai scritto
        ## e se non c'è, il giorno dopo te ne compaiono due

    ### ADDING A FRIEND
    add_friend_container = st.expander("Add a Friend")
    with add_friend_container:
        name = st.text_input("Name")
        surname = st.text_input("Surname")
        love = st.slider('How much do you love this person?',0,10)
        frequency = st.slider('I wanna hear them every X weeks',0,59)
        last_contact =  st.date_input(
            "Last Contact",
            date.today())
        ## run add friend function
        if st.button('add'):
            friend = bf.person(name, surname, love, frequency, last_contact)
            all_friends = bf.add_friend(friend, all_friends)

    ### MODIFYING RELATION
    modify_contact_container = st.expander("Heard From Someone?")
    with modify_contact_container:
        person = st.multiselect('What is his name?',
    (all_friends['name']+ ' ' + all_friends['surname']).values.tolist())
        last_contact = st.date_input(
            "When Did You Hear Him?",
            date.today())
        if st.button('modify'):
            bf.modifier(string=person, last_contact=last_contact, all_friends=all_friends)

    ### SHOW CALENDAR
    calendar_container = st.expander("Show Calendar")
    with calendar_container:
        # bf.call_calendar(future)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        image = st.pyplot(bf.call_calendar(future))