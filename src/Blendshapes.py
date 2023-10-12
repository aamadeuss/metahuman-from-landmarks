import matplotlib.pyplot as plt 
from tensorflow import keras
from keras.datasets import mnist 
from keras.models import Sequential
import numpy as np
import pandas as pd
#import ast
import re
from tqdm import tqdm
#from sklearn.model_selection import train_test_split
import tensorflow as tf
# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

blendshape_indices = ['_neutral',
 'browDownLeft',
 'browDownRight',
 'browInnerUp',
 'browOuterUpLeft',
 'browOuterUpRight',
 'cheekPuff',
 'cheekSquintLeft',
 'cheekSquintRight',
 'eyeBlinkLeft',
 'eyeBlinkRight',
 'eyeLookDownLeft',
 'eyeLookDownRight',
 'eyeLookInLeft',
 'eyeLookInRight',
 'eyeLookOutLeft',
 'eyeLookOutRight',
 'eyeLookUpLeft',
 'eyeLookUpRight',
 'eyeSquintLeft',
 'eyeSquintRight',
 'eyeWideLeft',
 'eyeWideRight',
 'jawForward',
 'jawLeft',
 'jawOpen',
 'jawRight',
 'mouthClose',
 'mouthDimpleLeft',
 'mouthDimpleRight',
 'mouthFrownLeft',
 'mouthFrownRight',
 'mouthFunnel',
 'mouthLeft',
 'mouthLowerDownLeft',
 'mouthLowerDownRight',
 'mouthPressLeft',
 'mouthPressRight',
 'mouthPucker',
 'mouthRight',
 'mouthRollLower',
 'mouthRollUpper',
 'mouthShrugLower',
 'mouthShrugUpper',
 'mouthSmileLeft',
 'mouthSmileRight',
 'mouthStretchLeft',
 'mouthStretchRight',
 'mouthUpperUpLeft',
 'mouthUpperUpRight',
 'noseSneerLeft',
 'noseSneerRight']



filter_lndmarks = [0, 1, 4, 5, 6, 7, 8, 10, 13, 14, 17, 21, 33, 37, 39, 40, 46, 52, 53, 54, 55, 58, 61, 63, 65, 66, 67, 70, 78, 80,
81, 82, 84, 87, 88, 91, 93, 95, 103, 105, 107, 109, 127, 132, 133, 136, 144, 145, 146, 148, 149, 150, 152, 153, 154, 155, 157,
158, 159, 160, 161, 162, 163, 168, 172, 173, 176, 178, 181, 185, 191, 195, 197, 234, 246, 249, 251, 263, 267, 269, 270, 276, 282,
283, 284, 285, 288, 291, 293, 295, 296, 297, 300, 308, 310, 311, 312, 314, 317, 318, 321, 323, 324, 332, 334, 336, 338, 356,
361, 362, 365, 373, 374, 375, 377, 378, 379, 380, 381, 382, 384, 385, 386, 387, 388, 389, 390, 397, 398, 400, 402, 405,
409, 415, 454, 466, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477]


def blendshapes(model, frame_input,filter_lndmarks = filter_lndmarks,blendshape_indices = blendshape_indices):
    # frame_input = []
    # model = tf.keras.models.load_model(model_path)

    # for i in filter_lndmarks:
    #     frame_input.append([detection_result.face_landmarks[0][i].x,detection_result.face_landmarks[0][i].y])

    #change the shape in the next line and then the reshape after that
    frame_input = np.array(frame_input).reshape(1,478,3).astype('float32')
    # frame_input = np.expand_dims(frame_input, -1)
    frame_input = frame_input.reshape(1,1,478,3,1)
    output_data = model.predict(frame_input)

    return output_data
