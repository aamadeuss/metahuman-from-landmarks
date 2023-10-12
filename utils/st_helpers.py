import streamlit as st
import tensorflow as tf
import json
from zipfile import ZipFile

def set_model_from_choice(state, choice):
    # if state.model_submitted:    
    # st.write('here')
    if choice == 'Mediapipe Landmarker':
        model = 'models/face_landmarker_v2_with_blendshapes.task'
    elif choice == 'CNN Model':
        model = 'models/CNN_20_softplus.keras'
    elif choice == 'MLP Mixer Model':
        model = 'models/MLP_Mixer_10.t5'    
    try:
        state.model = tf.keras.models.load_model(model, compile=False)
        state.update(model_submitted=True)
        st.write('Model loaded!')
        return st.session_state.model
    except:
        st.write('Model loading error.')

# @st.cache_data
def set_jsons_folder(state, file):
    # if state.jsons_submitted:
    filepath = file.name
    zipfolder = ZipFile(file, 'r')
    state.zip = zipfolder
    filenames = ZipFile.namelist(zipfolder)
    filenames.sort(key=len)
    jsons = []
    with st.spinner('Loading JSONs folder...'):
        for filename in filenames:    
            with zipfolder.open(filename) as f:
                jsons.append(json.load(f))    
    state.jsons = jsons
    # st.write('here' + str(state.jsons))
    try:
        st.write('JSONs folder loaded from ' + str(filepath) + '!')
        return st.session_state.jsons
    except:
        st.write('JSONs folder loading error.')