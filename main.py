import multiprocessing
import tensorflow as tf
import streamlit as st
import json, time, os
from dotenv import main
from src.sender import sender
from mediapipe.framework.formats import landmark_pb2
from src.Blendshapes import blendshapes
from utils.collectionLists import filter_landmarks, blendshape_indices, MediapipeBlendShape
from src.pylivelinkface import PyLiveLinkFace, FaceBlendShape
import stqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import matplotlib.pyplot as plt

filenum = 0
source_folder = './Birch_new'

#check for number of jsons here, and return message if no jsons
main.load_dotenv()
model_path = os.getenv('MODEL_PATH')

if model_path != '':
    model = tf.keras.models.load_model(model_path)

def getLivelink(blendshapes):
    live_link_face = PyLiveLinkFace(fps=60, filter_size=4)
    to_ignore = ['_neutral', 'eyeBlinkRight', 'eyeLookDownLeft', 'eyeLookDownRight', 'eyeLookInLeft', 'eyeLookInRight', 'eyeLookOutLeft', 'eyeLookOutRight', 'eyeLookUpLeft', 'eyeLookUpRight']
    to_double = ['eyeBlinkLeft']
    for index, name in blendshape_indices.items():
        if name in to_ignore:
            continue
        if name in to_double:
            live_link_face.set_blendshape(FaceBlendShape(MediapipeBlendShape[name].value), (blendshapes[index]**2)*4.)
            live_link_face.set_blendshape(FaceBlendShape.EyeBlinkRight, (blendshapes[index]**2)*4.)
            continue
        live_link_face.set_blendshape(FaceBlendShape(MediapipeBlendShape[name].value), blendshapes[index])
    return live_link_face

def getFrame(filenum):
    # print('Processing frame: ' + str(filenum))
    frames_landmarks = []
    filename = source_folder + '/' + str(filenum) + '.json'
    try:
        with open(filename) as json_file:
            data = json.load(json_file)
            frame = data['landmark']
            landmark_subset = landmark_pb2.NormalizedLandmarkList(
                landmark=frame)
        frames_landmarks.append(landmark_subset)
    except FileNotFoundError:
        return None
    frame_input = []
    for i in filter_landmarks:
        frame_input.append([frame[i]['x'], frame[i]['y']])
    if len(frame_input) > 0:
        model_output = blendshapes(model, frame_input)
        model_output = model_output[0]
        return getLivelink(model_output)
    