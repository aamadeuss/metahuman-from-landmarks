import streamlit as st
import os
from main import getFrame
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures
from utils.st_helpers import set_model_from_choice, set_jsons_folder

state = st.session_state
st.set_page_config(layout="wide")

if 'model' not in state:
    state.model = None

if 'jsons' not in state:
    state.jsons = None

if 'zip' not in state:
    state.zip = None

if 'save' not in state:
    state.save = []

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
    uploaded_zip = st.file_uploader('Choose folder:', key='zipfile', type='zip')
    submit_jsons_btn = st.form_submit_button(label='Submit',
                                             help='Submit the folder with jsons',
                                             on_click=lambda: state.update(jsons_submitted=True))
    if submit_jsons_btn:
        state.update(jsons=set_jsons_folder(state, uploaded_zip))

with col2.form('model_form'):
    st.subheader('Conversion Model')
    model_pick = st.selectbox('Choose the conversion model:', ('Mediapipe Landmarker', 'CNN Model', 'MLP Mixer Model', 'MobileNetV3'))
    submit_model_btn = st.form_submit_button(label='Submit',
                                             help='Submit the conversion model choice',
                                             on_click=lambda: state.update(model_submitted=True))
    if submit_model_btn:
        state.update(model=set_model_from_choice(state, model_pick))

st.divider()

if __name__ == '__main__':
    num = len(state.jsons) if state.jsons is not None else 0
    st.write('#### Number of frames: ' + str(num))
    num_workers = os.cpu_count()
    jobs = state.jsons
    mdl = state.model
    processed_jobs = {}

    compute = st.button('Compute', help='Compute the blendshapes')

    if compute and 'model' in state and 'jsons' in state:
        # st.write(getFrame(jobs[0]))
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            progress_bar = st.progress(0, text='Setting up...')
            for i, j in enumerate(jobs):
                # st.write(type(j))
                pj = executor.submit(getFrame, (mdl, j))
                # st.write(pj)
                processed_jobs[pj] = i
            output = [None] * num # pre_allocate slots
            for future in concurrent.futures.as_completed(processed_jobs):
                try:
                    idx = processed_jobs[future] # order of submission
                    output[idx] = future.result() # store result in correct order
                    p = round((idx+1)/num, 2) # progress at this stage stored in p as a number between 0 and 1
                    progress_bar.progress(p, text='Processing...   {}%'.format(int(p*100)))
                    # Incrementally save the completed task so far.
                    state.save.append(output[idx])
            
                except concurrent.futures.process.BrokenProcessPool as ex:
                    raise Exception(ex)
            progress_bar.empty()

    if len(state.save):
        st.write('#### Completed Jobs')
        state.update(computed=True)
        # st.write(f'{state.save}')