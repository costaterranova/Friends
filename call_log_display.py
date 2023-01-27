import streamlit as st
import basic_functions as bf
from datetime import datetime, timedelta, date

all_friends = bf.all_friends_reader()
sessiondata = bf.session_data_reader()
future = bf.future_week_reader()
### BULK
name_to_write, surname_to_write = bf.person_to_write_calculator(
    sessiondata,
    all_friends,
    future)

name_to_call, surname_to_call = bf.person_to_call_calculator(
    future)

st.write(f'call: {name_to_call} {surname_to_call}')
st.write(f'write to: {name_to_write} {surname_to_write}')

### ADDING A FRIEND
container = st.expander("Add a friend")
with container:
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
        st.write(friend)
        st.write(all_friends)

