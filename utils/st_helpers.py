import streamlit as st
import tensorflow as tf
import os
from zipfile import ZipFile

def set_model_from_choice(state, choice):
    # if state.model_submitted:    
    # st.write('here')
    if choice == 'Mediapipe Landmarker':
        state.model = 'models/face_landmarker_v2_with_blendshapes.task'
    elif choice == 'CNN Model':
        state.model = 'models/CNN_20_softplus.keras'
    elif choice == 'MLP Mixer Model':
        state.model = 'models/MLP_Mixer_10.t5'    
    try:
        # model = tf.keras.models.load_model(st.session_state.model)
        os.putenv('MODEL_PATH', st.session_state.model)
        state.update(model_submitted=True)
        st.write('Model loaded!')
        return st.session_state.model
    except:
        st.write('Model loading error.')

def set_jsons_folder(state, file):
    # if state.jsons_submitted:
    filepath = file.name
    os.putenv('JSONS_FOLDER_PATH', filepath)
    st.write(filepath)
    zipfolder = ZipFile(filepath)
    state.jsons = ZipFile.filelist(zipfolder)
    st.write('here' + str(state.jsons))
    try:
        st.write('JSONs folder loaded!')
        return st.session_state.jsons
    except:
        st.write('JSONs folder loading error.')