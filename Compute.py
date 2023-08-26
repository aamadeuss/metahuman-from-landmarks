import multiprocessing
import tensorflow as tf
import streamlit as st
import json, time, os
from src.sender import sender
from mediapipe.framework.formats import landmark_pb2
from src.Blendshapes import blendshapes
from utils.collectionLists import filter_landmarks, blendshape_indices, MediapipeBlendShape
from src.pylivelinkface import PyLiveLinkFace, FaceBlendShape
from main import getFrame
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures
import stqdm
from utils.st_helpers import set_model_from_choice

state = st.session_state
st.set_page_config(layout="wide")

if 'model' not in st.session_state:
    st.session_state.model = None

if 'save' not in st.session_state:
    st.session_state.save = []

if 'jsons_submitted' not in state:
    state.jsons_submitted = False

if 'model_submitted' not in state:
    state.model_submitted = False

# if 'to_compute' not in state:
#     state.to_compute = False

if 'computed' not in state:
    state.computed = False

st.header('Send face data to UE')
st.divider()

col1, col2 = st.columns(2)
with col1.form('jsons_form'):
    st.subheader('JSONs Folder')
    st.file_uploader('Choose folder:', key='zipfile', type='zip')
    submit_jsons_btn = st.form_submit_button(label='Submit',
                                             help='Submit the folder with jsons',
                                             on_click=lambda: state.update(jsons_submitted=True))
    if submit_jsons_btn:
        st.write(os.path())

with col2.form('model_form'):
    st.subheader('Conversion Model')
    model_pick = st.selectbox('Choose the conversion model:', ('Mediapipe Landmarker', 'CNN Model', 'MLP Mixer Model'))
    submit_model_btn = st.form_submit_button(label='Submit',
                                             help='Submit the conversion model choice',
                                             on_click=lambda: state.update(model_submitted=True))
    if submit_model_btn:
        state.update(model=set_model_from_choice(state, model_pick))

st.divider()

if __name__ == '__main__':
    num = 242
    num_workers = os.cpu_count()
    jobs = range(num)
    processed_jobs = {}

    compute = st.button('Compute', help='Compute the blendshapes')

    if compute and state.model is not None:
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            progress_bar = st.progress(0, text='Setting up...')
            for j in jobs:
                pj = executor.submit(getFrame, j)
                processed_jobs[pj] = j
            output = [None] * num # pre_allocate slots
            for future in concurrent.futures.as_completed(processed_jobs):
                try:
                    idx = processed_jobs[future] # order of submission
                    output[idx] = future.result() # store result in correct order
                    p = round((idx+1)/num, 2) # progress at this stage stored in p as a number between 0 and 1
                    progress_bar.progress(p, text='Processing...   {}%'.format(int(p*100)))
                    # Incrementally save the completed task so far.
                    st.session_state.save.append(output[idx])
            
                except concurrent.futures.process.BrokenProcessPool as ex:
                    raise Exception(ex)
            progress_bar.empty()

    if len(st.session_state.save):
        st.write('#### Completed Jobs')
        state.update(computed=True)
        # st.write(f'{st.session_state.save}')