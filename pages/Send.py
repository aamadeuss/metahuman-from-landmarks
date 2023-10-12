from src.sender import sender
import streamlit as st

state = st.session_state
if 'computed' not in state:
    state.computed = False
if state.computed:
    output = state.save
    unrealSender = sender(output, 60)
    st.button('Send data to UE', on_click=unrealSender.start)
else:
    st.write('# No data to send. \nPlease submit the JSONs folder and the conversion model for computing blendshapes.')