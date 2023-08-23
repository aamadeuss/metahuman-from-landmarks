import cv2, copy, json, numpy as np, transforms3d
from src.Blendshapes import blendshapes
from src.pylivelinkface import PyLiveLinkFace,FaceBlendShape
from mediapipe.framework.formats import landmark_pb2 
from utils.face_geometry import (PCF, get_metric_landmarks, procrustes_landmark_basis)
from utils.collectionLists import MediapipeBlendShape, filter_landmarks, blendshape_names, blendshape_indices

# points of the face model that will be used for SolvePnP later
points_idx = [33, 263, 61, 291, 199]
points_idx = points_idx + [key for (key, val) in procrustes_landmark_basis]
points_idx = list(set(points_idx))
points_idx.sort()

def calculate_rotation(face_landmarks, pcf: PCF, image_shape):
    frame_width, frame_height, channels = image_shape
    focal_length = frame_width
    center = (frame_width / 2, frame_height / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]], [0, focal_length, center[1]], [0, 0, 1]],
        dtype="double",
    )

    dist_coeff = np.zeros((4, 1))

    landmarks = np.array(
        [(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark[:468]]

    )
    landmarks = landmarks.T

    metric_landmarks, pose_transform_mat = get_metric_landmarks(
        landmarks.copy(), pcf
    )

    model_points = metric_landmarks[0:3, points_idx].T
    image_points = (
        landmarks[0:2, points_idx].T
        * np.array([frame_width, frame_height])[None, :]
    )

    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points,
        image_points,
        camera_matrix,
        dist_coeff,
        flags=cv2.SOLVEPNP_ITERATIVE,
    )

    return pose_transform_mat, metric_landmarks, rotation_vector, translation_vector

class jsonProcessor():
    def __init__(self, model, source_folder = './output_jsons'):
        self.source_folder = source_folder
        self.filenum = 0
        self.model = model

        self.image_height, self.image_width, channels = (480, 640, 3)
        focal_length = self.image_width
        center = (self.image_width/2, self.image_height/2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]],
            dtype = "double",
        )

        self.live_link_face = PyLiveLinkFace(fps=60, filter_size=4)
        self.pcf = PCF(
            near=1,
            far=10000,
            frame_height=self.image_height,
            frame_width=self.image_width,
            fy=camera_matrix[1, 1],
        )

        self.output = []

    def process(self):
        while self.filenum < 1364:
            print('Processing frame: ' + str(self.filenum))
            frames_landmarks = []

            filename = self.source_folder + '/' + str(self.filenum) + '.json'
            with open(filename) as json_file:
                data = json.load(json_file)
                frame = data['landmark']
                landmark_subset = landmark_pb2.NormalizedLandmarkList(
                    landmark=frame)
            frames_landmarks.append(landmark_subset)

            for face_landmarks in frames_landmarks:
                pose_transform_mat, metric_landmarks, rotation_vector, translation_vector = calculate_rotation(face_landmarks, self.pcf, (self.image_width, self.image_height, 3))  
                
                # calculate and set all the blendshapes
                # self.blendshape_calulator.calculate_blendshapes(
                #     self.live_link_face, metric_landmarks[0:3].T, face_landmarks.landmark)
                
                # calculate the head rotation out of the pose matrix
                eulerAngles = transforms3d.euler.mat2euler(pose_transform_mat)
                pitch = -eulerAngles[0]
                yaw = eulerAngles[1]
                roll = eulerAngles[2]
                self.live_link_face.set_blendshape(
                    FaceBlendShape.HeadPitch, pitch)
                self.live_link_face.set_blendshape(
                    FaceBlendShape.HeadRoll, roll)
                self.live_link_face.set_blendshape(FaceBlendShape.HeadYaw, yaw)

            frame_input = []
            for i in filter_landmarks:
                frame_input.append([frame[i]['x'], frame[i]['y']])
            self.filenum += 1
            if len(frame_input) > 0:
                output_data = blendshapes(self.model, frame_input)
                self.setBlendShapeValues(output_data[0])
                self.output.append(copy.deepcopy(self.live_link_face))

        return self.output

    def setBlendShapeValues(self, blendshape_values):
        # 'eyeBlinkLeft', 'eyeBlinkRight'
        to_ignore = ['_neutral', 'eyeLookDownLeft', 'eyeLookDownRight', 'eyeLookInLeft', 'eyeLookInRight', 'eyeLookOutLeft', 'eyeLookOutRight', 'eyeLookUpLeft', 'eyeLookUpRight']
        for index, name in blendshape_indices.items():
            if name in to_ignore:
                continue
            self.live_link_face.set_blendshape(FaceBlendShape(MediapipeBlendShape[name].value), blendshape_values[index])
            # self.live_link_face.set_blendshape(FaceBlendShape.JawOpen, 1 - blendshape_values[27])
        return
    